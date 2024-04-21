import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shopping_list_frontend/cubits/general/route_cubit.dart';
import 'package:shopping_list_frontend/cubits/user/user_cubit.dart';

class AppNavigator {
  final BuildContext _context;
  late RouteCubit _routeCubit;
  static const _protectedRoutes = [AppRoute.home];

  AppNavigator(this._context) {
    _routeCubit = _context.read<RouteCubit>();
  }

  void _navigate({
    required void Function(BuildContext, String) navigatorFunction,
    required AppRoute route,
  }) {
    navigatorFunction(_context, route.path);
    _routeCubit.changeRoute(route);
  }

  void sendToLogin() {
    _navigate(
      navigatorFunction: Navigator.pushReplacementNamed,
      route: AppRoute.login,
    );
  }

  void _protect({
    required void Function(BuildContext, String) navigatorFunction,
    required AppRoute route,
  }) async {
    final userCubit = _context.read<UserCubit>();

    if (_protectedRoutes.contains(route) && userCubit.state is UserInitial) {
      final user = await userCubit.getUser();
      if (user == null) {
        sendToLogin();
        return;
      }
    }

    _navigate(navigatorFunction: navigatorFunction, route: route);
  }

  void pushReplacementNamed(AppRoute route) {
    _protect(navigatorFunction: Navigator.pushReplacementNamed, route: route);
  }
}
