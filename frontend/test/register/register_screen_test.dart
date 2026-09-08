import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/screens/register/register_screen.dart';

void main() {
  testWidgets('exibe os campos e o botão de cadastro', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: RegisterScreen(),
      ),
    );

    expect(find.text('Criar sua conta'), findsOneWidget);
    expect(find.text('NOME COMPLETO'), findsOneWidget);
    expect(find.text('NOME PREFERIDO'), findsOneWidget);
    expect(find.text('E-MAIL'), findsOneWidget);
    expect(find.text('SENHA'), findsOneWidget);
    expect(find.text('CONFIRMAR SENHA'), findsOneWidget);
    expect(find.text('Criar conta'), findsOneWidget);
  });
}