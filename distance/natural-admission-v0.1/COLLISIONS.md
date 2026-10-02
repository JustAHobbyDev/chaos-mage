# Packet-local collision monitoring and offline preflight

Production evaluation contexts contain exactly one mapping packet. Multiple independent
processes are not simultaneous availability to one annotator. Source instrument/target
are named inputs without mapping Pxxx tables. Operator audit visits one packet at a
time; cross-case reporting receives findings/metrics, not multiple raw span tables.

Exposure PROV_LOCAL_ID_COLLISION_EXPOSURE is non-failing and emitted iff two or more
mapping packets are simultaneously available to an annotator and reuse a Pxxx ID.
Count per context; also list packet sets. Reused IDs across separate contexts are normal.

PROV_PACKET_ID_COLLISION_FAILURE requires all five:
1. >=2 packets simultaneously available;
2. a reused local source_id;
3. annotation cites that bare local ID;
4. representation accepts it or cannot uniquely resolve intended packet;
5. material wrong-packet SUPPORT/CONTEXT, genuine reviewer ambiguity of intended
   packet/span, or a legitimate cross-packet support relation impossible to express.
Case 5c's direct representational impossibility can establish failure without forcing
an invalid annotation through the other checks. Preserve the legitimate requirement.
A wrong citation with only one packet is initially a model error, not collision.

Offline preflight cases use existing H.5 historical fixtures and synthetic engineering
packet pairs. These are never provider measurements or generation controls. Verify:
- same local IDs in separate contexts: no exposure/failure;
- simultaneous reuse: exposure, no automatic failure;
- envelope mismatch rejected, no global fallback;
- correctly bound semantic support: accepted, no failure;
- strongest adversarial example: A/P003 says inspect evaluator scores; B/P003 says
  offsets +2 through +5 are incompatible; envelope A, bare P003, component states B's
  assertion. Mechanical ID existence may pass, but closed-bundle semantic review is
  INSUFFICIENT. A deliberately recorded false semantic acceptance must trigger failure;
- single-packet wrong citation: model error only;
- genuinely required cross-packet relation cannot be represented: explicit 5c case;
- remove each necessary condition: no collision-caused failure (except direct 5c).

The harness does not pretend to infer semantic support algorithmically. Preflight uses
explicit recorded engineering facts for material wrong-packet use, accepted support,
reviewer ambiguity and representational impossibility. H.5 mechanical acceptance alone
must never be reported as semantic acceptance. Engineering exposures are reported in
a separate preflight count, excluded from the 18 natural measurements.
