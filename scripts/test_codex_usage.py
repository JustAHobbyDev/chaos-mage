import copy
from datetime import datetime, timezone
import unittest

from codex_usage import UsageError, normalize, predict, sample_rate


NOW = 1800000000


def snapshot(used, captured, reset=NOW + 10000, secondary=None):
    result = {'rateLimits': {'limitId': 'codex', 'planType': 'test-plan',
                            'primary': {'usedPercent': used, 'windowDurationMins': 10080,
                                        'resetsAt': reset}, 'secondary': secondary},
              'rateLimitResetCredits': {'availableCount': 2, 'credits': [
                  {'id': 'DO-NOT-STORE', 'expiresAt': NOW + 20000}]}}
    return normalize(result, 'test-account', datetime.fromtimestamp(captured, timezone.utc).isoformat())


class UsageTests(unittest.TestCase):
    def setUp(self):
        self.current = snapshot(18, NOW)
        self.sample = {'usage_profile': 'astra-high-h6-claim', 'isolated_account_work': True,
                       'sessions': 20, 'before': snapshot(10, NOW - 600),
                       'after': snapshot(20, NOW - 300)}
        self.calibration = {'version': 1, 'samples': [self.sample]}
        self.plan = {'experiment_id': 'test', 'stages': [
            {'id': 'claims', 'sessions': 50, 'usage_profile': 'astra-high-h6-claim'}]}

    def predict(self, **kwargs):
        return predict(self.plan, self.current, self.calibration, as_of=NOW, **kwargs)

    def test_percentage_points_are_not_percent_of_remaining(self):
        report = self.predict()
        w = report['windows'][0]
        self.assertEqual(w['remaining_percent'], 82)
        self.assertEqual(w['predicted_percentage_points'], [22.5, 34.375])
        self.assertEqual(w['percent_of_remaining_allowance'], [27.44, 41.92])
        self.assertEqual(w['predicted_remaining_percent'], [47.625, 59.5])
        self.assertEqual(w['risk_to_reserve'], 'LOW')
        self.assertFalse(report['approval_required'])
        self.assertIsNone(report['exhaustion_probability'])

    def test_unknown_calibration_requires_approval(self):
        self.calibration['samples'] = []
        report = self.predict()
        self.assertTrue(report['approval_required'])
        self.assertIsNone(report['windows'][0]['predicted_percentage_points'])

    def test_high_and_borderline_risk(self):
        self.plan['stages'][0]['sessions'] = 120
        self.assertEqual(self.predict()['windows'][0]['risk_to_reserve'], 'BORDERLINE')
        self.plan['stages'][0]['sessions'] = 180
        self.assertEqual(self.predict()['windows'][0]['risk_to_reserve'], 'HIGH')

    def test_sample_crossing_reset_is_excluded(self):
        self.sample['after']['windows'][0]['resets_at'] += 10080 * 60
        report = self.predict()
        self.assertEqual(report['windows'][0]['risk_to_reserve'], 'UNKNOWN')
        self.assertIn('reset', report['excluded_samples'][0]['reason'])

    def test_saturated_and_decreasing_samples_are_excluded(self):
        for used in (100, 5):
            with self.subTest(used=used):
                self.sample['after']['windows'][0]['used_percent'] = used
                self.assertEqual(self.predict()['windows'][0]['risk_to_reserve'], 'UNKNOWN')

    def test_unattributed_work_is_excluded(self):
        self.sample['isolated_account_work'] = False
        self.assertEqual(self.predict()['windows'][0]['risk_to_reserve'], 'UNKNOWN')

    def test_profile_or_account_or_plan_mismatch_is_unknown(self):
        original = copy.deepcopy(self.sample)
        self.sample['usage_profile'] = 'different-model-and-context'
        self.assertTrue(self.predict()['approval_required'])
        self.calibration['samples'][0] = copy.deepcopy(original)
        self.calibration['samples'][0]['after']['account_scope'] = 'different-account'
        self.assertTrue(self.predict()['approval_required'])
        self.calibration['samples'][0] = copy.deepcopy(original)
        self.calibration['samples'][0]['after']['windows'][0]['plan_type'] = 'different-plan'
        self.assertTrue(self.predict()['approval_required'])

    def test_stale_or_future_snapshot_stops_prediction(self):
        for offset in (-301, 1):
            self.current = snapshot(18, NOW + offset)
            self.assertTrue(self.predict()['approval_required'])

    def test_passed_reset_requires_refresh_and_is_not_assumed_full(self):
        self.current = snapshot(18, NOW, reset=NOW)
        report = self.predict()
        self.assertEqual(report['windows'][0]['remaining_percent'], 82)
        self.assertTrue(report['approval_required'])

    def test_available_resets_do_not_increase_allowance(self):
        self.current['available_reset_credits'] = 99
        self.plan['stages'][0]['sessions'] = 180
        self.assertEqual(self.predict()['windows'][0]['risk_to_reserve'], 'HIGH')

    def test_zero_remaining_does_not_divide_by_zero(self):
        self.current = snapshot(100, NOW)
        w = self.predict()['windows'][0]
        self.assertEqual(w['risk_to_reserve'], 'HIGH')
        self.assertIsNone(w['percent_of_remaining_allowance'])

    def test_rounding_prevents_zero_delta_from_becoming_free(self):
        self.sample['after']['windows'][0]['used_percent'] = 10
        low, high, _ = sample_rate(self.sample, self.current, self.current['windows'][0], NOW)
        self.assertEqual(low, 0)
        self.assertGreater(high, 0)

    def test_no_windows_is_unknown_not_unlimited(self):
        self.current['windows'] = []
        self.assertTrue(self.predict()['approval_required'])

    def test_multiple_buckets_and_windows_are_all_preserved(self):
        raw = {'rateLimitsByLimitId': {key: {'planType': 'test', 'primary': {
            'usedPercent': percent, 'windowDurationMins': 300, 'resetsAt': NOW + 100},
            'secondary': {'usedPercent': 50, 'windowDurationMins': 10080, 'resetsAt': NOW + 500}}
            for key, percent in [('codex', 5), ('other-model', 99)]}}
        value = normalize(raw, 'test-account')
        self.assertEqual(len(value['windows']), 4)
        self.assertIsNone(value['available_reset_credits'])

    def test_snapshot_drops_reset_ids(self):
        self.assertNotIn('DO-NOT-STORE', str(self.current))
        self.assertEqual(self.current['reset_credit_expirations'], [NOW + 20000])

    def test_unknown_fanout_requires_approval(self):
        self.plan['stages'][0]['sessions'] = None
        self.assertTrue(self.predict()['approval_required'])

    def test_historical_different_reset_epoch_can_calibrate_same_window_type(self):
        # The pair must share an epoch; the current snapshot may be a later epoch.
        self.current['windows'][0]['resets_at'] += 10080 * 60
        self.assertFalse(self.predict()['approval_required'])

    def test_bad_values_fail_closed(self):
        for reserve in (-1, 101, float('nan')):
            with self.assertRaises(UsageError):
                self.predict(reserve_points=reserve)


if __name__ == '__main__':
    unittest.main()
