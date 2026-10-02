# Frozen deterministic selection — H.6

Eligible instruments are all files in instruments/*.yaml at base
fae0c0b742cd3bcbc7b54599fa9f6234b0ffdc4b whose extraction.status is accepted.
Use their unchanged five fields. Family = extraction.practice, exactly as recorded.

Visit T01 through T06, three slots each. Choose from families not already used for
that target. Among eligible instruments minimize the tuple:
(global prior use count, SHA256(UTF8("H6-natural-v0.1|" + target_id + "|" +
slot_number + "|" + instrument_id)), instrument_id).
Slot numbers are 1, 2, 3. Increment use count after each choice. No target wording,
semantic similarity, predicted success, or outcome enters selection. Freeze all
18 pairings before generation. No replacement, even for awkward pairings.
