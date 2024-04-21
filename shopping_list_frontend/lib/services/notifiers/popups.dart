import "package:flutter/material.dart";

enum SnackBarPopUpType { error, info }

class SnackBarPopUp {
  String? message;
  BuildContext context;
  GlobalKey<ScaffoldMessengerState>? rootScaffoldMessengerKey;

  SnackBarPopUp.message({
    required this.message,
    required this.context,
    this.rootScaffoldMessengerKey,
  }) {
    _triggerSnackBar(
      snackBarColor:
          Theme.of(context).snackBarTheme.backgroundColor ?? Colors.green,
      type: SnackBarPopUpType.info,
    );
  }

  SnackBarPopUp.error({
    required this.message,
    required this.context,
    this.rootScaffoldMessengerKey,
  }) {
    _triggerSnackBar(
      snackBarColor: Theme.of(context).colorScheme.error,
      type: SnackBarPopUpType.error,
    );
  }

  void _triggerSnackBar({
    required Color snackBarColor,
    required SnackBarPopUpType type,
  }) {
    Widget shownContent = Text(
      message ?? (type == SnackBarPopUpType.error ? "Error" : "Success"),
      style: const TextStyle(color: Colors.white),
    );
    try {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: shownContent,
          backgroundColor: snackBarColor,
          duration: const Duration(milliseconds: 2500),
        ),
      );
    } catch (_) {
      rootScaffoldMessengerKey?.currentState?.showSnackBar(
        SnackBar(
          content: shownContent,
          backgroundColor: snackBarColor,
          duration: const Duration(milliseconds: 2500),
        ),
      );
    }
  }
}
