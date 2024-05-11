import 'package:bloc/bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shopping_list_frontend/services/api/users.dart';
import 'package:shopping_list_frontend/types/users.dart';
import 'package:shopping_list_frontend/exceptions/users.dart';

class LoginState {}

class LoginInitial extends LoginState {}

class LoginFailed extends LoginState {}

class LoginLoading extends LoginState {}

class LoginSuccessful extends LoginState {
  String message;

  LoginSuccessful(this.message);
}

class LoginCubit extends Cubit<LoginState> {
  final userApi = UserApi();

  LoginCubit() : super(LoginInitial());

  Future<LoginUserOutput?> login({
    required String username,
    required String password,
  }) async {
    emit(LoginLoading());
    try {
      final loginOutput =
          await userApi.loginUser(username: username, password: password);
      emit(LoginSuccessful("You have logged in as $username."));
      SharedPreferences preferences = await SharedPreferences.getInstance();
      preferences.setString("token", loginOutput.token);
      return loginOutput;
    } on InvalidLoginCredentialsException catch (_) {
      emit(LoginFailed());
      return null;
    }
  }
}
