import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/screens/register/register_success_screen.dart';

void main() {
  testWidgets('exibe a tela de cadastro criado com sucesso', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: RegisterSuccessScreen(),
      ),
    );

    expect(find.text('Minha Pós'), findsOneWidget);
    expect(find.text('Conta criada com sucesso!'), findsOneWidget);
    expect(
      find.text(
        'Seu cadastro foi realizado com sucesso. '
        'Agora você já pode acessar sua conta e começar '
        'a acompanhar sua formação.',
      ),
      findsOneWidget,
    );
    expect(find.text('Fazer login'), findsOneWidget);
    expect(find.byIcon(Icons.arrow_back), findsOneWidget);
  });
}