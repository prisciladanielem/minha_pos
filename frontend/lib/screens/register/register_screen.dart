import 'package:flutter/material.dart';
import '../../services/user_service.dart';
import '../register/register_success_screen.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  static const primaryColor = Color(0xFF026A6A);
  static const backgroundColor = Color(0xFFFAFAF8);
  static const textColor = Color(0xFF111827);
  static const secondaryTextColor = Color(0xFF5B6464);
  static const borderColor = Color(0xFFE5E7EB);
  bool _isPasswordVisible = false;
  bool _isPasswordConfirmationVisible = false;

  final _passwordController = TextEditingController();
  final _passwordConfirmationController = TextEditingController();
  final _nameController = TextEditingController();
  final _preferredNameController = TextEditingController();
  final _emailController = TextEditingController();

  final _userService = UserService();

  bool get _isFormValid {
  final password = _passwordController.text;
  final confirmation = _passwordConfirmationController.text;

  return password.length >= 8 &&
      password.contains(RegExp(r'[A-Z]')) &&
      password.contains(RegExp(r'[a-z]')) &&
      password.contains(RegExp(r'[0-9]')) &&
      password.contains(RegExp(r'[^a-zA-Z0-9]')) &&
      password == confirmation;
}

  Future<void> _createAccount() async{
  if (_passwordController.text.length < 8) {
    return;
  }

  if (!_passwordController.text.contains(RegExp(r'[A-Z]'))) {
    return;
  }

  if (!_passwordController.text.contains(RegExp(r'[a-z]'))) {
    return;
  }

  if (!_passwordController.text.contains(RegExp(r'[0-9]'))) {
    return;
  }

  if (!_passwordController.text.contains(RegExp(r'[^a-zA-Z0-9]'))) {
    return;
  }

  if (_passwordController.text !=
      _passwordConfirmationController.text) {
    return;
  }

  final success = await _userService.createUser(
    name: _nameController.text,
    preferredName: _preferredNameController.text.isEmpty
        ? null
        : _preferredNameController.text,
    email: _emailController.text,
    password: _passwordController.text,
    passwordConfirmation: _passwordConfirmationController.text,
  );

  if (!mounted) {
    return;
  }

  if (success) {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => const RegisterSuccessScreen(),
      ),
  );
  }
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: backgroundColor,
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 390),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                children: [
                  _buildHeader(),
                  Expanded(
                    child: SingleChildScrollView(child: _buildContent()),
                  ),
                  _buildFooter(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return SizedBox(
      height: 60,
      child: Row(
        children: [
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.arrow_back),
            color: secondaryTextColor,
          ),
          const Spacer(),
          const Text(
            'Minha Pós',
            style: TextStyle(
              color: primaryColor,
              fontSize: 18,
              fontWeight: FontWeight.bold,
            ),
          ),
          const Spacer(),
          const SizedBox(width: 48),
        ],
      ),
    );
  }

  Widget _buildContent() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 12),
        const Text(
          'Criar sua conta',
          style: TextStyle(
            color: textColor,
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 6),
        const Text(
          'Preencha seus dados para iniciar o acompanhamento '
          'da sua formação acadêmica e clínica.',
          style: TextStyle(
            color: secondaryTextColor,
            fontSize: 13,
            height: 1.5,
          ),
        ),
        const SizedBox(height: 20),

        _buildTextField(
          label: 'NOME COMPLETO',
          hint: 'Ex: Mariana Vasconcelos',
          controller: _nameController,
          icon: Icons.person_outline,
        ),

        const SizedBox(height: 16),

        _buildTextField(
          label: 'NOME PREFERIDO',
          hint: 'Como quer ser chamado',
          controller: _preferredNameController,
          icon: Icons.badge_outlined,
          optional: true,
        ),

        const SizedBox(height: 16),

        _buildTextField(
          label: 'E-MAIL',
          hint: 'seu.email@instituicao.edu.br',
          controller: _emailController,
          icon: Icons.mail_outline,
          keyboardType: TextInputType.emailAddress,
        ),

        const SizedBox(height: 16),

        _buildTextField(
          label: 'SENHA',
          hint: 'Crie uma senha segura',
          icon: Icons.lock_outline,
          controller: _passwordController,
          obscureText: !_isPasswordVisible,
          onChanged: (_) {
            setState(() {});
          },
          onVisibilityPressed: () {
            setState(() {
              _isPasswordVisible = !_isPasswordVisible;
            });
          },
        ),

        const SizedBox(height: 8),

        _buildPasswordRequirements(),

        const SizedBox(height: 16),

        _buildTextField(
          label: 'CONFIRMAR SENHA',
          hint: 'Digite a mesma senha novamente',
          icon: Icons.lock_reset,
          obscureText: !_isPasswordConfirmationVisible,
          controller: _passwordConfirmationController,
          onChanged: (_) {
            setState(() {});
          },
          onVisibilityPressed: () {
            setState(() {
              _isPasswordConfirmationVisible = !_isPasswordConfirmationVisible;
            });
          },
        ),
        const SizedBox(height: 32),

        SizedBox(
          width: double.infinity,
          height: 48,
          child: ElevatedButton(
            onPressed: _isFormValid ? _createAccount : null,
            style: ElevatedButton.styleFrom(
              backgroundColor: primaryColor,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: const Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'Criar conta',
                  style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
                ),
                SizedBox(width: 8),
                Icon(Icons.arrow_forward, size: 20),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildPasswordRequirements() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: borderColor),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.shield_outlined, size: 16, color: primaryColor),
              SizedBox(width: 6),
              Text(
                'Sua senha deve conter:',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w600,
                  color: textColor,
                ),
              ),
            ],
          ),
          const SizedBox(height: 6),
          _buildPasswordRequirement(
            'Mínimo de 8 caracteres',
            _passwordController.text.length >= 8,
          ),
          _buildPasswordRequirement(
            'Uma letra maiúscula',
            _passwordController.text.contains(RegExp(r'[A-Z]')),
          ),
          _buildPasswordRequirement(
            'Uma letra minúscula',
            _passwordController.text.contains(RegExp(r'[a-z]')),
          ),
          _buildPasswordRequirement(
            'Um número',
            _passwordController.text.contains(RegExp(r'[0-9]')),
          ),
          _buildPasswordRequirement(
            'Um símbolo (ex: @, #, \$, !)',
            _passwordController.text.contains(
              RegExp(r'[^a-zA-Z0-9]'),
            ),
          ),
          _buildPasswordRequirement(
            'As senhas devem ser iguais',
            _passwordController.text == _passwordConfirmationController.text &&
                _passwordController.text.isNotEmpty,
          ),
        ],
      ),
    );
  }

  Widget _buildPasswordRequirement(String text, bool isValid) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Icon(
            isValid ? Icons.check_circle : Icons.radio_button_unchecked,
            size: 14,
            color: isValid
                ? const Color(0xFF80C8C3)
                : const Color(0xFFD1D5DB),
          ),
          const SizedBox(width: 6),
          Text(
            text,
            style: const TextStyle(fontSize: 11, color: secondaryTextColor),
          ),
        ],
      ),
    );
  }

  Widget _buildTextField({
    required String label,
    required String hint,
    required IconData icon,
    bool optional = false,
    bool obscureText = false,
    TextInputType? keyboardType,
    VoidCallback? onVisibilityPressed,
    TextEditingController? controller,
    ValueChanged<String>? onChanged,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              label,
              style: const TextStyle(
                color: Color(0xFF374151),
                fontSize: 11,
                fontWeight: FontWeight.w600,
                letterSpacing: 1,
              ),
            ),
            if (optional)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  color: Color(0xFFF0F2F1),
                  borderRadius: BorderRadius.circular(999),
                ),
                child: const Text(
                  'Opcional',
                  style: TextStyle(color: Color(0xFF6B7280), fontSize: 11),
                ),
              ),
          ],
        ),
        const SizedBox(height: 6),
        TextField(
          controller: controller,
          obscureText: obscureText == true,
          onChanged: onChanged,
          keyboardType: keyboardType,
          decoration: InputDecoration(
            hintText: hint,
            prefixIcon: Icon(icon, color: Color(0xFF9CA3AF), size: 20),
            suffixIcon: onVisibilityPressed != null
                ? IconButton(
                    onPressed: onVisibilityPressed,
                    icon: Icon(
                      obscureText
                          ? Icons.visibility_outlined
                          : Icons.visibility_off_outlined,
                      color: const Color(0xFF9CA3AF),
                      size: 20,
                    ),
                  )
                : null,
            filled: true,
            fillColor: Colors.white,
            contentPadding: const EdgeInsets.symmetric(
              horizontal: 16,
              vertical: 12,
            ),
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: borderColor),
            ),
            enabledBorder: OutlineInputBorder(
              borderRadius: BorderRadius.circular(12),
              borderSide: const BorderSide(color: borderColor),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildFooter() {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 12),
      decoration: const BoxDecoration(
        border: Border(top: BorderSide(color: Color(0xFFECEEEB))),
      ),
      child: const Center(
        child: Text.rich(
          TextSpan(
            text: 'Já possui uma conta? ',
            style: TextStyle(color: secondaryTextColor, fontSize: 14),
            children: [
              TextSpan(
                text: 'Fazer login',
                style: TextStyle(
                  color: primaryColor,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
