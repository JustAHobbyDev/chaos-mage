# Judgment retention

Raw events, stderr, prompts, response files, reservations, and validation records
live under ignored `.runtime/distance-v0.1/`. Never overwrite a reserved run or
repair an output by feeding it back to a classifier. A and B are independent
replicates using the same configuration, not different model families.

After all initial judgments have been frozen by a result hash manifest, validated
responses may be copied unchanged here as the named calibration snapshot. The
review and reference labels are separate artifacts and never classifier inputs.
Raw runtime files are not committed. Failed runs remain in the result manifest;
missing pairs prevent a complete calibration report rather than shrinking its
denominator silently.
