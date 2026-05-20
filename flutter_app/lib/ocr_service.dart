import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'config.dart';

class OcrOptions {
  final String engine;
  final String lang;
  final bool fuzzy;
  final String fuzzer;

  const OcrOptions({
    this.engine = 'easyocr',
    this.lang = 'auto',
    this.fuzzy = false,
    this.fuzzer = 'symspell',
  });

  Map<String, dynamic> toJson() => {
        'engine': engine,
        'lang': lang,
        'fuzzy': fuzzy,
        'fuzzer': fuzzer,
      };
}

class BoundingBox {
  final int x;
  final int y;
  final int width;
  final int height;

  const BoundingBox({
    required this.x,
    required this.y,
    required this.width,
    required this.height,
  });

  factory BoundingBox.fromJson(Map<String, dynamic> json) => BoundingBox(
        x: json['x'] as int,
        y: json['y'] as int,
        width: json['width'] as int,
        height: json['height'] as int,
      );
}

class OcrBlock {
  final int index;
  final String text;
  final double? confidence;
  final BoundingBox? bbox;

  OcrBlock({
    required this.index,
    required this.text,
    this.confidence,
    this.bbox,
  });

  factory OcrBlock.fromJson(Map<String, dynamic> json) => OcrBlock(
        index: json['index'] as int,
        text: json['text'] as String,
        confidence: (json['confidence'] as num?)?.toDouble(),
        bbox: json['bbox'] != null
            ? BoundingBox.fromJson(json['bbox'] as Map<String, dynamic>)
            : null,
      );
}

class OcrResponse {
  final String status;
  final String engine;
  final String? language;
  final List<OcrBlock> blocks;
  final String fullText;

  OcrResponse({
    required this.status,
    required this.engine,
    this.language,
    required this.blocks,
    required this.fullText,
  });

  factory OcrResponse.fromJson(Map<String, dynamic> json) => OcrResponse(
        status: json['status'] as String,
        engine: json['engine'] as String,
        language: json['language'] as String?,
        blocks: (json['blocks'] as List)
            .map((b) => OcrBlock.fromJson(b as Map<String, dynamic>))
            .toList(),
        fullText: json['full_text'] as String,
      );
}

class OcrService {
  Future<OcrResponse> processFile(File file, OcrOptions options) async {
    return processBytes(await file.readAsBytes(), options);
  }

  Future<OcrResponse> processBytes(
      Uint8List imageBytes, OcrOptions options) async {
    final uri = Uri.parse(BackendConfig.ocrEndpoint);
    final body = jsonEncode({
      'image': base64Encode(imageBytes),
      ...options.toJson(),
    });

    http.Response response;
    try {
      response = await http
          .post(
            uri,
            headers: {'Content-Type': 'application/json'},
            body: body,
          )
          .timeout(
            const Duration(seconds: 30),
            onTimeout: () => throw OcrException('request timed out'),
          );
    } on OcrException {
      rethrow;
    } catch (e) {
      throw OcrException('network error: $e');
    }

    if (response.statusCode == 200) {
      return OcrResponse.fromJson(
          jsonDecode(response.body) as Map<String, dynamic>);
    } else {
      throw OcrException(
          'server error ${response.statusCode}: ${response.body}');
    }
  }
}

class OcrException implements Exception {
  final String message;
  OcrException(this.message);

  @override
  String toString() => message;
}
