# Accessibility Analysis

## Implemented accessibility features

- TTS output for full text and per-block text (`flutter_app/lib/ocr_result_screen.dart`, `flutter_app/lib/tts_service.dart`)
- Semantics labels on many actionable controls (buttons/toggles/language items) in `home_screen.dart` and `ocr_result_screen.dart`
- Status/error announcements via `SemanticsService.announce` (`home_screen.dart::_announce`)
- Large tap targets for camera/upload actions and overlay block taps
- Visual focus state for selected text block in result list

## Missing accessibility features

- No explicit keyboard shortcut map or focus-order management for non-touch interaction
- TTS language appears fixed to `en-US` availability path; no dynamic voice-language match to detected OCR language
- No explicit confidence/uncertainty verbalization before reading content
- No accessibility settings profile (speech speed presets, high contrast toggle beyond current dark theme)
- No user-facing fallback when TTS unavailable beyond silent no-op behavior

## Risks

- Users may trust OCR output without uncertainty cues (danger for critical documents).
- Non-English OCR text may be spoken with incorrect TTS voice/language.
- UI claims PDF upload but likely fails server-side, creating confusing flow for assistive users.
- Lack of formal usability testing evidence with visually impaired participants.

## Concrete improvements for a 3-week project

1. Add robust non-visual navigation mode:
   - next/previous block controls, read-current, read-page summary, repeat-last.
2. Add uncertainty communication:
   - announce low-confidence blocks and offer “review visually/retake image”.
3. Add multilingual TTS fallback strategy:
   - map OCR language to TTS locale with graceful fallback message.
4. Add input-validation feedback before upload:
   - explicitly state supported formats and PDF limitation (or implement conversion).
5. Add accessibility test protocol:
   - task-based tests (capture, understand, navigate, recover from error).
