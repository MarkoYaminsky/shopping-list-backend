import 'package:bloc/bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shopping_list_frontend/exceptions/general.dart';
import 'package:shopping_list_frontend/services/api/users.dart';
import 'package:shopping_list_frontend/types/users.dart';

abstract class UserState {}

class UserInitial extends UserState {}

class UserFailed extends UserState {}

class UserSuccess extends UserState {
  User user;

  UserSuccess(this.user);
}

class UserCubit extends Cubit<UserState> {
  final userApi = UserApi();

  UserCubit() : super(UserInitial());

  Future<User?> getUser() async {
    try {
      final user = await UserApi().getUserInfo();
      emit(UserSuccess(user));
      return user;
    } on NotAuthenticatedException catch (_) {
      emit(UserFailed());
      return null;
    }
  }

  Future<void> eraseUser() async {
    final sharedPreferences = await SharedPreferences.getInstance();
    sharedPreferences.remove("token");
  }
}
