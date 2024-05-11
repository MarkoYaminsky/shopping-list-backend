import 'package:flutter/material.dart';

class NoConnectionScreen extends StatelessWidget {
  const NoConnectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    Color errorColor = Theme.of(context).colorScheme.error;
    return Scaffold(
      appBar: AppBar(
        backgroundColor: errorColor,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "Error loading the app",
              style: TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.w900,
                color: errorColor,
              ),
            ),
            const SizedBox(height: 50),
            const Text(
              "Ані руш! Прохід охороняє Денис",
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            Image.asset('assets/denys.jpg'),
          ],
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        color: errorColor,
        height: 30,
      ),
    );
  }
}
