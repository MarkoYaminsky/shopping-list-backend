import 'dart:convert';

import 'package:http/http.dart';

import 'package:shopping_list_frontend/exceptions/users.dart';
import 'package:shopping_list_frontend/types/users.dart';
import 'base.dart';

class UserService extends BaseRequestSender {
  @override
  String get basePath => "users/";

  Future<void> checkRegistrationErrors({required String username}) async {
    Response response = await create(
        path: "register/check/", body: {"username": username});
    if (response.statusCode == 400) {
      throw RegistrationCheckFailException(username);
    }
  }

  Future<void> registerUser(
      {required String username, required String password}) async {
    await create(
      path: "register/",
      body: {"username": username, "password": password},
    );
  }

  Future<LoginUserOutput> loginUser(
      {required String username, required String password}) async {
    Response response = await create(
      path: "login/",
      body: {"username": username, "password": password},
    );

    if (response.statusCode != 200) {
      throw InvalidLoginCredentialsException;
    }

    return LoginUserOutput.fromJson(jsonDecode(response.body));
  }
}
