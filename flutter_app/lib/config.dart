// change host to your laptop's IP before running
// mac: ipconfig getifaddr en0
class BackendConfig {
  static String host = '192.168.1.100';
  static int port = 8000;

  static String get ocrEndpoint => 'http://$host:$port/ocr';
  static String get healthEndpoint => 'http://$host:$port/health';
}
