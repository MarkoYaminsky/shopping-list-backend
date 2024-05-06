import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shopping_list_frontend/cubits/general/route_cubit.dart';
import 'package:shopping_list_frontend/cubits/user/login_cubit.dart';
import 'package:shopping_list_frontend/cubits/user/user_cubit.dart';

import 'package:shopping_list_frontend/exceptions/users.dart';
import 'package:shopping_list_frontend/services/notifiers/popups.dart';
import 'package:shopping_list_frontend/validators/user/user_validators.dart';

import 'package:shopping_list_frontend/services/lifecycle/navigator.dart';

class LoginScreen extends StatelessWidget {
  LoginScreen({super.key});

  final _formKey = GlobalKey<FormBuilderState>();
  final userCubit = UserCubit();

  Future<void> _submitForm(BuildContext context) async {
    var currentState = _formKey.currentState!;
    if (!currentState.validate()) {
      return;
    }
    Map fields = currentState.fields;
    final response = await context.read<LoginCubit>().login(
          username: fields["username"].value,
          password: fields["password"].value,
        );
    if (response != null) {
      SharedPreferences preferences = await SharedPreferences.getInstance();
      preferences.setString("token", response.token);
    }
  }

  @override
  Widget build(BuildContext context) {
    final appNavigator = AppNavigator(context);

    return Scaffold(
      resizeToAvoidBottomInset: false,
      appBar: AppBar(
        backgroundColor: Colors.blue,
        title: const Text(
          "Login",
          style: TextStyle(color: Colors.white),
        ),
      ),
      body: BlocConsumer<LoginCubit, LoginState>(
        listener: (context, state) {
          if (state is LoginFailed) {
            SnackBarPopUp.error(
              message: InvalidLoginCredentialsException.message,
              context: context,
            );
          } else if (state is LoginSuccessful) {
            SnackBarPopUp.message(
              context: context,
              message: state.message,
            );
            appNavigator.pushReplacementNamed(AppRoute.loading);
          }
        },
        builder: (context, state) {
          return Padding(
            padding: const EdgeInsets.all(20),
            child: FormBuilder(
              key: _formKey,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    "Log in to your account",
                    style: TextStyle(fontSize: 30, fontWeight: FontWeight.w700),
                  ),
                  const SizedBox(height: 120),
                  FormBuilderTextField(
                    name: "username",
                    validator: UserValidator.usernameValidator,
                    autovalidateMode: AutovalidateMode.onUserInteraction,
                    decoration: const InputDecoration(hintText: "Username"),
                  ),
                  FormBuilderTextField(
                    name: "password",
                    obscureText: true,
                    validator: UserValidator.passwordValidator,
                    autovalidateMode: AutovalidateMode.onUserInteraction,
                    decoration: const InputDecoration(hintText: "Password"),
                  ),
                  const SizedBox(height: 120),
                  SizedBox(
                    width: 320,
                    child: ElevatedButton(
                      onPressed: () => _submitForm(context),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue,
                        shape: const RoundedRectangleBorder(
                          borderRadius: BorderRadius.all(
                            Radius.circular(10),
                          ),
                        ),
                      ),
                      child: state is LoginLoading
                          ? const CircularProgressIndicator()
                          : const Text(
                              "Submit",
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 18,
                              ),
                            ),
                    ),
                  ),
                  const SizedBox(height: 5),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text("Don't have an account yet? "),
                      GestureDetector(
                        onTap: () => appNavigator.pushReplacementNamed(
                          AppRoute.registration,
                        ),
                        child: Text(
                          "Register",
                          style: TextStyle(
                            decoration: TextDecoration.underline,
                            color: Theme.of(context).primaryColor,
                          ),
                        ),
                      )
                    ],
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
