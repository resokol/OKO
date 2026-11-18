# OKO 1.8.4 preview — spoken historical corrections and dealer handout

Date: 2026-11-18. User-confirmed keyword: «Ошибка».

## Behavior

«Ошибка, бокс два, рейз до пяти тысяч» selects the most recent accepted action of that seat in the current betting street, even when other players acted afterwards. «Первое действие» or «действие один» selects an older occurrence for that seat. «Правильно бокс четыре чек» can replace the assigned seat; explicit «последнее действие» selects global latest. A standalone keyword arms correction across a pause, and every replacement names its seat.

The bounded512-action journal retains explicit/implicit intent, record/command identity and cursor checkpoints. A valid edit replays retained intents, preserves later explicit seats and recalculates later implicit assignments. Conflicts reject the entire edit without changing values or cursor. Repeating an equivalent correction before a new ordinary action keeps the same target even if its corrected seat has changed. Discarded-history counts retain absolute action numbering; a missing/evicted target never falls back to a different action. Visible history remains bounded20, with amended values, raw utterances, and distinct correction/request labels.

Lifecycle resets clear the journal and pending selection. No manual transcript route, chip ledger, camera control or PokerVision write integration was added. OutputConnected remains false. The default Vosk engine/model and CPU isolation are unchanged.

## Verification

- Full application suite: **320/320 passed**, including selection of earlier actions, indexed occurrences, fold/all-in reversal, explicit anchors, later implicit reassignment, atomic conflicts, missing targets, pauses, duplicates, lifecycle fencing, bounded history and repeated seat-changing correction. Regression tests first reproduced missing functionality and the two discovered boundary/retargeting defects, then passed after fixes.
- Independent read-only code review reported no Critical/Important findings in historical selection, replay, rollback or lifecycle paths. Native validation was performed separately by the implementer.
- Real Vosk 0.3.45 / small-ru-0.22 recognized standalone «ошибка». Through the isolated native worker and real speech API, the keyword followed by a native «бокс один чек» replaced an earlier seat1 raise, preserved a later seat2 call and retained expected next3. No platform writes occurred.
- Seven existing synthetic poker WAVs produced identical transcripts with the baseline and expanded vocabulary. Acoustic accuracy remains imperfect: combined correction samples sometimes produced incomplete text; this is not an accuracy guarantee for dealer hardware. The handout recommends a pause after the keyword.
- Browser verification passed for amended original values, raw audit, correction/request labels, pending replacement, invalid-edit atomicity, continuing implicit turns, earlier edits, and seat-change replay; no JS errors or horizontal overflow at1440/320. Captures inspected.
- Dealer PDF inspected as two A4 pages: commands, turn order, latest/older/indexed/seat corrections. No buttons, setup instructions, API/platform architecture or implementation descriptions. Native Windows/vMix/Hollyland were not available in this Linux environment.

Public distribution contains compiled binaries, packaging tools and user docs/PDF only. Previous releases and stable OKO.exe are retained.

Windows EXE: 50,516,898 bytes; SHA-256 `6f2a8235a067cd20b110d973a02b123e8b302c0f0c5685644042643f2b7b99f7`. Dealer PDF: 56,517 bytes; SHA-256 `14e5dccd6a9d783625b20489c7086fbe70a859d98b769dca27f2441b9ab97572`.
