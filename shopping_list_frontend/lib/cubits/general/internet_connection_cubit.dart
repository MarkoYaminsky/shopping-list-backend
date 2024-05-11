import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shopping_list_frontend/services/api/connectivity.dart';

enum InternetConnectionState {
  initial,
  noConnection,
  connectionRestored,
}

class InternetConnectionCubit extends Cubit<InternetConnectionState> {
  late ConnectivityCheck connectivityCheck;

  InternetConnectionCubit() : super(InternetConnectionState.initial) {
    connectivityCheck = ConnectivityCheck(
      onError: () {
        emit(InternetConnectionState.noConnection);
      },
      onSuccess: () {
        if (state != InternetConnectionState.initial) {
          emit(InternetConnectionState.connectionRestored);
        }
      },
    );
    connectivityCheck.listen();
  }

  void triggerConnectionFailed() async {
    emit(InternetConnectionState.noConnection);
  }
}
