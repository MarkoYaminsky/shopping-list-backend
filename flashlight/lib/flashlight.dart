
import 'flashlight_platform_interface.dart';

class Flashlight {
  Future<String?> getPlatformVersion() {
    return FlashlightPlatform.instance.getPlatformVersion();
  }
}
