# U1 unresolved-dependency metadata recovery

The last Stage B response completed successfully, passed both frozen JSON schemas,
and reported DEPENDENCY_UNCERTAIN with a classified embedded operation. It put D1
in unresolved_dependencies rather than inventing a concrete resolved operation.
The local validator required equality between embedded-classification IDs and only
the resolved dependency IDs. That extra representation assertion conflicts with the
prompt's explicit unresolved-dependency path. It does not identify a provider,
scientific classification, or contract-judgment failure.

Original response, request, events, exit, reservation, failure and pause are retained
byte-for-byte under original/. evidence.json binds their hashes, original session,
execution commit and the input allowlist. contracts.py, all schemas, prompts, cases,
packets and prior observations remain unchanged. The provider never sees local
validation implementation or this recovery code.

The additive recovery.py validator is bound to this exact unchanged response.
It links the companion D1 record to the explicitly named unresolved D1 instead of
requiring a resolved operation. Every other original validation assertion remains.
It neither invents an obligation nor changes closure. U1 still cannot aggregate to
SATISFIED even if its governance judgment passes. Ten offline regression tests pass,
including altered scientific-field rejection and unchanged validation of all other
25 responses. No repeat request or additional model call is authorized or needed.

Supplementary evidence is appended; the original failure and PAUSED_EVENT record
remain. A new validation.json may be created only because none existed; it labels
itself supplementary and references the original failure. The observation is copied
from the original response bytes into its previously absent judgment path. Committed
non-contamination evidence precedes the append-only recovery transition and Stage B
freeze. Stage C still uses the original runner, prompts, schemas and validator;
only offline freezing and final metrics use the bound metadata supplement.

Authority: the handoff's existing recovery policy and the user's explicit approval
until H6.R2 completion. This is engineering recovery, not a budget-authorized retry,
terminal-state precedence change, or provider no-observation policy.
