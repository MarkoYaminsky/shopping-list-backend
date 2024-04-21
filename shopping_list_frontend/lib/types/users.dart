class LoginRegisterUserInput {
  final String username;
  final String password;

  const LoginRegisterUserInput({
    required this.username,
    required this.password,
  });
}

class RegisterUserCheckInput {
  final String username;

  const RegisterUserCheckInput({required this.username});
}

class LoginUserOutput {
  final String token;

  const LoginUserOutput({required this.token});

  factory LoginUserOutput.fromJson(Map<String, dynamic> json) {
    return LoginUserOutput(token: json["token"] as String);
  }
}

class User {
  final String username;

  User(this.username);

  factory User.fromJson(Map<String, dynamic> json) {
    return User(json["username"] as String);
  }
}
