import 'dart:convert';

import 'package:http/http.dart' as http;

class UserService {
  Future<void> createUser({
    required String name,
    String? preferredName,
    required String email,
    required String password,
    required String passwordConfirmation,
  }) async {
    final response = await http.post(
      Uri.parse('http://localhost:8000/users'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'name': name,
        'preferred_name': preferredName,
        'email': email,
        'password': password,
        'password_confirmation': passwordConfirmation,
      }),
    );

    print(response.statusCode);
    print(response.body);
  }
}