class RegistrationCheckFailException implements Exception {
  late final String message;

  RegistrationCheckFailException(String username) {
    message = "Username $username is already taken.";
  }

  @override
  String toString() => "RegistrationCheckFailException: $message";
}


class InvalidLoginCredentialsException implements Exception {
  static const String message = "Your username or password is incorrect.";

  @override
  String toString() => "InvalidLoginCredentials: $message";
}
