import 'package:flutter_bloc/flutter_bloc.dart';

class TOSFailedAttemptsCubit extends Cubit<int> {
  TOSFailedAttemptsCubit() : super(0);

  void incrementFailedAttempts() {
    emit(state + 1);
  }
}
