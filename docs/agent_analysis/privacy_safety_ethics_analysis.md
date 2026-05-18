# Privacy, Safety, and Ethics Analysis

| Risk | Evidence | Impact | Mitigation | Implementation difficulty |
|---|---|---|---|---|
| Sensitive document exposure over network | Backend URL uses plain `http://` (`flutter_app/lib/config.dart`) | Interception risk on local/shared networks | Prefer on-device OCR or HTTPS/TLS in non-local deployments; warn users when using insecure transport | moderate |
| No explicit data retention policy | No backend storage/deletion logic in current code; no policy docs found | Users cannot know whether captured content is retained | Add explicit “no storage by default” policy and enforce delete-after-process behavior | moderate |
| Missing informed consent UX | No consent/privacy notice in `home_screen.dart` | Ethical/legal risk for scanning personal data | Add first-run consent dialog and concise privacy statement | low |
| False reassurance from README claims | README claims OCR pipeline/eval folder not present in current code | Overstated capability in academic reporting | Align documentation to current implementation and separate planned vs implemented features | low |
| OCR error harms for accessibility users | TTS reads text directly; no uncertainty cues (`tts_service.dart`, `home_screen.dart`) | Misread instructions/medical/financial info could cause harm | Add confidence-based warnings and “verify critical text” prompts | moderate |
| No auth on backend endpoint | No authentication middleware in `backend/main.py` | Unauthorized use if backend exposed beyond trusted LAN | Add token/shared-secret for upload endpoints; bind to localhost where possible | moderate |
| Potential logging of sensitive payloads (future risk) | Current backend minimal; no logging policy in repo | Future debugging may leak content | Define safe logging policy: never log raw document text/images | low |
| Accessibility bias risk | No documented testing with visually impaired users | Solution may not meet actual user needs | Add participatory testing protocol and report limitations | moderate |
| Misuse risk (capturing non-consensual documents) | App designed for camera capture; no user warning workflow | Ethical misuse scenario | Add in-app responsible-use notice and project ethics section in paper | low |

## Notes
- Current backend lacks OCR implementation, so some privacy risks are latent but should be addressed before expansion.
- Evidence is from current checkout; verify again after backend OCR implementation lands.
