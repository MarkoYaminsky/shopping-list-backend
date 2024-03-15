import 'package:flutter/material.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:shopping_list_frontend/services/users.dart';

import '../exceptions/users.dart';

class RegistrationScreen extends StatefulWidget {
  const RegistrationScreen({super.key});

  @override
  State<RegistrationScreen> createState() => _RegistrationScreenState();
}

class _RegistrationScreenState extends State<RegistrationScreen> {
  final _formKey = GlobalKey<FormBuilderState>();

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
                decoration: const InputDecoration(hintText: "Username"),
              ),
              FormBuilderTextField(
                name: "password",
                obscureText: true,
                decoration: const InputDecoration(hintText: "Password"),
              ),
              FormBuilderCheckbox(
                name: "terms of service",
                title: const Text(
                    "I have read and agree to the terms of service."),
              ),
              const SizedBox(height: 120),
              SizedBox(
                width: 320,
                child: ElevatedButton(
                  onPressed: () async {
                    Map fields = _formKey.currentState!.fields;
                    try {
                      await checkRegistrationErrors(username: fields["username"].value);
                    } catch (error) {
                      if (error is RegistrationCheckFailException) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text(error.message)),
                        );
                        return;
                      }
                    }
                    registerUser(
                      username: fields["username"].value,
                      password: fields["password"].value,
                    );
                  },
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
