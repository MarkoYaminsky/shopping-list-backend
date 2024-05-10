import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shopping_list_frontend/exceptions/users.dart';
import 'package:shopping_list_frontend/services/api/users.dart';

abstract class RegistrationStatus {}

class RegistrationStatusInitial extends RegistrationStatus {}

class RegistrationStatusLoading extends RegistrationStatus {}

class RegistrationStatusCheckFailed extends RegistrationStatus {
  final String errorMessage;

  RegistrationStatusCheckFailed(this.errorMessage);
}

class RegistrationStatusSuccessful extends RegistrationStatus {}

abstract class TermsOfServiceStatus {}

class TermsOfServiceRequiresConfirmation extends TermsOfServiceStatus {
  static const int attemptsCount = 9;
  int failedAttemptsCount;

  TermsOfServiceRequiresConfirmation(this.failedAttemptsCount);
}

class TermsOfServiceAttemptLimitReached extends TermsOfServiceStatus {}

class RegistrationState {
  RegistrationStatus registrationStatus;
  TermsOfServiceStatus termsOfServiceStatus;

  RegistrationState({
    required this.termsOfServiceStatus,
    required this.registrationStatus,
  });

  RegistrationState copyWith({
    RegistrationStatus? registrationStatus,
    TermsOfServiceStatus? termsOfServiceStatus,
  }) {
    return RegistrationState(
      registrationStatus: registrationStatus ?? this.registrationStatus,
      termsOfServiceStatus: termsOfServiceStatus ?? this.termsOfServiceStatus,
    );
  }
}

class RegistrationCubit extends Cubit<RegistrationState> {
  UserApi userApi = UserApi();

  RegistrationCubit()
      : super(
          RegistrationState(
            termsOfServiceStatus: TermsOfServiceRequiresConfirmation(0),
            registrationStatus: RegistrationStatusInitial(),
          ),
        );

  void incrementFailedAttempts() {
    final termsOfServiceStatus = state.termsOfServiceStatus;
    if (termsOfServiceStatus is TermsOfServiceRequiresConfirmation &&
        termsOfServiceStatus.failedAttemptsCount <
            TermsOfServiceRequiresConfirmation.attemptsCount) {
      emit(
        state.copyWith(
          termsOfServiceStatus: TermsOfServiceRequiresConfirmation(
            termsOfServiceStatus.failedAttemptsCount + 1,
          ),
        ),
      );
    } else {
      emit(
        state.copyWith(
            termsOfServiceStatus: TermsOfServiceAttemptLimitReached()),
      );
    }
  }

  Future<void> registerUser({
    required String username,
    required String password,
  }) async {
    emit(state.copyWith(registrationStatus: RegistrationStatusLoading()));
    try {
      await userApi.checkRegistrationErrors(username: username);
    } on RegistrationCheckFailException catch (error) {
      emit(
        state.copyWith(
          registrationStatus: RegistrationStatusCheckFailed(error.message),
        ),
      );
      return;
    }
    await userApi.registerUser(
      username: username,
      password: password,
    );
    emit(state.copyWith(registrationStatus: RegistrationStatusSuccessful()));
  }
}
