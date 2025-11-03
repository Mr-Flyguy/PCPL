import math
import sys

class BiEquation:
    '''
    Класс для решения биквадратного уравнения
    '''
    
    def __init__(self):
        '''
        Инициализирует объект класса
        '''
        # Список коэффициентов
        self.coefs = []
        
        # Список корней
        self.roots = []
        
        # Дискриминант 
        self.discriminant = None
        
    @staticmethod
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
        
    def get_coefs(self):
        '''
        Считывает коэффициенты из командной строки или с клавиатуры
        '''
        for i in range(3):
            try:
                # Пытаемся считать коэффициент из командной строки
                coef_str = sys.argv[i+1]
                # Пытаемся преобразовать в число
                coef = float(coef_str)
                # Проверяем, не нулевой ли первый коэффициент
                if not self.check_coef(i, coef):
                    # Если коэффициент нулевой и первый, то выводим сообщение
                    print(f"Первый коэффициент не может быть нулем! Используется интерактивный ввод.")
                    raise ValueError
            except:
                # Если не получилось, то коэффициент = None
                coef = None

            # Проверяем, не нулевой ли первый коэффициент
            if coef is None  or not self.check_coef(i, coef):
                # Выводим сообщение об ошибке
                print(f"Ошибка ввода коэффициента {i+1} из командной строки")
                while True:
                    try:
                        # Пытаемся считать коэффициент с клавиатуры
                        coef_str = input(f"Введите коэффициент {i+1}: ")
                        # Пытаемся преобразовать в число
                        coef = float(coef_str)
                        # Проверяем, не нулевой ли первый коэффициент
                        if self.check_coef(i, coef):
                            # Если все хорошо, то завершаем цикл
                            break
                        else:
                            # Если коэффициент нулевой и первый, то выводим сообщение
                            print("Первый коэффициент не может быть нулем!")
                    except ValueError:
                        # Если не получилось, выводим сообщение
                        print("Ошибка: введите число!")
            # Добавляем коэффициент в список
            self.coefs.append(coef)
    
    def get_discriminant(self):
        '''
        Вычисляет дискриминант
        '''
        # Вычисляем дискриминант
        self.disctriminant = self.coefs[1]**2 - 4*self.coefs[0]*self.coefs[2]
    
    def get_roots(self):
        '''
        Находит действительные корни уравнения с помощью дискриминанта
        '''
        # Проверяем, введены ли коэффициенты
        if len(self.coefs) != 3:
            # Если не введены, то выводим сообщение и завершаем работу функции
            print("Коэффициенты не введены")
            return
        
        # Вычисляем дискриминант
        self.get_discriminant()
        
        # Список временных корней до обратной замены
        temp_roots = []
        
        # Если дискриминант больше нуля, то добавляем два корня
        if self.disctriminant > 0:
            temp_roots.append((-self.coefs[1] + math.sqrt(self.disctriminant)) / (2*self.coefs[0]))
            temp_roots.append((-self.coefs[1] - math.sqrt(self.disctriminant)) / (2*self.coefs[0]))
        # Если дискриминант равен нулю, то добавляем один корень
        elif self.disctriminant == 0:
            temp_roots.append(-self.coefs[1] / (2*self.coefs[0]))
            
        # Производим обратную замену
        for temp_root in temp_roots:
            # Если до замены корень больше нуля, то добавляем его корень с разными знаками
            if temp_root > 0:
                self.roots.append(math.sqrt(temp_root))
                self.roots.append(-math.sqrt(temp_root))
            # Если до замены корень равен нулю, то добавляем его
            elif temp_root == 0:
                self.roots.append(0)
        
        # Сортируем корни
        self.roots.sort()
    
    def print_roots(self):
        '''
        Выводит корни уравнения
        '''
        # Проверяем, введены ли корни
        if len(self.roots) == 0:
            print("Корни не найдены")
            return
        
        # Выводим корни
        for i in range(len(self.roots)):
            print(f"Корень {i+1}: {self.roots[i]}")

def main():
    '''
    Главная функция
    '''
    # Создаем объект класса
    equation = BiEquation()
    # Получаем коэффициенты
    equation.get_coefs()
    # Получаем корни
    equation.get_roots()
    # Выводим корни
    equation.print_roots()
    
if __name__ == "__main__":
    main()