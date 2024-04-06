import 'package:flutter/material.dart';
import 'package:shopping_list_frontend/screens/registration.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'cubits/user/tos_failed_attempts_cubit.dart';

void main() {
  runApp(const App());
}

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => TOSFailedAttemptsCubit(),
      child: MaterialApp(
        title: 'Flutter Demo',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        home: const RegistrationScreen(),
      ),
    );
  }
}
