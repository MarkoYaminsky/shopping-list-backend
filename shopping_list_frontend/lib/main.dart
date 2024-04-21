import 'package:flutter/material.dart';
import 'package:shopping_list_frontend/cubits/user/login_cubit.dart';
import 'package:shopping_list_frontend/cubits/user/user_cubit.dart';
import 'package:shopping_list_frontend/screens/home.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shopping_list_frontend/screens/loading_screen.dart';
import 'package:shopping_list_frontend/screens/login.dart';
import 'package:shopping_list_frontend/screens/no_connection.dart';
import 'package:shopping_list_frontend/screens/registration.dart';
import 'package:shopping_list_frontend/services/lifecycle/connection_listener.dart';
import 'cubits/general/internet_connection_cubit.dart';
import 'cubits/general/route_cubit.dart';
import 'cubits/user/registration_cubit.dart';

void main() {
  runApp(App());
}

class App extends StatelessWidget {
  App({super.key});

  final GlobalKey<ScaffoldMessengerState> rootScaffoldMessengerKey =
      GlobalKey<ScaffoldMessengerState>();
  final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider<RegistrationCubit>(
          create: (context) => RegistrationCubit(),
        ),
        BlocProvider<InternetConnectionCubit>(
          create: (context) => InternetConnectionCubit(),
        ),
        BlocProvider<LoginCubit>(
          create: (context) => LoginCubit(),
        ),
        BlocProvider<RouteCubit>(
          create: (context) => RouteCubit(),
        ),
        BlocProvider<UserCubit>(
          create: (context) => UserCubit(),
        )
      ],
      child: BlocListener<InternetConnectionCubit, InternetConnectionState>(
        listener: (context, state) {
          ConnectionStateListener.initialize(
            context: context,
            internetConnectionState: state,
            rootScaffoldMessengerKey: rootScaffoldMessengerKey,
            navigatorKey: navigatorKey,
          );
        },
        child: MaterialApp(
          title: 'Flutter Demo',
          theme: ThemeData(
            colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
            useMaterial3: true,
          ),
          home: const LoadingScreen(),
          scaffoldMessengerKey: rootScaffoldMessengerKey,
          navigatorKey: navigatorKey,
          routes: {
            AppRoute.registration.path: (context) => RegistrationScreen(),
            AppRoute.login.path: (context) => LoginScreen(),
            AppRoute.noConnection.path: (context) => const NoConnectionScreen(),
            AppRoute.home.path: (context) => const HomeScreen(),
          },
        ),
      ),
    );
  }
}
