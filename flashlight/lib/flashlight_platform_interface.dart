import 'package:plugin_platform_interface/plugin_platform_interface.dart';

import 'flashlight_method_channel.dart';

abstract class FlashlightPlatform extends PlatformInterface {
  /// Constructs a FlashlightPlatform.
  FlashlightPlatform() : super(token: _token);

  static final Object _token = Object();

  static FlashlightPlatform _instance = MethodChannelFlashlight();

  /// The default instance of [FlashlightPlatform] to use.
  ///
  /// Defaults to [MethodChannelFlashlight].
  static FlashlightPlatform get instance => _instance;

  /// Platform-specific implementations should set this with their own
  /// platform-specific class that extends [FlashlightPlatform] when
  /// they register themselves.
  static set instance(FlashlightPlatform instance) {
    PlatformInterface.verifyToken(instance, _token);
    _instance = instance;
  }

  Future<String?> getPlatformVersion() {
    throw UnimplementedError('platformVersion() has not been implemented.');
  }
}
