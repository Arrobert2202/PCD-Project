# Supported Languages

Language support per OCR engine and fuzzy correction backend.

| Language | Code | Tesseract | PaddleOCR | EasyOCR | SymSpell | pyspellchecker |
|---|---|:---:|:---:|:---:|:---:|:---:|
| English | `en` | ✓ | ✓ | ✓ | ✓ | ✓ |
| French | `fr` | ✓ | ✓ | ✓ | ✓ | ✓ |
| German | `de` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Spanish | `es` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Portuguese | `pt` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Russian | `ru` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Arabic | `ar` | ✓ | ✓ | ✓ | ✓ | ✓ |
| Italian | `it` | ✓ | ✓ | ✓ | ✓ | → en |
| Chinese (Simplified) | `zh` | ✓ | ✓ | ✓ | ✓ | → en |
| Japanese | `ja` | ✓ | ✓ | ✓ | ✓ | → en |
| Korean | `ko` | ✓ | ✓ | ✓ | ✓ | → en |
| Romanian | `ro` | ✓ | — | ✓ | ✓ | → en |
| Dutch | `nl` | ✓ | — | ✓ | ✓ | → en |
| Polish | `pl` | ✓ | — | ✓ | ✓ | → en |
| Swedish | `sv` | ✓ | — | ✓ | ✓ | → en |
| Turkish | `tr` | ✓ | — | ✓ | ✓ | → en |
| Basque | `eu` | — | — | ✓ | ✓ | ✓ |
| Latvian | `lv` | — | — | ✓ | ✓ | ✓ |

**Legend:**
- ✓ — natively supported
- → en — falls back to English spell correction (OCR still runs in the correct language)
- — — not supported by this engine

## Notes

- **Tesseract** requires a `.traineddata` file per language in `D:\Tesseract-OCR\tessdata\`. All languages above are currently installed.
- **PaddleOCR** has a smaller language set but generally strong accuracy on the languages it supports.
- **EasyOCR** downloads its model files automatically on first use per language, cached in `C:\Users\ninjafail\.EasyOCR\model\`.
- **SymSpell** natively supports all 18 languages in the table via frequency lists downloaded from hermitdave/FrequencyWords, cached in `backend/symspell_dicts/`.
- **pyspellchecker** only natively supports: `en`, `es`, `fr`, `pt`, `de`, `ru`, `ar`, `eu`, `lv`. All other languages fall back to English correction — OCR output is unaffected, only spell correction degrades.
