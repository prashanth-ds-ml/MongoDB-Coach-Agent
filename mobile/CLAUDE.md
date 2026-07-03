# Claude Project Instructions (mobile/)

Follow `mobile/AGENTS.md` for work in this directory.

`mobile/` is a standalone Expo/React Native flashcard app. It bundles `assets/flashcards.json` locally and keeps progress in `AsyncStorage` — it does not call the `certcoach` CLI's MongoDB backend. Root-level `memory/` context (Phase 4 question-bank state, lesson pipeline, etc.) does not apply here.
