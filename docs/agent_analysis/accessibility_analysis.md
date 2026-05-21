# Accessibility Analysis

## Implemented accessibility features
- **Text-to-speech output** for full OCR text and per-block reading (`flutter_app/lib/tts_service.dart`, `flutter_app/lib/ocr_result_screen.dart`)
- **Block-level interaction** by tapping overlay regions and list entries (`ocr_result_screen.dart::_readBlock`)
- **Semantic labels and button semantics** across major controls (`Semantics(...)` in `home_screen.dart` and `ocr_result_screen.dart`)
- **Live announcements** for processing/error states (`home_screen.dart::_announce`)
- **Readable high-contrast dark theme styling** (inferred from color choices in `main.dart`, `home_screen.dart`)

## Missing accessibility features
- **No explicit screen-reader navigation model** (next/previous block commands, section landmarks, document outline)
- **No confidence/uncertainty narration** despite confidence values available in blocks
- **No language-aware TTS voice switching**; TTS initialized as `en-US` only (`tts_service.dart`)
- **No explicit keyboard-only workflow documentation/tests**
- **No accessibility-focused automated tests**
- **No user-adjustable speech presets** (rate/pitch presets, pause controls, rewind by sentence)

## Risks
- Users may hear incorrect pronunciation for non-English OCR results due to fixed `en-US` TTS.
- Tap-only block navigation may be difficult for some visually impaired users without linear command navigation.
- OCR errors are not consistently surfaced as uncertainty cues, risking over-trust.
- PDF option in picker can fail unexpectedly, harming usability confidence.

## Concrete improvements for a 3-week project
1. Add **linear navigation controls** (next/previous block, repeat current block, jump to top/bottom).
2. Add **confidence-aware prompts** (e.g., “low confidence block” before speaking).
3. Add **auto TTS language switch/fallback** using backend `language` response.
4. Add **error explanation UX** for unsupported formats (especially PDF path).
5. Add **accessibility acceptance checklist** and manual test script (TalkBack/VoiceOver scenarios).
6. Add **shortcut gestures/buttons** for “Read all”, “Stop”, and “Re-read selected block”.
