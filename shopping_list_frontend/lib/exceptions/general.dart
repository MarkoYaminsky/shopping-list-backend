class InternetConnectionError implements Exception {
  static const String message = "A dog ate someone's Internet router.";
}

class NotAuthenticatedException implements Exception {
  static const String message = "This request requires authentication.";
}