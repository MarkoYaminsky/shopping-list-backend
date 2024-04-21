import 'package:bloc/bloc.dart';

enum AppRoute {
  registration,
  login,
  home,
  noConnection,
}

extension ValueExtension on AppRoute {
  String get path {
    switch (this) {
      case AppRoute.registration: return "/registration/";
      case AppRoute.login: return "/login/";
      case AppRoute.home: return "/home/";
      case AppRoute.noConnection: return "/no-connection/";
    }
  }
}

class RouteCubit extends Cubit<AppRoute> {
  RouteCubit() : super(AppRoute.home);

  void changeRoute(AppRoute route) {
    emit(route);
  }
}