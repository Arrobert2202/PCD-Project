import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'config.dart';

class OcrBlock {
  final int index;
  final String text;
  final double? confidence;

  OcrBlock({required this.index, required this.text, this.confidence});

  factory OcrBlock.fromJson(Map<String, dynamic> json) => OcrBlock(
        index: json['index'] as int,
        text: json['text'] as String,
        confidence: (json['confidence'] as num?)?.toDouble(),
      );
}

class OcrResponse {
  final String status;
  final String engine;
  final List<OcrBlock> blocks;
  final String fullText;

  OcrResponse({
    required this.status,
    required this.engine,
    required this.blocks,
    required this.fullText,
  });

  factory OcrResponse.fromJson(Map<String, dynamic> json) => OcrResponse(
        status: json['status'] as String,
        engine: json['engine'] as String,
        blocks: (json['blocks'] as List)
            .map((b) => OcrBlock.fromJson(b as Map<String, dynamic>))
            .toList(),
        fullText: json['full_text'] as String,
      );
}

class OcrService {
  Future<OcrResponse> processImage(File imageFile) async {
    final uri = Uri.parse(BackendConfig.ocrEndpoint);
    final request = http.MultipartRequest('POST', uri);

    request.files.add(await http.MultipartFile.fromPath('file', imageFile.path));

    http.StreamedResponse streamedResponse;
    try {
      streamedResponse = await request.send().timeout(
        const Duration(seconds: 15),
        onTimeout: () => throw OcrException('request timed out after 15 seconds'),
      );
    } on OcrException {
      rethrow;
    } catch (e) {
      throw OcrException('network error: $e');
    }

    final body = await streamedResponse.stream.bytesToString();

    if (streamedResponse.statusCode == 200) {
      return OcrResponse.fromJson(jsonDecode(body) as Map<String, dynamic>);
    } else {
      throw OcrException('server error ${streamedResponse.statusCode}: $body');
    }
  }
}

class OcrException implements Exception {
  final String message;
  OcrException(this.message);

  @override
  String toString() => message;
}
