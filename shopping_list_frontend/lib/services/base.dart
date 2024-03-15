import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

Future<Map<String, String>> getTokenHeader() async {
  final SharedPreferences preferences = await SharedPreferences.getInstance();
  final String? token = preferences.getString("token");
  return {"Authorization": "Token $token"};
}

Future<Uri> getUrl(String path, {Map<String, String>? queryParameters}) async {
  return Uri(
    scheme: "http",
    host: "10.0.2.2",
    port: 8001,
    queryParameters: queryParameters,
    path: path,
  );
}

Future<http.Response> list({
  required String path,
  Map<String, String>? queryParameters,
  bool isAuthenticated = false,
}) async {
  Map<String, String> headers = isAuthenticated ? await getTokenHeader() : {};
  return http.get(await getUrl(path, queryParameters: queryParameters),
      headers: headers);
}

Future<http.Response> create(
    {required String path, body, isAuthenticated = false}) async {
  Map<String, String> headers = isAuthenticated ? await getTokenHeader() : {};
  return http.post(await getUrl(path), body: body, headers: headers);
}

Future<http.Response> retrieve(
    {required String path, isAuthenticated = false}) async {
  Map<String, String> headers = isAuthenticated ? await getTokenHeader() : {};
  return http.get(await getUrl(path), headers: headers);
}

Future<http.Response> update(
    {required String path, body, isAuthenticated = false}) async {
  Map<String, String> headers = isAuthenticated ? await getTokenHeader() : {};
  return http.patch(await getUrl(path), body: body, headers: headers);
}

Future<http.Response> delete(
    {required String path, isAuthenticated = false}) async {
  Map<String, String> headers = isAuthenticated ? await getTokenHeader() : {};
  return http.delete(await getUrl(path), headers: headers);
}
