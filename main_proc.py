import math
import sys
    
def check_coef(index:int, coef:float) -> bool:
    '''
    Проверяет, не нулевой ли первый коэффициент
    
    Args:
        index (int): индекс коэффициента
        coef (float): коэффициент
        
    Returns:
        bool: True, если коэффициент не нулевой или не первый
              False, если коэффициент нулевой и первый
    '''
    return (index != 0) or (coef != 0)
    
def get_coefs() -> list[float]:
    '''
    Считывает коэффициенты из командной строки или с клавиатуры
    
    Returns:
        list[float]: список коэффициентов
    '''
    
    # Список коэффициентов
    coefs = []
    
    for i in range(3):
        try:
            # Пытаемся считать коэффициент из командной строки
            coef_str = sys.argv[i+1]
            # Пытаемся преобразовать в число
            coef = float(coef_str)
            # Проверяем, не нулевой ли первый коэффициент
            if not check_coef(i, coef):
                # Если коэффициент нулевой и первый, то выводим сообщение
                print(f"Первый коэффициент не может быть нулем! Используется интерактивный ввод.")
                raise ValueError
        except:
            # Если не получилось, то коэффициент = None
            coef = None

        # Проверяем, не нулевой ли первый коэффициент
        if coef is None or not check_coef(i, coef):
            # Выводим сообщение об ошибке
            print(f"Ошибка ввода коэффициента {i+1} из командной строки")
            while True:
                try:
                    # Пытаемся считать коэффициент с клавиатуры
                    coef_str = input(f"Введите коэффициент {i+1}: ")
                    # Пытаемся преобразовать в число
                    coef = float(coef_str)
                    # Проверяем, не нулевой ли первый коэффициент
                    if check_coef(i, coef):
                        # Если все хорошо, то завершаем цикл
                        break
                    else:
                        # Если коэффициент нулевой и первый, то выводим сообщение
                        print("Первый коэффициент не может быть нулем!")
                except ValueError:
                    # Если не получилось, выводим сообщение
                    print("Ошибка: введите число!")
        # Добавляем коэффициент в список
        coefs.append(coef)
    
    # Возвращаем список
    return coefs

def get_discriminant(coefs:list[float]) -> float:
    '''
    Вычисляет дискриминант
    
    Args:
        coefs (list[float]): список коэффициентов
    
    Returns:
        float: дискриминант
    '''
    
    # Вычисляем дискриминант
    disctriminant = coefs[1]**2 - 4*coefs[0]*coefs[2]
    
    # Возвращаем дискриминант
    return disctriminant

def get_roots(coefs:list[float]) -> list[float]:
    '''
    Находит действительные корни уравнения с помощью дискриминанта
    
    Args:
        coefs (list[float]): список коэффициентов
    
    Returns:
        list[float]: список корней
    '''
    
    # Список корней
    roots = []
    
    # Проверяем, введены ли коэффициенты
    if len(coefs) != 3:
        # Если не введены, то выводим сообщение и завершаем работу функции
        print("Коэффициенты не введены")
        return
    
    # Вычисляем дискриминант
    disctriminant = get_discriminant(coefs)
    
    # Список временных корней до обратной замены
    temp_roots = []
    
    # Если дискриминант больше нуля, то добавляем два корня
    if disctriminant > 0:
        temp_roots.append((-coefs[1] + math.sqrt(disctriminant)) / (2*coefs[0]))
        temp_roots.append((-coefs[1] - math.sqrt(disctriminant)) / (2*coefs[0]))
    # Если дискриминант равен нулю, то добавляем один корень
    elif disctriminant == 0:
        temp_roots.append(-coefs[1] / (2*coefs[0]))
        
    # Производим обратную замену
    for temp_root in temp_roots:
        # Если до замены корень больше нуля, то добавляем его корень с разными знаками
        if temp_root > 0:
            roots.append(math.sqrt(temp_root))
            roots.append(-math.sqrt(temp_root))
        # Если до замены корень равен нулю, то добавляем его
        elif temp_root == 0:
            roots.append(0)
    
    # Сортируем корни и возвращаем  
    return sorted(roots)

def print_roots(roots:list[float]):
    '''
    Выводит корни уравнения
    
    Args:
        roots (list[float]): список корней
    '''
    
    # Проверяем, введены ли корни
    if len(roots) == 0:
        print("Корни не найдены")
        return
    
    # Выводим корни
    for i in range(len(roots)):
        print(f"Корень {i+1}: {roots[i]}")

def main():
    '''
    Главная функция
    '''
    
    # Получаем коэффициенты
    coefs = get_coefs()
    
    # Получаем корни
    roots = get_roots(coefs)
    
    # Выводим корни
    print_roots(roots)

# Если файл запущен напрямую
if __name__ == "__main__":
    main()