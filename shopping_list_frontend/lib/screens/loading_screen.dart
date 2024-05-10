import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shopping_list_frontend/cubits/user/user_cubit.dart';
import 'package:shopping_list_frontend/screens/home.dart';
import 'package:shopping_list_frontend/screens/login.dart';

class LoadingScreen extends StatelessWidget {
  const LoadingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: _awaitUser(context),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.done) {
          final userState = context.read<UserCubit>().state;
          if (userState is UserSuccess) {
            return const HomeScreen();
          } else if (userState is UserFailed) {
            return LoginScreen();
          }
        }
        return const Scaffold(
          body: Center(
            child: CircularProgressIndicator(),
          ),
        );
      },
    );
  }

  Future<void> _awaitUser(BuildContext context) async {
    final userCubit = context.read<UserCubit>();
    await userCubit.getUser();
  }
}
