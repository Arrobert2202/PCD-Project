# Accessibility Analysis

## Implemented accessibility features
- **Speech output:** OCR result is read via `FlutterTts` (`flutter_app/lib/tts_service.dart`).
- **State announcements:** `SemanticsService.announce` is used for processing, done, stop, and error events (`home_screen.dart::_announce`).
- **Semantic labels:** Key controls are wrapped in `Semantics` (scan, stop, settings, status, inputs) in `home_screen.dart`.
- **Simple interaction model:** Single primary action reduces UI complexity.

## Missing accessibility features
- No navigable reading units (by block/line/section/page).
- No visible transcript panel for low-vision users needing both visual and audio support.
- No explicit confidence/uncertainty communication for OCR errors.
- No customizable TTS options (voice, language, speech rate UI).
- No accessibility onboarding/help flow for first-time visually impaired users.
- No explicit keyboard/focus management for non-touch navigation scenarios.

## Risks
- Monolithic readout can overwhelm users on long documents.
- OCR mistakes are spoken without confidence context, risking misinformation.
- Lack of structured navigation reduces practical usability for document understanding tasks.
- Missing backend OCR currently prevents validating accessibility claims end to end.

## Concrete improvements for a 3-week project
1. **Add block navigation controls** (next/previous/repeat block) once backend returns structured blocks.
2. **Expose transcript + active highlight** to pair audio with visual context.
3. **Announce confidence warnings** (e.g., low-confidence block alerts).
4. **Add quick accessibility settings** (speech rate, pause/resume, repeat sentence).
5. **Create usability protocol** with visually impaired users (or representative accessibility testing if recruitment is constrained).
6. **Add robust error guidance** (network unavailable, OCR empty, camera denied) with recovery instructions.
