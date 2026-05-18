import re
from pathlib import Path
from typing import Optional

import requests as _requests

PYSPELL_LANGS  = {"en", "es", "fr", "pt", "de", "ru", "ar", "eu", "lv"}
SYMSPELL_LANGS = PYSPELL_LANGS | {"it", "ro", "nl", "pl", "sv", "tr", "zh", "ja", "ko"}

_spell_checkers: dict = {}
_symspell_checkers: dict = {}

_DICT_DIR = Path(__file__).parent / "symspell_dicts"
_FREQWORDS_URLS = [
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/{lang}/{lang}_50k.txt",
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2016/{lang}/{lang}_50k.txt",
]


def _download_dict(lang: str) -> Optional[Path]:
    _DICT_DIR.mkdir(exist_ok=True)
    path = _DICT_DIR / f"{lang}_50k.txt"
    if path.exists():
        return path
    for template in _FREQWORDS_URLS:
        try:
            resp = _requests.get(template.format(lang=lang), timeout=15)
            if resp.status_code == 200:
                path.write_bytes(resp.content)
                return path
        except Exception:
            continue
    return None


def _get_symspell(lang: str):
    if lang not in _symspell_checkers:
        from symspellpy import SymSpell
        sym = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        dict_path = _download_dict(lang) or _download_dict("en")
        if dict_path:
            sym.load_dictionary(str(dict_path), term_index=0, count_index=1, separator=" ", encoding="utf-8")
        _symspell_checkers[lang] = sym
    return _symspell_checkers[lang]


def _get_pyspell(lang: str):
    if lang not in _spell_checkers:
        from spellchecker import SpellChecker
        _spell_checkers[lang] = SpellChecker(language=lang)
    return _spell_checkers[lang]


def apply_fuzzy_matching(text: str, lang: Optional[str], fuzzer: str = "symspell") -> str:
    corrected_lines = []
    if fuzzer == "symspell":
        effective_lang = lang if lang in SYMSPELL_LANGS else "en"
        sym = _get_symspell(effective_lang)
        for line in text.splitlines():
            corrected_lines.append(_correct_symspell(sym, line))
    else:
        effective_lang = lang if lang in PYSPELL_LANGS else "en"
        spell = _get_pyspell(effective_lang)
        for line in text.splitlines():
            corrected_lines.append(_correct_pyspell(spell, line))
    return "\n".join(corrected_lines)


def _correct_symspell(sym, line: str) -> str:
    from symspellpy import Verbosity
    tokens = re.findall(r"[A-Za-z']+|[^A-Za-z']+", line)
    result = []
    for token in tokens:
        if re.fullmatch(r"[A-Za-z']+", token):
            suggestions = sym.lookup(token, Verbosity.CLOSEST, max_edit_distance=2)
            result.append(suggestions[0].term if suggestions else token)
        else:
            result.append(token)
    return "".join(result)


def _correct_pyspell(spell, line: str) -> str:
    tokens = re.findall(r"[A-Za-z']+|[^A-Za-z']+", line)
    result = []
    for token in tokens:
        if re.fullmatch(r"[A-Za-z']+", token):
            correction = spell.correction(token)
            result.append(correction if correction else token)
        else:
            result.append(token)
    return "".join(result)
