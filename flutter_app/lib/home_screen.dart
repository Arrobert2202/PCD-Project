import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter/semantics.dart';
import 'package:image_picker/image_picker.dart';
import 'package:file_picker/file_picker.dart';
import 'ocr_service.dart';
import 'ocr_result_screen.dart';
import 'config.dart';

enum AppState { ready, loading, error }

class _LangOption {
  final String code;
  final String name;
  final String flag;
  const _LangOption(this.code, this.name, this.flag);
}

const _kLanguages = [
  _LangOption('auto', 'Auto-detect',          '🌐'),
  _LangOption('en',   'English',              '🇬🇧'),
  _LangOption('ro',   'Romanian',             '🇷🇴'),
  _LangOption('fr',   'French',               '🇫🇷'),
  _LangOption('de',   'German',               '🇩🇪'),
  _LangOption('es',   'Spanish',              '🇪🇸'),
  _LangOption('pt',   'Portuguese',           '🇵🇹'),
  _LangOption('it',   'Italian',              '🇮🇹'),
  _LangOption('nl',   'Dutch',                '🇳🇱'),
  _LangOption('pl',   'Polish',               '🇵🇱'),
  _LangOption('ru',   'Russian',              '🇷🇺'),
  _LangOption('ar',   'Arabic',               '🇸🇦'),
  _LangOption('zh',   'Chinese (Simplified)', '🇨🇳'),
  _LangOption('ja',   'Japanese',             '🇯🇵'),
  _LangOption('ko',   'Korean',               '🇰🇷'),
  _LangOption('sv',   'Swedish',              '🇸🇪'),
  _LangOption('tr',   'Turkish',              '🇹🇷'),
  _LangOption('eu',   'Basque',               '🏴'),
  _LangOption('lv',   'Latvian',              '🇱🇻'),
];

class _LanguageMenu extends StatelessWidget {
  final String selected;
  final ScrollController scrollController;
  final void Function(String) onSelected;

  const _LanguageMenu({
    required this.selected,
    required this.scrollController,
    required this.onSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Color(0xFF1A1A2E),
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        children: [
          // drag handle
          Padding(
            padding: const EdgeInsets.only(top: 10, bottom: 4),
            child: Container(
              width: 36,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.25),
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          // title
          Padding(
            padding:
                const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            child: Row(
              children: [
                const Text(
                  'Select Language',
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                      fontWeight: FontWeight.w600),
                ),
                const Spacer(),
                Text(
                  '${_kLanguages.length} languages',
                  style: TextStyle(
                      color: Colors.white.withOpacity(0.35), fontSize: 12),
                ),
              ],
            ),
          ),
          Divider(color: Colors.white.withOpacity(0.07), height: 1),
          // list
          Expanded(
            child: ListView.builder(
              controller: scrollController,
              itemCount: _kLanguages.length,
              itemBuilder: (_, i) {
                final lang = _kLanguages[i];
                final isSelected = lang.code == selected;
                return _LanguageTile(
                  lang: lang,
                  isSelected: isSelected,
                  onTap: () => onSelected(lang.code),
                );
              },
            ),
          ),
          SizedBox(height: MediaQuery.of(context).padding.bottom + 8),
        ],
      ),
    );
  }
}

class _LanguageTile extends StatelessWidget {
  final _LangOption lang;
  final bool isSelected;
  final VoidCallback onTap;

  const _LanguageTile({
    required this.lang,
    required this.isSelected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: lang.name,
      button: true,
      selected: isSelected,
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          splashColor: const Color(0xFF4A90E2).withOpacity(0.1),
          highlightColor: const Color(0xFF4A90E2).withOpacity(0.06),
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 150),
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
            decoration: BoxDecoration(
              color: isSelected
                  ? const Color(0xFF4A90E2).withOpacity(0.1)
                  : Colors.transparent,
              border: Border(
                left: BorderSide(
                  color: isSelected
                      ? const Color(0xFF4A90E2)
                      : Colors.transparent,
                  width: 3,
                ),
              ),
            ),
            child: Row(
              children: [
                SizedBox(
                  width: 36,
                  child: Text(
                    lang.flag,
                    style: const TextStyle(
                      fontSize: 24,
                      fontFamilyFallback: [
                        'Apple Color Emoji',
                        'Noto Color Emoji'
                      ],
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Text(
                    lang.name,
                    style: TextStyle(
                      color: isSelected
                          ? const Color(0xFF4A90E2)
                          : Colors.white.withOpacity(0.9),
                      fontSize: 14,
                      fontWeight: isSelected
                          ? FontWeight.w600
                          : FontWeight.normal,
                    ),
                  ),
                ),
                Text(
                  lang.code.toUpperCase(),
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.3),
                    fontSize: 11,
                    fontWeight: FontWeight.w500,
                    letterSpacing: 0.5,
                  ),
                ),
                if (isSelected) ...[
                  const SizedBox(width: 8),
                  const Icon(Icons.check_rounded,
                      color: Color(0xFF4A90E2), size: 18),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen>
    with SingleTickerProviderStateMixin {
  final _ocr = OcrService();
  final _picker = ImagePicker();

  AppState _state = AppState.ready;
  String _error = '';

  String _engine = 'easyocr';
  String _lang = 'auto';
  bool _fuzzy = false;
  String _fuzzer = 'symspell';

  Uint8List? _lastImageBytes;

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
  }

  @override
  void dispose() {
    _pulseController.dispose();
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
    await _processBytes(await file.readAsBytes());
  }

  Future<void> _processBytes(Uint8List imageBytes) async {
    setState(() => _state = AppState.loading);
    _announce('processing, please wait');

    try {
      final options = OcrOptions(
        engine: _engine,
        lang: _lang,
        fuzzy: _fuzzy,
        fuzzer: _fuzzer,
      );
      final response = await _ocr.processBytes(imageBytes, options);

      if (response.status == 'no_text_detected' || response.blocks.isEmpty) {
        _setError('no text was detected');
        return;
      }

      setState(() {
        _state = AppState.ready;
        _lastImageBytes = imageBytes;
      });
      if (!mounted) return;
      await Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => OcrResultScreen(
            imageBytes: imageBytes,
            response: response,
          ),
        ),
      );
    } on OcrException catch (e) {
      _setError(e.message);
    } catch (e) {
      _setError('unexpected error: $e');
    }
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
                style: TextStyle(
                    color: Colors.white.withOpacity(0.5), fontSize: 12),
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
                child: const Icon(Icons.settings_outlined,
                    color: Colors.white, size: 24),
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
        const SizedBox(height: 40),
        _buildInputButtons(),
        const SizedBox(height: 16),
        if (_lastImageBytes != null) ...[
          _buildLastImageStrip(),
          const SizedBox(height: 12),
        ],
        const SizedBox(height: 12),
        _buildOcrOptionsPanel(),
        const Spacer(),
        _buildFooter(),
      ],
    );
  }

  Widget _buildLastImageStrip() {
    final enabled = _state == AppState.ready || _state == AppState.error;
    return Semantics(
      label: 're-process last image',
      button: true,
      enabled: enabled,
      child: GestureDetector(
        onTap: enabled ? () => _processBytes(_lastImageBytes!) : null,
        child: Container(
          margin: const EdgeInsets.symmetric(horizontal: 20),
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.05),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: Colors.white.withOpacity(0.08)),
          ),
          child: Row(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: Image.memory(
                  _lastImageBytes!,
                  width: 52,
                  height: 52,
                  fit: BoxFit.cover,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Re-process last image',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                    const SizedBox(height: 2),
                    Text(
                      'with current settings',
                      style: TextStyle(
                        color: Colors.white.withOpacity(0.4),
                        fontSize: 11,
                      ),
                    ),
                  ],
                ),
              ),
              Icon(
                Icons.refresh_rounded,
                color: enabled
                    ? const Color(0xFF4A90E2)
                    : Colors.white.withOpacity(0.2),
                size: 22,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatusCard() {
    switch (_state) {
      case AppState.loading:
        return _statusCard(
          icon: const SizedBox(
            width: 32,
            height: 32,
            child: CircularProgressIndicator(
                color: Colors.white, strokeWidth: 3),
          ),
          text: 'Analysing document...',
          color: const Color(0xFF0F3460),
        );
      case AppState.error:
        return _statusCard(
          icon: const Icon(Icons.error_outline_rounded,
              color: Colors.redAccent, size: 32),
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

  Widget _statusCard(
      {required Widget icon, required String text, required Color color}) {
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
                style: const TextStyle(
                    color: Colors.white, fontSize: 15, height: 1.4),
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
                ? [
                    BoxShadow(
                        color: color.withOpacity(0.4),
                        blurRadius: 24,
                        spreadRadius: 4)
                  ]
                : [],
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: Colors.white, size: 44),
              const SizedBox(height: 8),
              Text(label,
                  style: const TextStyle(
                      color: Colors.white,
                      fontSize: 14,
                      fontWeight: FontWeight.w600)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLanguageSelectorButton() {
    final current = _kLanguages.firstWhere((l) => l.code == _lang,
        orElse: () => _kLanguages.first);
    return Semantics(
      label: 'selected language: ${current.name}',
      button: true,
      child: GestureDetector(
        onTap: _showLanguageMenu,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          decoration: BoxDecoration(
            color: const Color(0xFF4A90E2).withOpacity(0.12),
            borderRadius: BorderRadius.circular(10),
            border:
                Border.all(color: const Color(0xFF4A90E2).withOpacity(0.4)),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(current.flag,
                  style: const TextStyle(fontSize: 20,
                      fontFamilyFallback: ['Apple Color Emoji', 'Noto Color Emoji'])),
              const SizedBox(width: 8),
              Text(
                current.name,
                style: const TextStyle(
                    color: Colors.white,
                    fontSize: 13,
                    fontWeight: FontWeight.w500),
              ),
              const SizedBox(width: 6),
              Icon(Icons.expand_more_rounded,
                  color: Colors.white.withOpacity(0.55), size: 18),
            ],
          ),
        ),
      ),
    );
  }

  void _showLanguageMenu() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (ctx) => DraggableScrollableSheet(
        expand: false,
        initialChildSize: 0.55,
        minChildSize: 0.35,
        maxChildSize: 0.88,
        builder: (_, controller) => _LanguageMenu(
          selected: _lang,
          scrollController: controller,
          onSelected: (code) {
            setState(() => _lang = code);
            Navigator.pop(ctx);
          },
        ),
      ),
    );
  }

  Widget _buildOcrOptionsPanel() {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 20),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.08)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _optionLabel('Engine'),
          const SizedBox(height: 8),
          _chipRow(
            options: const ['easyocr', 'tesseract', 'paddleocr'],
            labels: const ['EasyOCR', 'Tesseract', 'PaddleOCR'],
            selected: _engine,
            onSelected: (v) => setState(() => _engine = v),
          ),
          const SizedBox(height: 14),
          _optionLabel('Language'),
          const SizedBox(height: 8),
          _buildLanguageSelectorButton(),
          const SizedBox(height: 14),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _optionLabel('Fuzzy matching'),
              Semantics(
                label: 'fuzzy matching toggle',
                child: Switch(
                  value: _fuzzy,
                  onChanged: (v) => setState(() => _fuzzy = v),
                  activeColor: const Color(0xFF4A90E2),
                  materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                ),
              ),
            ],
          ),
          if (_fuzzy) ...[
            const SizedBox(height: 8),
            _chipRow(
              options: const ['symspell', 'pyspellchecker'],
              labels: const ['SymSpell', 'PySpellchecker'],
              selected: _fuzzer,
              onSelected: (v) => setState(() => _fuzzer = v),
            ),
          ],
        ],
      ),
    );
  }

  Widget _optionLabel(String text) {
    return Text(
      text,
      style: TextStyle(
        color: Colors.white.withOpacity(0.55),
        fontSize: 11,
        fontWeight: FontWeight.w600,
        letterSpacing: 0.8,
      ),
    );
  }

  Widget _chipRow({
    required List<String> options,
    required List<String> labels,
    required String selected,
    required void Function(String) onSelected,
  }) {
    return Wrap(
      spacing: 8,
      runSpacing: 6,
      children: [
        for (int i = 0; i < options.length; i++)
          Semantics(
            label: labels[i],
            button: true,
            selected: selected == options[i],
            child: ChoiceChip(
              label: Text(labels[i]),
              selected: selected == options[i],
              onSelected: (_) => onSelected(options[i]),
              selectedColor: const Color(0xFF4A90E2),
              backgroundColor: Colors.white.withOpacity(0.08),
              labelStyle: TextStyle(
                color: selected == options[i]
                    ? Colors.white
                    : Colors.white.withOpacity(0.55),
                fontSize: 12,
                fontWeight: selected == options[i]
                    ? FontWeight.w600
                    : FontWeight.normal,
              ),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(8)),
              side: BorderSide(
                color: selected == options[i]
                    ? const Color(0xFF4A90E2)
                    : Colors.white.withOpacity(0.12),
              ),
              padding:
                  const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              visualDensity: VisualDensity.compact,
            ),
          ),
      ],
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
    final portCtrl =
        TextEditingController(text: BackendConfig.port.toString());

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF1A1A2E),
        shape:
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: const Text('Backend Settings',
            style: TextStyle(color: Colors.white)),
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
                  labelStyle:
                      TextStyle(color: Colors.white.withOpacity(0.6)),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide:
                        BorderSide(color: Colors.white.withOpacity(0.2)),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide:
                        const BorderSide(color: Color(0xFF4A90E2)),
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
                  labelStyle:
                      TextStyle(color: Colors.white.withOpacity(0.6)),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide:
                        BorderSide(color: Colors.white.withOpacity(0.2)),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                    borderSide:
                        const BorderSide(color: Color(0xFF4A90E2)),
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
            child: Text('Cancel',
                style: TextStyle(color: Colors.white.withOpacity(0.6))),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF4A90E2),
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12)),
            ),
            onPressed: () {
              BackendConfig.host = hostCtrl.text.trim();
              BackendConfig.port =
                  int.tryParse(portCtrl.text.trim()) ?? 8000;
              Navigator.pop(ctx);
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }
}
