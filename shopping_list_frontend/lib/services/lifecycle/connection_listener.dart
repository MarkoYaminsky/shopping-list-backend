import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shopping_list_frontend/cubits/general/internet_connection_cubit.dart';
import 'package:shopping_list_frontend/cubits/general/route_cubit.dart';
import 'package:shopping_list_frontend/services/lifecycle/navigator.dart';

import 'package:shopping_list_frontend/services/notifiers/popups.dart';

class ConnectionStateListener {
  ConnectionStateListener.initialize({
    required BuildContext context,
    required InternetConnectionState internetConnectionState,
    required GlobalKey<ScaffoldMessengerState> rootScaffoldMessengerKey,
    required GlobalKey<NavigatorState> navigatorKey,
  }) {
    final currentRoute = context.read<RouteCubit>().state;
    if (internetConnectionState == InternetConnectionState.noConnection) {
      navigatorKey.currentState?.pushReplacementNamed(
        AppRoute.noConnection.path,
      );
      SnackBarPopUp.error(
        message: "No Internet connection.",
        context: context,
        rootScaffoldMessengerKey: rootScaffoldMessengerKey,
      );
    } else if (internetConnectionState ==
        InternetConnectionState.connectionRestored) {
      navigatorKey.currentState?.pushReplacementNamed(currentRoute.path);
      SnackBarPopUp.message(
        message: "Internet connection established.",
        context: context,
        rootScaffoldMessengerKey: rootScaffoldMessengerKey,
      );
    }
  }
}
