import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';

import 'package:shopping_list_frontend/services/api/users.dart';
import 'package:shopping_list_frontend/exceptions/users.dart';
import 'package:shopping_list_frontend/services/notifiers/popups.dart';
import 'package:shopping_list_frontend/validators/user_validators.dart';
import 'package:shopping_list_frontend/cubits/user/tos_failed_attempts_cubit.dart';

const int tosUnconditionalSuccessfulAttempt = 9;

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

class RegistrationScreen extends StatefulWidget {
  const RegistrationScreen({super.key});

  @override
  State<RegistrationScreen> createState() => _RegistrationScreenState();
}

class _RegistrationScreenState extends State<RegistrationScreen> {
  final _formKey = GlobalKey<FormBuilderState>();

  bool _validateForm() {
    bool isFormValid = _formKey.currentState!.validate();
    if (!isFormValid) return false;
    bool? termsOfServiceValue =
        _formKey.currentState?.fields["termsOfService"]?.value;
    if (termsOfServiceValue != true &&
        context.read<TOSFailedAttemptsCubit>().state <
            tosUnconditionalSuccessfulAttempt) {
      context.read<TOSFailedAttemptsCubit>().incrementFailedAttempts();
      SnackBarPopUp.error(
        message: failedAttemptsToMessage[
            context.read<TOSFailedAttemptsCubit>().state],
        context: context,
      );
      return false;
    }
    return true;
  }

  Future<void> _submitForm() async {
    if (!_validateForm()) {
      return;
    }
    Map fields = _formKey.currentState!.fields;
    UserApi userApi = UserApi();
    try {
      await userApi.checkRegistrationErrors(username: fields["username"].value);
    } catch (error) {
      if (error is RegistrationCheckFailException && context.mounted) {
        SnackBarPopUp.error(message: error.message, context: context);
        return;
      }
    }
    await userApi.registerUser(
      username: fields["username"].value,
      password: fields["password"].value,
    );
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
      body: Padding(
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
                validator: usernameValidator,
                autovalidateMode: AutovalidateMode.onUserInteraction,
                decoration: const InputDecoration(hintText: "Username"),
              ),
              FormBuilderTextField(
                name: "password",
                obscureText: true,
                validator: passwordValidator,
                autovalidateMode: AutovalidateMode.onUserInteraction,
                decoration: const InputDecoration(hintText: "Password"),
              ),
              FormBuilderTextField(
                name: "confirmPassword",
                validator: (value) => confirmPasswordValidator(
                  value,
                  _formKey.currentState?.fields["password"]?.value,
                ),
                autovalidateMode: AutovalidateMode.onUserInteraction,
                decoration: const InputDecoration(hintText: "Confirm password"),
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
                  onPressed: _submitForm,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    shape: const RoundedRectangleBorder(
                      borderRadius: BorderRadius.all(
                        Radius.circular(10),
                      ),
                    ),
                  ),
                  child: const Text(
                    "Submit",
                    style: TextStyle(color: Colors.white, fontSize: 18),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
