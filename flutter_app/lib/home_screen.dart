import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:image_picker/image_picker.dart';
import 'package:file_picker/file_picker.dart';
import 'ocr_service.dart';
import 'tts_service.dart';
import 'config.dart';

enum AppState { ready, loading, playing, error }

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with SingleTickerProviderStateMixin {
  final _ocr = OcrService();
  final _tts = TtsService();
  final _picker = ImagePicker();

  AppState _state = AppState.ready;
  String _error = '';
  String _text = '';

  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();

    _pulseController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.08).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );

    _tts.initialize().then((_) {
      if (!_tts.isAvailable) {
        _setError('text-to-speech is not supported on this device');
      }
    });
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _tts.dispose();
    super.dispose();
  }

  Future<void> _captureFromCamera() async {
    XFile? photo;
    try {
      photo = await _picker.pickImage(source: ImageSource.camera);
    } catch (e) {
      _setError('camera unavailable or permission denied');
      return;
    }
    if (photo == null) return;
    await _processFile(File(photo.path));
  }

  Future<void> _pickFromFiles() async {
    FilePickerResult? result;
    try {
      result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['jpg', 'jpeg', 'png', 'pdf'],
      );
    } catch (e) {
      _setError('could not open file picker');
      return;
    }
    if (result == null || result.files.single.path == null) return;
    await _processFile(File(result.files.single.path!));
  }

  Future<void> _processFile(File file) async {
    setState(() => _state = AppState.loading);
    _announce('processing, please wait');

    try {
      final response = await _ocr.processFile(file);
      _text = response.fullText;

      if (_text.isEmpty) {
        _setError('no text was detected');
        return;
      }

      setState(() => _state = AppState.playing);
      _announce('reading text aloud');
      await _tts.speak(_text, onComplete: _onDone);
    } on OcrException catch (e) {
      _setError(e.message);
    } catch (e) {
      _setError('unexpected error: $e');
    }
  }

  void _onDone() {
    if (mounted) {
      setState(() => _state = AppState.ready);
      _announce('done. ready to scan again');
    }
  }

  Future<void> _stop() async {
    await _tts.stop();
    setState(() => _state = AppState.ready);
    _announce('stopped');
  }

  void _setError(String msg) {
    setState(() {
      _state = AppState.error;
      _error = msg;
    });
    _announce('error: $msg');
  }

  void _announce(String msg) {
    SemanticsService.announce(msg, TextDirection.ltr);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF0A0A0A), Color(0xFF1A1A2E), Color(0xFF16213E)],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              _buildAppBar(),
              Expanded(child: _buildBody()),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAppBar() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'ReadDoc',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 0.5,
                ),
              ),
              Text(
                'scan & listen',
                style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 12),
              ),
            ],
          ),
          Semantics(
            label: 'settings',
            button: true,
            child: GestureDetector(
              onTap: _showSettings,
              child: Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(Icons.settings_outlined, color: Colors.white, size: 24),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildBody() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Spacer(),
        _buildStatusCard(),
        const SizedBox(height: 48),
        if (_state == AppState.playing)
          _buildStopButton()
        else
          _buildInputButtons(),
        const Spacer(),
        _buildFooter(),
      ],
    );
  }

  Widget _buildStatusCard() {
    switch (_state) {
      case AppState.loading:
        return _statusCard(
          icon: const SizedBox(
            width: 32, height: 32,
            child: CircularProgressIndicator(color: Colors.white, strokeWidth: 3),
          ),
          text: 'Analysing document...',
          color: const Color(0xFF0F3460),
        );
      case AppState.playing:
        return _statusCard(
          icon: const Icon(Icons.volume_up_rounded, color: Colors.greenAccent, size: 32),
          text: 'Reading aloud...',
          color: const Color(0xFF0D3B2E),
        );
      case AppState.error:
        return _statusCard(
          icon: const Icon(Icons.error_outline_rounded, color: Colors.redAccent, size: 32),
          text: _error,
          color: const Color(0xFF3B0D0D),
        );
      case AppState.ready:
        return _statusCard(
          icon: Icon(Icons.document_scanner_outlined,
              color: Colors.white.withOpacity(0.7), size: 32),
          text: 'Take a photo or upload a file to get started',
          color: Colors.white.withOpacity(0.05),
        );
    }
  }

  Widget _statusCard({required Widget icon, required String text, required Color color}) {
    return Semantics(
      label: text,
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 32),
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.white.withOpacity(0.08)),
        ),
        child: Row(
          children: [
            icon,
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                text,
                style: const TextStyle(color: Colors.white, fontSize: 15, height: 1.4),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInputButtons() {
    final enabled = _state == AppState.ready || _state == AppState.error;
    return AnimatedBuilder(
      animation: _pulseAnimation,
      builder: (context, child) => Transform.scale(
        scale: enabled ? _pulseAnimation.value : 1.0,
        child: child,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _actionButton(
            label: 'Camera',
            semanticLabel: 'take a photo',
            icon: Icons.camera_alt_rounded,
            color: const Color(0xFF4A90E2),
            onTap: enabled ? _captureFromCamera : null,
          ),
          const SizedBox(width: 24),
          _actionButton(
            label: 'Upload',
            semanticLabel: 'upload a file or pdf',
            icon: Icons.upload_file_rounded,
            color: const Color(0xFF5C6BC0),
            onTap: enabled ? _pickFromFiles : null,
          ),
        ],
      ),
    );
  }

  Widget _actionButton({
    required String label,
    required String semanticLabel,
    required IconData icon,
    required Color color,
    required VoidCallback? onTap,
  }) {
    return Semantics(
      label: semanticLabel,
      button: true,
      enabled: onTap != null,
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          width: 130,
          height: 130,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: onTap != null
                  ? [color, color.withOpacity(0.7)]
                  : [Colors.grey.shade800, Colors.grey.shade700],
            ),
            boxShadow: onTap != null
                ? [BoxShadow(color: color.withOpacity(0.4), blurRadius: 24, spreadRadius: 4)]
                : [],
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: Colors.white, size: 44),
              const SizedBox(height: 8),
              Text(label,
                  style: const TextStyle(
                      color: Colors.white, fontSize: 14, fontWeight: FontWeight.w600)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStopButton() {
    return Semantics(
      label: 'stop reading',
      button: true,
      child: GestureDetector(
        onTap: _stop,
        child: Container(
          width: 140,
          height: 140,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: Colors.redAccent.withOpacity(0.15),
            border: Border.all(color: Colors.redAccent, width: 2),
          ),
          child: const Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.stop_rounded, color: Colors.redAccent, size: 52),
              SizedBox(height: 8),
              Text('Stop',
                  style: TextStyle(
                      color: Colors.redAccent, fontSize: 16, fontWeight: FontWeight.w600)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFooter() {
    return Padding(
      padding: const EdgeInsets.only(bottom: 24),
      child: Text(
        'OCR Document Reader',
        style: TextStyle(color: Colors.white.withOpacity(0.2), fontSize: 12),
      ),
    );
  }

  void _showSettings() {
    final hostCtrl = TextEditingController(text: BackendConfig.host);
    final portCtrl = TextEditingController(text: BackendConfig.port.toString());

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1A1A2E),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text('Backend Settings', style: TextStyle(color: Colors.white)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Semantics(
              label: 'ip address input',
              child: TextField(
                controller: hostCtrl,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: 'IP Address',
                  labelStyle: TextStyle(color: Colors.white.withOpacity(0.6)),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide(color: Colors.white.withOpacity(0.2)),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: Color(0xFF4A90E2)),
                  ),
                ),
                keyboardType: TextInputType.number,
              ),
            ),
            const SizedBox(height: 12),
            Semantics(
              label: 'port input',
              child: TextField(
                controller: portCtrl,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: 'Port',
                  labelStyle: TextStyle(color: Colors.white.withOpacity(0.6)),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: BorderSide(color: Colors.white.withOpacity(0.2)),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide: const BorderSide(color: Color(0xFF4A90E2)),
                  ),
                ),
                keyboardType: TextInputType.number,
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: Text('Cancel', style: TextStyle(color: Colors.white.withOpacity(0.6))),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF4A90E2),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            onPressed: () {
              BackendConfig.host = hostCtrl.text.trim();
              BackendConfig.port = int.tryParse(portCtrl.text.trim()) ?? 8000;
              Navigator.pop(ctx);
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }
}
