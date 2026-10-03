# H6.R3 continuation after first authorized batch

Only the first three Stage A sessions were approved and consumed. R3K01-C1, R3K02-C1 and R3K03-C1 are complete and may never be rescheduled. Ten Stage A sessions remain. Stage B/C are not authorized by that limited approval. No stage-wide classification freeze exists yet.

Current cumulative financial plan remains budgets/plan-001.json, hash 20751994b986b5f32d8fbcc253196c03b2769612cde920663ef1618125e6be1b. The ledger approval reference explicitly limits consent to the first three Stage A sessions; an allowed ledger status does not expand user authorization. Fresh per-batch usage forecasts and applicable consent remain required, with reserve 10 points. Bookkeeping for batch 0000 is complete; the sample is excluded because isolation and settling were not established.

The complete raw records for the first batch are already archived and partially frozen. When the whole stage is complete, use `python -B distance/compound-obligation-calibration-v0.2/freeze_stage.py classification`. This offline adapter runs the unchanged frozen runner's validations and freeze logic, accepting an existing archive only if every byte matches. It cannot overwrite differing evidence or run a provider. Two archive regression tests pass. The scientific runner, schemas, prompts and executed inputs are unchanged.

After committing the full Stage A freeze: prepare dependency packets, commit them, reforecast and obtain applicable authorization. Stage B classifications freeze before deterministic resolve-dependencies and the obligation-set freeze. The complete Stage C projection barrier and actual P2 preflight remain mandatory. Follow PROTOCOL.md through final audit; no natural-claim test or historical continuation.
