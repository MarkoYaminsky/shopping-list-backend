import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shopping_list_frontend/cubits/user/user_cubit.dart';
import 'package:shopping_list_frontend/services/lifecycle/navigator.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final userCubit = context.read<UserCubit>();
    final appNavigator = AppNavigator(context);

    final userState = context.read<UserCubit>().state;
    if (userState is UserSuccess) {
      return Scaffold(
        appBar: AppBar(
          title: const Text("Home"),
          backgroundColor: Theme.of(context).primaryColor,
          titleTextStyle: const TextStyle(color: Colors.white, fontSize: 24),
        ),
        body: Center(
          child: Column(
            children: [
              Text(
                "This is a home screen. You are ${userState.user.username}.",
              ),
              const Text(
                "Do you enjoy this amazing home screen? If no, ",
                style: TextStyle(fontSize: 18),
              ),
              GestureDetector(
                onTap: () {
                  userCubit.eraseUser();
                  appNavigator.sendToLogin();
                },
                child: const Text(
                  "Log out",
                  style: TextStyle(
                    fontSize: 60,
                    decoration: TextDecoration.underline,
                  ),
                ),
              )
            ],
          ),
        ),
      );
    } else {
      appNavigator.sendToLogin();
      return const Text("Forbidden");
    }
  }
}
