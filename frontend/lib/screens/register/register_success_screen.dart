import 'package:flutter/material.dart';

class RegisterSuccessScreen extends StatelessWidget {
  const RegisterSuccessScreen({super.key});

  static const primaryColor = Color(0xFF026A6A);
  static const backgroundColor = Color(0xFFFAFAF8);
  static const textColor = Color(0xFF111827);
  static const secondaryTextColor = Color(0xFF5B6464);
  static const borderColor = Color(0xFFE5E7EB);
  static const lightTealColor = Color(0xFFE6F3F3);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: backgroundColor,
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 390),
            child: Column(
              children: [
                _buildHeader(),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(20, 56, 20, 32),
                    child: Column(
                      children: [
                        Expanded(
                          child: Center(
                            child: _buildSuccessContent(),
                          ),
                        ),
                        _buildLoginButton(context),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

Widget _buildHeader() {
  return Container(
    height: 64,
    padding: const EdgeInsets.symmetric(horizontal: 12),
    decoration: const BoxDecoration(
      border: Border(
        bottom: BorderSide(
          color: borderColor,
          width: 0.5,
        ),
      ),
    ),
    child: Row(
      children: [
        IconButton(
          onPressed: () {},
          icon: const Icon(
            Icons.arrow_back,
          ),
        ),
        const SizedBox(width: 4),
        const Text(
          'Minha Pós',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w700,
            color: primaryColor,
          ),
        ),
      ],
    ),
  );
}

  Widget _buildSuccessContent() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 72,
          height: 72,
          decoration: const BoxDecoration(
            color: lightTealColor,
            shape: BoxShape.circle,
          ),
          child: Center(
            child: Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: primaryColor.withValues(alpha: 0.1),
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.check,
                size: 32,
                color: primaryColor,
              ),
            ),
          ),
        ),
        const SizedBox(height: 24),
        const Text(
          'Conta criada com sucesso!',
          textAlign: TextAlign.center,
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.w700,
            color: textColor,
          ),
        ),
        const SizedBox(height: 12),
        const SizedBox(
          width: 290,
          child: Text(
            'Seu cadastro foi realizado com sucesso. '
            'Agora você já pode acessar sua conta e começar '
            'a acompanhar sua formação.',
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: 14,
              height: 1.5,
              color: secondaryTextColor,
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildLoginButton(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      height: 48,
      child: ElevatedButton(
        onPressed: () {
          // Login será implementado posteriormente.
        },
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: Colors.white,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        child: const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Fazer login',
              style: TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}