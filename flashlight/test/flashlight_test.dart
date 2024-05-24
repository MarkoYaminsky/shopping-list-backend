import 'package:flutter_test/flutter_test.dart';
import 'package:flashlight/flashlight.dart';
import 'package:flashlight/flashlight_platform_interface.dart';
import 'package:flashlight/flashlight_method_channel.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';

class MockFlashlightPlatform
    with MockPlatformInterfaceMixin
    implements FlashlightPlatform {

  @override
  Future<String?> getPlatformVersion() => Future.value('42');
}

void main() {
  final FlashlightPlatform initialPlatform = FlashlightPlatform.instance;

  test('$MethodChannelFlashlight is the default instance', () {
    expect(initialPlatform, isInstanceOf<MethodChannelFlashlight>());
  });

  test('getPlatformVersion', () async {
    Flashlight flashlightPlugin = Flashlight();
    MockFlashlightPlatform fakePlatform = MockFlashlightPlatform();
    FlashlightPlatform.instance = fakePlatform;

    expect(await flashlightPlugin.getPlatformVersion(), '42');
  });
}
