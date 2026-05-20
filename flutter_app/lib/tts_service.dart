import 'package:flutter/foundation.dart';
import 'package:flutter_tts/flutter_tts.dart';

class TtsService {
  final FlutterTts _tts = FlutterTts();
  bool _isAvailable = false;

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

  Future<void> speak(String text, {VoidCallback? onComplete}) async {
    if (!_isAvailable) return;
    _tts.setCompletionHandler(() => onComplete?.call());
    await _tts.speak(text);
  }

  Future<void> stop() async {
    await _tts.stop();
  }

  Future<void> dispose() async {
    await _tts.stop();
  }
}
