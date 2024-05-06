import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shopping_list_frontend/services/api/connectivity.dart';

import 'package:shopping_list_frontend/cubits/general/internet_connection_cubit.dart';

String apiIp = "10.0.2.2";

abstract class BaseRequestSender {
  ConnectivityCheck connectivityCheck = ConnectivityCheck(onError: () {});
  InternetConnectionCubit internetConnectionCubit = InternetConnectionCubit();

  Future<Map<String, String>> _getTokenHeader() async {
    final SharedPreferences preferences = await SharedPreferences.getInstance();
    final String? token = preferences.getString("token");
    return {"Authorization": "Token $token"};
  }

  Future<http.Response?> _sendRequest(Function() requestHandler) async {
    bool isConnected = await connectivityCheck.trigger();
    if (!isConnected) {
      internetConnectionCubit.triggerConnectionFailed();
      return null;
    }
    return requestHandler();
  }

  String get basePath => "";

  Future<Uri> getUrl(String path,
          {Map<String, String>? queryParameters}) async =>
      Uri(
        scheme: "http",
        host: apiIp,
        port: 8001,
        queryParameters: queryParameters,
        path: "$basePath$path",
      );

  Future<http.Response> list({
    required String path,
    Map<String, String>? queryParameters,
    bool isAuthenticated = false,
  }) async {
    Map<String, String> headers =
        isAuthenticated ? await _getTokenHeader() : {};
    return http.get(
      await getUrl(path, queryParameters: queryParameters),
      headers: headers,
    );
  }

  Future<http.Response?> create(
      {required String path, body, isAuthenticated = false}) async {
    Map<String, String> headers =
        isAuthenticated ? await _getTokenHeader() : {};
    return _sendRequest(
      () async => http.post(await getUrl(path), body: body, headers: headers),
    );
  }

  Future<http.Response?> retrieve(
      {required String path, isAuthenticated = false}) async {
    Map<String, String> headers =
        isAuthenticated ? await _getTokenHeader() : {};
    return _sendRequest(
      () async => http.get(await getUrl(path), headers: headers),
    );
  }

  Future<http.Response?> update(
      {required String path, body, isAuthenticated = false}) async {
    Map<String, String> headers =
        isAuthenticated ? await _getTokenHeader() : {};
    return _sendRequest(
      () async => http.patch(await getUrl(path), body: body, headers: headers),
    );
  }

  Future<http.Response?> delete(
      {required String path, isAuthenticated = false}) async {
    Map<String, String> headers =
        isAuthenticated ? await _getTokenHeader() : {};
    return _sendRequest(
      () async => http.delete(await getUrl(path), headers: headers),
    );
  }
}
