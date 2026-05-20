import 'dart:math' as math;
import 'dart:typed_data';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'ocr_service.dart';
import 'tts_service.dart';

class OcrResultScreen extends StatefulWidget {
  final Uint8List imageBytes;
  final OcrResponse response;

  const OcrResultScreen({
    super.key,
    required this.imageBytes,
    required this.response,
  });

  @override
  State<OcrResultScreen> createState() => _OcrResultScreenState();
}

class _OcrResultScreenState extends State<OcrResultScreen> {
  final _tts = TtsService();
  final _listController = ScrollController();

  bool _isPlaying = false;
  int? _selectedIndex;
  bool _showBoxes = true;
  bool _showLabels = true;
  late Future<ui.Size> _imageSizeFuture;

  // item height used for approximate scroll-to-selected
  static const double _itemHeight = 64.0;

  @override
  void initState() {
    super.initState();
    _imageSizeFuture = _decodeImageSize(widget.imageBytes);
    _tts.initialize();
  }

  @override
  void dispose() {
    _tts.dispose();
    _listController.dispose();
    super.dispose();
  }

  Future<ui.Size> _decodeImageSize(Uint8List bytes) async {
    final codec = await ui.instantiateImageCodec(bytes);
    final frame = await codec.getNextFrame();
    final img = frame.image;
    return ui.Size(img.width.toDouble(), img.height.toDouble());
  }

  Future<void> _toggleReadAll() async {
    if (_isPlaying) {
      await _tts.stop();
      setState(() => _isPlaying = false);
      return;
    }
    setState(() {
      _isPlaying = true;
      _selectedIndex = null;
    });
    await _tts.speak(
      widget.response.fullText,
      onComplete: () {
        if (mounted) setState(() => _isPlaying = false);
      },
    );
  }

  Future<void> _readBlock(int blockIndex) async {
    final block = widget.response.blocks[blockIndex];
    setState(() {
      _selectedIndex = blockIndex;
      _isPlaying = false;
    });
    await _tts.stop();
    await _tts.speak(block.text, onComplete: () {});
    _scrollListTo(blockIndex);
  }

  void _scrollListTo(int index) {
    if (!_listController.hasClients) return;
    final target = (index * _itemHeight)
        .clamp(0.0, _listController.position.maxScrollExtent);
    _listController.animateTo(
      target,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeOut,
    );
  }

  @override
  Widget build(BuildContext context) {
    final engine = widget.response.engine;
    final lang = widget.response.language ?? 'unknown';

    return Scaffold(
      backgroundColor: const Color(0xFF0A0A0A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1A1A2E),
        foregroundColor: Colors.white,
        elevation: 0,
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Detected Text',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            Text(
              '$engine  •  $lang',
              style: TextStyle(
                  fontSize: 11, color: Colors.white.withOpacity(0.45)),
            ),
          ],
        ),
        actions: [
          Semantics(
            label: _showLabels ? 'hide text labels' : 'show text labels',
            button: true,
            child: IconButton(
              icon: Icon(
                _showLabels ? Icons.label_rounded : Icons.label_off_rounded,
                color: _showLabels ? Colors.white : Colors.white38,
              ),
              tooltip: _showLabels ? 'Hide labels' : 'Show labels',
              onPressed: () => setState(() => _showLabels = !_showLabels),
            ),
          ),
          Semantics(
            label: _showBoxes ? 'hide bounding boxes' : 'show bounding boxes',
            button: true,
            child: IconButton(
              icon: Icon(
                _showBoxes ? Icons.layers_rounded : Icons.layers_clear_rounded,
                color: _showBoxes ? Colors.white : Colors.white38,
              ),
              tooltip: _showBoxes ? 'Hide boxes' : 'Show boxes',
              onPressed: () => setState(() {
                _showBoxes = !_showBoxes;
                if (!_showBoxes) _showLabels = false;
              }),
            ),
          ),
          Semantics(
            label: _isPlaying ? 'stop reading' : 'read all aloud',
            button: true,
            child: IconButton(
              icon: Icon(
                _isPlaying ? Icons.stop_rounded : Icons.volume_up_rounded,
                color: _isPlaying ? Colors.redAccent : Colors.white,
              ),
              tooltip: _isPlaying ? 'Stop' : 'Read all',
              onPressed: _toggleReadAll,
            ),
          ),
        ],
      ),
      body: FutureBuilder<ui.Size>(
        future: _imageSizeFuture,
        builder: (context, snap) {
          if (!snap.hasData) {
            return const Center(
              child: CircularProgressIndicator(
                  color: Color(0xFF4A90E2), strokeWidth: 2),
            );
          }
          return _buildContent(snap.data!);
        },
      ),
    );
  }

  Widget _buildContent(ui.Size imageSize) {
    return Column(
      children: [
        Expanded(
          flex: 55,
          child: _buildImageOverlay(imageSize),
        ),
        Container(height: 1, color: Colors.white.withOpacity(0.07)),
        Expanded(
          flex: 45,
          child: _buildBlockList(),
        ),
      ],
    );
  }

  Widget _buildImageOverlay(ui.Size imageSize) {
    final blocksWithBbox =
        widget.response.blocks.where((b) => b.bbox != null).toList();

    return ColoredBox(
      color: Colors.black,
      child: InteractiveViewer(
        minScale: 1.0,
        maxScale: 6.0,
        child: Stack(
          fit: StackFit.expand,
          children: [
            Image.memory(widget.imageBytes, fit: BoxFit.contain),
            if (_showBoxes)
              CustomPaint(
                painter: _OverlayPainter(
                  blocks: blocksWithBbox,
                  imageSize: imageSize,
                  selectedIndex: _selectedIndex,
                  showLabels: _showLabels,
                ),
              ),
            // Transparent tap targets aligned to each bbox
            LayoutBuilder(builder: (context, constraints) {
            final widgetSize =
                Size(constraints.maxWidth, constraints.maxHeight);
            final scale = math.min(
              widgetSize.width / imageSize.width,
              widgetSize.height / imageSize.height,
            );
            final offsetX =
                (widgetSize.width - imageSize.width * scale) / 2;
            final offsetY =
                (widgetSize.height - imageSize.height * scale) / 2;

            return Stack(
              children: [
                for (final block in blocksWithBbox)
                  Positioned(
                    left: block.bbox!.x * scale + offsetX,
                    top: block.bbox!.y * scale + offsetY,
                    width: block.bbox!.width * scale,
                    height: block.bbox!.height * scale,
                    child: GestureDetector(
                      behavior: HitTestBehavior.opaque,
                      onTap: () => _readBlock(block.index),
                      child: const SizedBox.expand(),
                    ),
                  ),
              ],
            );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildBlockList() {
    final blocks = widget.response.blocks;
    if (blocks.isEmpty) {
      return Center(
        child: Text(
          'No text blocks',
          style: TextStyle(color: Colors.white.withOpacity(0.35), fontSize: 13),
        ),
      );
    }

    return Container(
      color: const Color(0xFF111827),
      child: ListView.separated(
        controller: _listController,
        padding: const EdgeInsets.symmetric(vertical: 4),
        itemCount: blocks.length,
        separatorBuilder: (_, __) => Divider(
          color: Colors.white.withOpacity(0.05),
          height: 1,
          indent: 52,
        ),
        itemBuilder: (context, i) {
          final block = blocks[i];
          final isSelected = _selectedIndex == block.index;
          return _buildBlockItem(block, i, isSelected);
        },
      ),
    );
  }

  Widget _buildBlockItem(OcrBlock block, int listIndex, bool isSelected) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: () => _readBlock(block.index),
        splashColor: const Color(0xFF4A90E2).withOpacity(0.1),
        highlightColor: const Color(0xFF4A90E2).withOpacity(0.06),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          height: _itemHeight,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          decoration: BoxDecoration(
            border: isSelected
                ? const Border(
                    left: BorderSide(color: Color(0xFF4A90E2), width: 3))
                : const Border(
                    left: BorderSide(color: Colors.transparent, width: 3)),
            color: isSelected
                ? const Color(0xFF4A90E2).withOpacity(0.08)
                : Colors.transparent,
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              _blockBadge(listIndex + 1, isSelected),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      block.text,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        color: isSelected
                            ? Colors.white
                            : Colors.white.withOpacity(0.85),
                        fontSize: 13,
                        height: 1.3,
                      ),
                    ),
                    if (block.confidence != null) ...[
                      const SizedBox(height: 2),
                      _confidenceBar(block.confidence!),
                    ],
                  ],
                ),
              ),
              const SizedBox(width: 8),
              Icon(
                Icons.play_circle_outline_rounded,
                size: 18,
                color: isSelected
                    ? const Color(0xFF4A90E2)
                    : Colors.white.withOpacity(0.18),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _blockBadge(int number, bool isSelected) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      width: 24,
      height: 24,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: isSelected
            ? const Color(0xFF4A90E2)
            : Colors.white.withOpacity(0.1),
      ),
      child: Text(
        '$number',
        style: TextStyle(
          color: isSelected ? Colors.white : Colors.white54,
          fontSize: 10,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }

  Widget _confidenceBar(double confidence) {
    // EasyOCR returns 0–1, Tesseract returns 0–100
    final pct = confidence > 1.0 ? confidence / 100.0 : confidence;
    final color = pct >= 0.8
        ? Colors.greenAccent
        : pct >= 0.5
            ? Colors.orangeAccent
            : Colors.redAccent;

    return Row(
      children: [
        SizedBox(
          width: 48,
          height: 3,
          child: ClipRRect(
            borderRadius: BorderRadius.circular(2),
            child: LinearProgressIndicator(
              value: pct.clamp(0.0, 1.0),
              backgroundColor: Colors.white.withOpacity(0.08),
              valueColor: AlwaysStoppedAnimation(color.withOpacity(0.7)),
            ),
          ),
        ),
        const SizedBox(width: 5),
        Text(
          '${(pct * 100).toStringAsFixed(0)}%',
          style: TextStyle(
            color: Colors.white.withOpacity(0.3),
            fontSize: 9,
          ),
        ),
      ],
    );
  }
}

class _OverlayPainter extends CustomPainter {
  final List<OcrBlock> blocks;
  final ui.Size imageSize;
  final int? selectedIndex;
  final bool showLabels;

  static const _accent = Color(0xFFFFD600);

  const _OverlayPainter({
    required this.blocks,
    required this.imageSize,
    required this.selectedIndex,
    required this.showLabels,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final scale = math.min(
      size.width / imageSize.width,
      size.height / imageSize.height,
    );
    final offsetX = (size.width - imageSize.width * scale) / 2;
    final offsetY = (size.height - imageSize.height * scale) / 2;

    final borderPaint = Paint()..style = PaintingStyle.stroke..strokeWidth = 1.5;
    final fillPaint = Paint()..style = PaintingStyle.fill;

    for (final block in blocks) {
      final b = block.bbox!;
      final rect = Rect.fromLTWH(
        b.x * scale + offsetX,
        b.y * scale + offsetY,
        b.width * scale,
        b.height * scale,
      );

      final isSelected = selectedIndex == block.index;

      borderPaint.color =
          isSelected ? _accent : _accent.withOpacity(0.65);
      fillPaint.color =
          isSelected ? _accent.withOpacity(0.22) : _accent.withOpacity(0.1);

      canvas.drawRect(rect, fillPaint);
      canvas.drawRect(rect, borderPaint);

      if (showLabels) _drawLabel(canvas, block.text, rect, isSelected);
    }
  }

  void _drawLabel(
      Canvas canvas, String text, Rect boxRect, bool isSelected) {
    if (boxRect.width < 16) return;

    final fontSize = math.max(8.5, math.min(11.5, boxRect.width * 0.15));
    final truncated =
        text.length > 50 ? '${text.substring(0, 48)}…' : text;

    final tp = TextPainter(
      text: TextSpan(
        text: truncated,
        style: TextStyle(
          color: Colors.white,
          fontSize: fontSize,
          fontWeight: FontWeight.w500,
          height: 1.2,
        ),
      ),
      textDirection: TextDirection.ltr,
      maxLines: 1,
    )..layout(maxWidth: math.min(240, boxRect.width + 60));

    const hPad = 5.0;
    const vPad = 3.0;
    final labelW = tp.width + hPad * 2;
    final labelH = tp.height + vPad * 2;

    // prefer above the box; if that clips the canvas top, go inside
    double labelTop = boxRect.top - labelH - 2;
    if (labelTop < 0) labelTop = boxRect.top + 2;

    final labelLeft = boxRect.left.clamp(0.0, double.infinity);

    final labelRect = Rect.fromLTWH(labelLeft, labelTop, labelW, labelH);

    final bgPaint = Paint()
      ..color = (isSelected ? _accent : _accent.withOpacity(0.75))
      ..style = PaintingStyle.fill;

    canvas.drawRRect(
      RRect.fromRectAndRadius(labelRect, const Radius.circular(3)),
      bgPaint,
    );

    tp.paint(
        canvas, Offset(labelRect.left + hPad, labelRect.top + vPad));
  }

  @override
  bool shouldRepaint(_OverlayPainter old) =>
      old.selectedIndex != selectedIndex ||
      old.blocks != blocks ||
      old.showLabels != showLabels;
}
