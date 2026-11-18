# OKO 1.8.2 preview — contextual dealer speech

Date: 2026-11-18. Adds a separate «Слежение за столом» toggle to the voice workspace. It is disabled by default and never persisted as enabled across restarts.

## Behavior

The initial expected player comes from PokerVision's current acting player. If it is seat 2, a bare «чек» becomes `{seat:2, action:check}`. Subsequent bare actions advance through active seats with wraparound. Explicit seat phrases re-anchor the cursor. Initial absent/left/folded/zero-stack players and locally spoken folds/all-ins are skipped.

The user's sequence «первый бокс чек, второй поднял на сто, третий сбросил, чек» resolves to seats 1, 2, 3, 4 with canonical actions check, raise-by 100, fold, check. До/на and positive integral amounts remain strict. Mixed explicit/implicit fragments are parsed atomically, with the existing ten-command/1024-character bounds.

This is a speech cursor, not an independent poker engine. Streets and hands come from PokerVision; chip balances are not calculated locally. Membership and initial actor are frozen for each street, then advanced by speech, because platform acting/fold/all-in updates can precede recognition of the very action they acknowledge. Same-street platform updates must not advance or rewind the voice cursor. An explicit seat or toggling tracking re-synchronizes it. If the initial actor is absent, the tracker waits for it until a speech anchor or error. New hand/street/play-status changes invalidate old audio and reinitialize context; local folds/all-ins persist only for their hand.

Malformed/empty/error audio suspends implicit assignment until an explicit seat. Server overflow invalidates queued anchors as well. An unconfirmed upload or browser queue overflow stops capture and tracking instead of letting missing actions shift all subsequent seats. Stop, disconnect, recognizer failure and restart disable tracking; navigation retains it. Toggling is protected by the existing local token/origin checks and an epoch lease.

## Verification

- **298/298 application tests passed.** New integration cases first failed against the missing route/grammar. Additional failing regressions reproduced platform updates racing ahead of ASR, delayed initial actor, lost recognizer, blank audio, queue overflow and pause without street change; all passed after fixes. Existing camera/director/hotkey/recorder tests remained green.
- Browser fixture: keyboard toggle, current actor2 seed, mixed commands/assigned seats, strict fallback when disabled, navigation persistence, re-enable resync, street reset, disconnect, no JS errors, widths 1440/768/320. Desktop/mobile screenshots inspected.
- Native Vosk 0.3.45 / small-ru-0.22: actual bare «чек» WAVs passed through the isolated worker and live speech API, consecutively producing seat2 check and seat3 check. Expected next seat advanced to4; platform acting/stack values remained unchanged. Stop disabled tracking.
- Real browser microphone/worklet/WAV/native Vosk path and navigation regression passed. A deliberately aborted audio request first reproduced failure to stop, then confirmed that mic/tracking stop with a visible recovery error.
- Standalone Windows x64 and Linux x64 Release builds completed. Windows/vMix/Hollyland and real dealer acoustic accuracy were not exercised in this Linux environment. Synthetic bare-check recognition is a limited smoke test, not an accuracy guarantee.

PokerVision outputConnected remains false. No camera arming/switching or PokerVision writes were added; no production test/transcript injection route exists. The public repository receives compiled binaries/package tooling and user docs only. Previous binaries and stable OKO.exe remain intact.

Windows EXE: 50,508,640 bytes, SHA-256 `0a43174599ba933c6e426a96a69368cce5354ec16244f2dd5bf320ce19a67dba`.
