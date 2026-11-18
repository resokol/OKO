# OKO 1.8.1 preview — expanded dealer vocabulary

Date: 2026-11-18. Small speech-module update on top of 1.8.0; no director, vMix, capture, queue or platform-writer changes.

## Behavior

- Ordinal seats 1–10: «первый чек», «третий бокс чек», «бокс третий чек». Both е/ё spellings of четвёртый are accepted.
- Natural actions: сбросил/скинул → fold; уравнял → call; поднял/повысил до → raise-to; поднял/повысил на → raise-by; поставил → bet.
- Old labeled/cardinal commands and exact glued seat repairs remain supported. Mixed command sequences preserve order. Ordinals never become chip amounts; missing numbers, missing raise direction, unknown tails and ambiguous amounts remain rejected.
- Vosk grammar includes the new supported model words; Whisper context prompt includes ordinal examples. No new model download is needed.

## Evidence

The four new positive parser/grammar tests failed before implementation with the expected missing-seat/missing-phrase errors; the remaining suite passed (276/280). After implementation the complete suite passed **280/280**. This covers all ten ordinals, both label positions, action synonyms, mixed sequences with complete amounts, positive/zero/unknown amounts, missing до/на, unknown seats and unknown residual speech.

Native Vosk 0.3.45 / small-ru-0.22 was loaded and queried for every new active vocabulary word. The model contains четвёртый but not четвертый, so the existing model-word filter keeps the ё spelling and the parser normalizes it. Words absent from this model (e.g. заколлировал, прочекал) were excluded from the added aliases.

Self-contained Windows x64 and Linux x64 Release builds succeeded. Packaged Linux integration exercised the real speech worker, native model and WAV capture API: synthetic «первый чек» produced `{seat:1, action:check, amount:null}`, then Stop and clean exit. No PokerVision writes were made; outputConnected remains false.

An additional eleven-phrase synthetic-audio run completed in about 1.3 seconds after worker invocation, with no native errors. Acoustic output was imperfect: four exact transcripts, two wrong actions, five incomplete transcripts. This is a smoke test of native execution, not proof of dealer accuracy or Windows latency. The expanded grammar must be tried on the actual dealer microphone. Native Windows, vMix and physical Hollyland input were not available in this environment.

Windows EXE: 50,503,417 bytes, SHA-256 `920112ae7e58647a1965c64f20f07e1bdd8ce8958d0e1ffad96635aeee1385f8`.

The public repository receives only compiled binary delta/package tooling and user documentation; private application source and settings are excluded. Previous release files and stable OKO.exe are retained.
