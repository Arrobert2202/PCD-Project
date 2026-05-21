import 'package:flutter/foundation.dart';
import 'package:flutter_tts/flutter_tts.dart';

class TtsService {
  final FlutterTts _tts = FlutterTts();
  bool _isAvailable = false;
  String _currentLocale = 'en-US';
  int _generation = 0;

  // Maps OCR language codes returned by the backend to BCP 47 TTS locales.
  static const _localeMap = {
    'en':  'en-US',
    'ro':  'ro-RO',
    'fr':  'fr-FR',
    'de':  'de-DE',
    'es':  'es-ES',
    'pt':  'pt-PT',
    'it':  'it-IT',
    'nl':  'nl-NL',
    'pl':  'pl-PL',
    'ru':  'ru-RU',
    'ar':  'ar-SA',
    'zh':  'zh-CN',
    'ja':  'ja-JP',
    'ko':  'ko-KR',
    'sv':  'sv-SE',
    'tr':  'tr-TR',
    'lv':  'lv-LV',
  };

  Future<void> initialize() async {
    _isAvailable = await _tts.isLanguageAvailable('en-US') ?? false;
    if (_isAvailable) {
      await _tts.setLanguage('en-US');
      await _tts.setSpeechRate(0.5);
      await _tts.setVolume(1.0);
      await _tts.setPitch(1.0);
    }
  }

  bool get isAvailable => _isAvailable;

  Future<void> speak(String text, {String? language, VoidCallback? onComplete}) async {
    if (!_isAvailable || text.trim().isEmpty) return;
    final gen = ++_generation;
    final locale = TtsService.localeFor(language);
    if (locale != _currentLocale) {
      final available = await _tts.isLanguageAvailable(locale) ?? false;
      if (gen != _generation) return;
      final target = available ? locale : 'en-US';
      await _tts.setLanguage(target);
      if (gen != _generation) return;
      _currentLocale = target;
    }
    if (gen != _generation) return;
    _tts.setCompletionHandler(() => onComplete?.call());
    await _tts.speak(text);
  }

  Future<void> stop() async {
    ++_generation; // invalidate any in-flight speak
    await _tts.stop();
  }

  Future<void> dispose() async {
    await _tts.stop();
  }

  static String localeFor(String? langCode) {
    if (langCode == null) return 'en-US';
    // Handle codes that already look like BCP 47 (e.g. "en-US", "zh-CN").
    if (langCode.contains('-')) return langCode;
    return _localeMap[langCode.toLowerCase()] ?? 'en-US';
  }
}
