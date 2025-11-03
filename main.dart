import 'dart:io';
import 'dart:math';

class BiEquation {
  /// Список коэффициентов уравнения
  List<double> coefs = [];

  /// Список корней уравнения
  List<double> roots = [];

  /// Дискриминант уравнения
  double? discriminant;

  /// Проверяет, не нулевой ли первый коэффициент
  ///
  /// [index]: индекс коэффициента
  /// [coef]: значение коэффициента
  ///
  /// Возвращает true, если коэффициент не нулевой или не первый
  /// Возвращает false, если коэффициент нулевой и первый
  static bool check_coef(int index, double coef) {
    return (index != 0) || (coef != 0);
  }

  /// Считывает коэффициенты из аргументов командной строки или с клавиатуры
  void get_coefs(List<String> args) {

    for (int i = 0; i < 3; i++) {
      try {
        // Пытаемся считать коэффициент из аргументов командной строки
        if (args.length > i) {
          final coef_str = args[i];
          final coef = double.parse(coef_str);

          // Проверяем, не нулевой ли первый коэффициент
          if (!check_coef(i, coef)) {
            print(
                "Первый коэффициент не может быть нулем! Используется интерактивный ввод.");
            throw Exception("Invalid coefficient");
          }

          // Добавляем коэффициент в список
          coefs.add(coef);
          continue;
        }
      } catch (e) {}

      double? coef;

      // Если не удалось считать из аргументов, запрашиваем с клавиатуры
      while (true) {
        // Выводим сообщение об ошибке
        print("Ошибка ввода коэффициента ${i + 1} из командной строки");
        try {
          // Пытаемся считать коэффициент с клавиатуры
          stdout.write('Введите коэффициент ${i + 1}: ');
          // Получаем ввод
          final input = stdin.readLineSync();
          // Проверяем, введено ли что-то
          if (input == null || input.isEmpty) {
            throw Exception("Ошибка ввода");
          }

          // Пытаемся преобразовать в число
          coef = double.parse(input);

          // Проверяем, не нулевой ли первый коэффициент
          if (!check_coef(i, coef)) {
            print("Первый коэффициент не может быть нулем!");
            continue;
          }

          break;
        } catch (e) {
          print("Ошибка: введите корректное число!");
        }
      }

      // Добавляем коэффициент в список
      coefs.add(coef);
    }
  }

  /// Вычисляет дискриминант уравнения
  void get_discriminant() {
    discriminant = coefs[1] * coefs[1] - 4 * coefs[0] * coefs[2];
  }

  /// Находит действительные корни уравнения с помощью дискриминанта
  void get_roots() {
    // Проверяем, введены ли коэффициенты
    if (coefs.length != 3) {
      print("Коэффициенты не введены");
      return;
    }

    // Вычисляем дискриминант
    get_discriminant();

    // Список временных корней до обратной замены
    List<double> temp_roots = [];

    // Если дискриминант больше нуля, то добавляем два корня
    if (discriminant! > 0) {
      temp_roots.add((-coefs[1] + sqrt(discriminant!)) / (2 * coefs[0]));
      temp_roots.add((-coefs[1] - sqrt(discriminant!)) / (2 * coefs[0]));
    }
    // Если дискриминант равен нулю, то добавляем один корень
    else if (discriminant == 0) {
      temp_roots.add(-coefs[1] / (2 * coefs[0]));
    }

    // Производим обратную замену
    for (final temp_root in temp_roots) {
      // Если до замены корень больше нуля, то добавляем его корень с разными знаками
      if (temp_root > 0) {
        roots.add(sqrt(temp_root));
        roots.add(-sqrt(temp_root));
      }
      // Если до замены корень равен нулю, то добавляем его
      else if (temp_root == 0) {
        roots.add(0);
      }
    }

    // Сортируем корни
    roots.sort();
  }

  /// Выводит корни уравнения
  void print_roots() {
    // Проверяем, есть ли корни
    if (roots.isEmpty) {
      print("Нет корней");
    } else {
      // Выводим все корни
      for (int i = 0; i < roots.length; i++) {
        print("Корень ${i + 1}: ${roots[i]}");
      }
    }
  }
}

/// Главная функция программы
void main(List<String> args) {
  // Создаем объект уравнения
  final equation = BiEquation();

  // Получаем коэффициенты
  equation.get_coefs(args);

  // Находим корни
  equation.get_roots();

  // Выводим корни
  equation.print_roots();
}
