import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:shopping_list_frontend/cubits/general/route_cubit.dart';
import 'package:shopping_list_frontend/cubits/user/login_cubit.dart';
import 'package:shopping_list_frontend/services/lifecycle/navigator.dart';

import 'package:shopping_list_frontend/services/notifiers/popups.dart';
import 'package:shopping_list_frontend/validators/user/user_validators.dart';
import 'package:shopping_list_frontend/cubits/user/registration_cubit.dart';

Map<int, String> failedAttemptsToMessage = {
  1: "Please read and agree to the terms of service.",
  2: "You don't actually have to read the terms of service, just agree.",
  3: "Oh come on, it this so hard for you?",
  4: "...",
  5: "Stop being stubborn.",
  6: "We can do this for hours.",
  7: "This is disgusting...",
  8: "Don't provoke me.",
  9: "Okay, fine, I guess you can't read. Sure, whatever, you can register."
};

class RegistrationScreen extends StatelessWidget {
  RegistrationScreen({super.key});

  final _formKey = GlobalKey<FormBuilderState>();

  bool _validateTermsOfService(BuildContext context) {
    bool? termsOfServiceValue =
        _formKey.currentState?.fields["termsOfService"]?.value;
    if (termsOfServiceValue != true &&
        context.read<RegistrationCubit>().state.termsOfServiceStatus
            is TermsOfServiceRequiresConfirmation) {
      context.read<RegistrationCubit>().incrementFailedAttempts();
      return false;
    }
    return true;
  }

  bool _validateForm(BuildContext context) {
    bool isFormValid = _formKey.currentState?.validate() ?? false;
    if (!isFormValid) return false;
    return _validateTermsOfService(context);
  }

  Future<void> _submitForm(BuildContext context) async {
    final loginCubit = context.read<LoginCubit>();
    final registrationCubit = context.read<RegistrationCubit>();
    if (!_validateForm(context)) {
      return;
    }
    Map fields = _formKey.currentState!.fields;
    String username = fields["username"].value;
    String password = fields["password"].value;
    await registrationCubit.registerUser(
          username: username,
          password: password,
        );
    await loginCubit.login(username: username, password: password);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      appBar: AppBar(
        backgroundColor: Colors.blue,
        title: const Text(
          "Registration",
          style: TextStyle(color: Colors.white),
        ),
      ),
      body: BlocConsumer<RegistrationCubit, RegistrationState>(
        listener: (context, state) {
          final registrationStatus = state.registrationStatus;
          final termsOfServiceStatus = state.termsOfServiceStatus;
          if (registrationStatus is RegistrationStatusCheckFailed) {
            SnackBarPopUp.error(
              message: registrationStatus.errorMessage,
              context: context,
            );
          } else if (state.registrationStatus is RegistrationStatusSuccessful) {
            SnackBarPopUp.message(
              context: context,
              message: "You are successfully registered.",
            );
            AppNavigator(context).pushReplacementNamed(AppRoute.home);
          }
          if (termsOfServiceStatus is TermsOfServiceRequiresConfirmation &&
              termsOfServiceStatus.failedAttemptsCount > 0) {
            SnackBarPopUp.error(
              message: failedAttemptsToMessage[
                  termsOfServiceStatus.failedAttemptsCount],
              context: context,
            );
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
                    "Create your account",
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
                  FormBuilderTextField(
                    name: "confirmPassword",
                    validator: (value) =>
                        UserValidator.confirmPasswordValidator(
                      value,
                      _formKey.currentState?.fields["password"]?.value,
                    ),
                    autovalidateMode: AutovalidateMode.onUserInteraction,
                    decoration:
                        const InputDecoration(hintText: "Confirm password"),
                  ),
                  FormBuilderCheckbox(
                    name: "termsOfService",
                    title: const Text(
                      "I have read and agreed to the terms of service.",
                    ),
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
                      child:
                          state.registrationStatus is RegistrationStatusLoading
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
                      const Text("Have an account already? "),
                      GestureDetector(
                        onTap: () => AppNavigator(context)
                            .pushReplacementNamed(AppRoute.login),
                        child: Text(
                          "Log in",
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
