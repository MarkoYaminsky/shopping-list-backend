import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

import 'flashlight_platform_interface.dart';

/// An implementation of [FlashlightPlatform] that uses method channels.
class MethodChannelFlashlight extends FlashlightPlatform {
  /// The method channel used to interact with the native platform.
  @visibleForTesting
  final methodChannel = const MethodChannel('flashlight');

  @override
  Future<String?> getPlatformVersion() async {
    final version = await methodChannel.invokeMethod<String>('getPlatformVersion');
    return version;
  }
}
