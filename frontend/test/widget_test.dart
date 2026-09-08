import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/app/app.dart';

void main() {
  testWidgets('exibe a tela de cadastro', (WidgetTester tester) async {
    await tester.pumpWidget(const MinhaPosApp());

    expect(find.text('Criar sua conta'), findsOneWidget);
  });
}