import 'package:form_builder_validators/form_builder_validators.dart';

String? Function(String?) usernameValidator = FormBuilderValidators.compose(
  [
    FormBuilderValidators.required(),
    FormBuilderValidators.minLength(
      3,
      errorText: "Username can't be shorter than 3 symbols.",
    ),
    FormBuilderValidators.maxLength(
      30,
      errorText: "Username can't be longer than 30 symbols.",
    )
  ],
);

String? Function(String?) passwordValidator = FormBuilderValidators.compose(
  [
    FormBuilderValidators.required(),
    FormBuilderValidators.minLength(
      8,
      errorText: "Password must have a minimum of 8 symbols.",
    ),
    FormBuilderValidators.match(
      r"\d+",
      errorText: "Password must contain at least 1 digit.",
    ),
    FormBuilderValidators.match(
      r"(?=.*[a-z])(?=.*[A-Z]).+",
      errorText: "Password must contain both upper and lower cases.",
    )
  ],
);

String? confirmPasswordValidator(
  String? value,
  String? passwordValue,
) {
  return FormBuilderValidators.compose([
    FormBuilderValidators.required(),
    (String? _) => validatedPasswordsMatch(value, passwordValue),
  ])(value);
}

String? validatedPasswordsMatch(String? value, String? passwordValue) {
  if (value == passwordValue) {
    return null;
  }
  return "Passwords must match.";
}
