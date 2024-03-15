import 'dart:convert';

import 'package:http/http.dart';

import '../exceptions/users.dart';
import '../types/users.dart';
import 'base.dart';

Future<void> checkRegistrationErrors({required String username}) async {
  Response response =
      await create(path: "users/register/check/", body: {"username": username});
  if (response.statusCode == 400) {
    throw RegistrationCheckFailException(username);
  }
}

void registerUser({required String username, required String password}) async {
  await create(
    path: "users/register/",
    body: {"username": username, "password": password},
  );
}

Future<LoginUserOutput> loginUser(
    {required String username, required String password}) async {
  Response response = await create(
    path: "users/login/",
    body: {"username": username, "password": password},
  );

  if (response.statusCode != 200) {
    throw InvalidLoginCredentialsException;
  }

  return LoginUserOutput.fromJson(jsonDecode(response.body));
}
