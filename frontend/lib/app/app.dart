import 'package:flutter/material.dart';

import '../screens/register/register_screen.dart';

class MinhaPosApp extends StatelessWidget {
  const MinhaPosApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Minha Pós',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.deepPurple,
        ),
        useMaterial3: true,
      ),
      home: const RegisterScreen(),
    );
  }
}
