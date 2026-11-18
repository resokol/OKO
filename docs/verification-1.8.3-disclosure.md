# OKO 1.8.3 preview — all-in/heads-up disclosure

Date: 2026-11-18. UI-only change requested from the scenario workspace screenshot.

The all-in/two-player settings now occupy their own default-closed disclosure, «Олл-ин или дуэль», alongside emotions, long-turn and pre-hand settings. It uses the existing setting-disclosure component and styling. Pre-hand direction moved into the existing «Проход по игрокам» disclosure. The custom scenario editor retains its rules and camera-order fields. Existing control IDs, values, disabled-state rules and save logic were retained; no director, speech or platform integration code changed.

Browser verification against an isolated HostUi passed: four sibling disclosures; default collapsed runout fields; keyboard opening; enabling/editing shot duration, split, river input and Merge; pre-hand direction; collapsing before saving and exact saved values (3500ms, cameras1/2, Merge750ms, clockwise). The existing six-workspace verification also passed: persistent drafts, camera edits, global Stop/manual, hidden settings save, masked overlay credentials, unique IDs, offline state and widths320/768/1440 with no JS errors. Desktop/mobile collapsed/expanded captures were inspected. No new unit tests were added for this markup rearrangement.

Windows x64 Release binary built for publication; native Windows/vMix were not run in this Linux environment. Distribution stays binary-only; existing releases and stable OKO.exe remain intact. The existing speech model and settings remain compatible.

Windows EXE: 50,508,666 bytes; SHA-256 `384308df21e2e5fbe07e465a9948d1ce3db9a9cb0192f48b7a4a3f15c0e3bdd9`.
