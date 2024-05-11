import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:shopping_list_frontend/exceptions/general.dart';

class ConnectivityCheck {
  Function? onSuccess;
  late Function onError;

  ConnectivityCheck({
    Function? onError,
    this.onSuccess,
  }) {
    this.onError = onError ?? () => throw InternetConnectionError;
  }

  bool _checkInternetIsConnected(List<ConnectivityResult> results) {
    if ((results.contains(ConnectivityResult.mobile) ||
        results.contains(ConnectivityResult.wifi))) {
      return true;
    }
    return false;
  }

  void _triggerByCheckResults(List<ConnectivityResult> results) {
    if (_checkInternetIsConnected(results)) {
      onSuccess?.call();
      return;
    }
    onError();
  }

  void _triggerNotificationManually(bool isInternetConnected) {
    if (isInternetConnected) {
      onSuccess?.call();
      return;
    }
    onError();
  }

  Future<bool> trigger() async {
    final connectivityResults = await Connectivity().checkConnectivity();
    bool isInternetConnected = _checkInternetIsConnected(connectivityResults);
    _triggerNotificationManually(isInternetConnected);
    return isInternetConnected;
  }

  void listen() {
    Connectivity().onConnectivityChanged.listen(_triggerByCheckResults);
  }
}
