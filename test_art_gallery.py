import unittest
from prettytable import PrettyTable
from typing import List
import sys


from art_gallery import (
    Picture, Author,
    PictureRepository, AuthorRepository,
    PictureService, AuthorService,
    PictureFormatter, AuthorFormatter
)


class BeautifulTestResult(unittest.TextTestResult):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_results = []
        self.current_test_class = None
    
    def startTest(self, test):
        super().startTest(test)
        self.current_test_start = test
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_results.append({
            'class': test.__class__.__name__,
            'test': test._testMethodName,
            'status': '✓ PASS',
            'message': ''
        })
    
    def addError(self, test, err):
        super().addError(test, err)
        self.test_results.append({
            'class': test.__class__.__name__,
            'test': test._testMethodName,
            'status': '✗ ERROR',
            'message': str(err[1])
        })
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_results.append({
            'class': test.__class__.__name__,
            'test': test._testMethodName,
            'status': '✗ FAIL',
            'message': str(err[1])
        })
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_results.append({
            'class': test.__class__.__name__,
            'test': test._testMethodName,
            'status': '○ SKIP',
            'message': reason
        })
    
    def print_beautiful_results(self):
        print('\n' + '=' * 120)
        print('ИТОГОВЫЕ РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ'.center(120))
        print('=' * 120)
        
        test_classes = {}
        for result in self.test_results:
            class_name = result['class']
            if class_name not in test_classes:
                test_classes[class_name] = []
            test_classes[class_name].append(result)
        
        for class_name, tests in test_classes.items():
            print(f'\n{class_name}')
            print('-' * 120)
            
            table = PrettyTable()
            table.field_names = ['№', 'Название теста', 'Статус', 'Сообщение об ошибке']
            table.align['№'] = 'c'
            table.align['Название теста'] = 'l'
            table.align['Статус'] = 'c'
            table.align['Сообщение об ошибке'] = 'l'
            table.max_width['Название теста'] = 60
            table.max_width['Сообщение об ошибке'] = 40
            
            for idx, test in enumerate(tests, 1):
                test_name = test['test'].replace('test_', '').replace('_', ' ').capitalize()

                status = test['status']
                message = test['message'][:100] if test['message'] else '—'
                
                table.add_row([idx, test_name, status, message])
            
            print(table)

        print('\n' + '=' * 120)
        self._print_summary()
        print('=' * 120 + '\n')
    
    def _print_summary(self):
        total = len(self.test_results)
        passed = len([r for r in self.test_results if '✓ PASS' in r['status']])
        failed = len([r for r in self.test_results if '✗ FAIL' in r['status']])
        errors = len([r for r in self.test_results if '✗ ERROR' in r['status']])
        skipped = len([r for r in self.test_results if '○ SKIP' in r['status']])
        
        summary_table = PrettyTable()
        summary_table.field_names = ['Всего', 'Пройдено', 'Провалено', 'Ошибок', 'Пропущено', 'Успешность']
        
        success_rate = (passed / total * 100) if total > 0 else 0
        
        summary_table.add_row([
            total,
            f'{passed} ({passed/total*100:.1f}%)' if total > 0 else '0',
            f'{failed} ({failed/total*100:.1f}%)' if total > 0 else '0',
            f'{errors} ({errors/total*100:.1f}%)' if total > 0 else '0',
            f'{skipped} ({skipped/total*100:.1f}%)' if total > 0 else '0',
            f'{success_rate:.1f}%'
        ])
        
        print('\nСТАТИСТИКА')
        print(summary_table)
        
        if success_rate == 100:
            print('\nРЕЗУЛЬТАТ: ✓ Все тесты успешно пройдены'.center(120))
        elif success_rate >= 80:
            print('\nРЕЗУЛЬТАТ: ~ Большинство тестов пройдено, есть замечания'.center(120))
        else:
            print('\nРЕЗУЛЬТАТ: ✗ Требуется исправление критических ошибок'.center(120))


class BeautifulTestRunner(unittest.TextTestRunner):
    resultclass = BeautifulTestResult
    
    def run(self, test):
        print('\n' + '=' * 120)
        print('ЗАПУСК НАБОРА ТЕСТОВ'.center(120))
        print('=' * 120)
        print('\nПосле каждого теста нажимайте ENTER для продолжения\n')
        
        result = super().run(test)
        
        if hasattr(result, 'print_beautiful_results'):
            result.print_beautiful_results()
        
        return result

class TestPictureRepository(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print(f'\n{"=" * 80}')
        print(f'КЛАСС ТЕСТОВ: {cls.__name__}'.center(80))
        print(f'{"=" * 80}')
    
    def setUp(self):
        self.repo = PictureRepository()
        print(f'\n{"-" * 80}')
        print(f'► Тест: {self._testMethodName}')
        print(f'{"-" * 80}')
    
    def tearDown(self):
        print(f'\n{"─" * 80}')
        print(f'✓ Тест завершён: {self._testMethodName}')
        print(f'{"─" * 80}')
        input('\n[Нажмите ENTER для следующего теста]')
    
    def test_add_picture_assigns_correct_id(self):
        print('\nОписание: Проверяем, что репозиторий последовательно присваивает ID')
        
        picture1 = Picture(name='Мона Лиза', year=1503)
        picture2 = Picture(name='Звёздная ночь', year=1889)
        
        id1 = self.repo.add(picture1)
        id2 = self.repo.add(picture2)
        
        print('\nРезультат операций:')
        self._print_test_data([picture1, picture2])
        
        self.assertEqual(id1, 0, "Первая картина должна иметь ID = 0")
        self.assertEqual(id2, 1, "Вторая картина должна иметь ID = 1")
        self.assertEqual(picture1.id, 0, "ID должен быть присвоен объекту")
        self.assertEqual(picture2.id, 1, "ID должен быть присвоен объекту")
        
        print('\nПроверки:')
        print('  ✓ ID присваиваются последовательно (0, 1, 2...)')
        print('  ✓ ID сохраняется в объекте картины')
    
    def test_delete_picture_updates_ids(self):
        print('\nОписание: При удалении картины ID остальных должны пересчитаться')
        
        picture1 = Picture(name='Картина 1')
        picture2 = Picture(name='Картина 2')
        picture3 = Picture(name='Картина 3')
        
        self.repo.add(picture1)
        self.repo.add(picture2)
        self.repo.add(picture3)
        
        print('\nСостояние ДО удаления:')
        self._print_test_data(self.repo.get_all())
        
        success = self.repo.delete(1)
        
        print('\nСостояние ПОСЛЕ удаления картины с ID=1:')
        self._print_test_data(self.repo.get_all())
        
        self.assertTrue(success, "Удаление должно быть успешным")
        self.assertEqual(len(self.repo.get_all()), 2, "Должно остаться 2 картины")
        
        remaining_pictures = self.repo.get_all()
        self.assertEqual(remaining_pictures[0].id, 0, "Первая картина: ID=0")
        self.assertEqual(remaining_pictures[1].id, 1, "Третья картина стала второй: ID=1")
        self.assertEqual(remaining_pictures[1].name, 'Картина 3', "Это должна быть 'Картина 3'")
        
        print('\nПроверки:')
        print('  ✓ Картина с ID=1 удалена')
        print('  ✓ ID оставшихся картин пересчитаны')
        print('  ✓ Порядок картин сохранён')
    
    def test_find_by_price_range(self):
        print('\nОписание: Поиск картин в заданном диапазоне цен')
        
        self.repo.add(Picture(name='Дешёвая', price=1000))
        self.repo.add(Picture(name='Средняя', price=5000))
        self.repo.add(Picture(name='Дорогая', price=10000))
        self.repo.add(Picture(name='Неизвестная цена', price='Неизвестно'))
        
        print('\nВсе картины в базе:')
        self._print_test_data(self.repo.get_all())
        
        print('\nПараметры поиска: от 2000$ до 8000$')
        results = self.repo.find_by_price_range(2000, 8000)
        
        print('\nРезультаты поиска:')
        self._print_test_data(results)
        
        self.assertEqual(len(results), 1, "Должна найтись 1 картина")
        self.assertEqual(results[0].name, 'Средняя', "Должна найтись 'Средняя'")
        
        print('\nПроверки:')
        print('  ✓ Найдена 1 картина в диапазоне')
        print('  ✓ Картины с некорректной ценой отфильтрованы')
    
    def _print_test_data(self, pictures: List[Picture]):
        if not pictures:
            print('  (пусто)')
            return
        
        table = PrettyTable()
        table.field_names = ['ID', 'Название', 'Год', 'Цена']
        table.align['Название'] = 'l'
        table.align['ID'] = 'c'
        
        for pic in pictures:
            table.add_row([
                pic.id,
                pic.name,
                pic.year if hasattr(pic, 'year') else '—',
                f'{pic.price}$' if isinstance(pic.price, int) else pic.price
            ])
        
        print(table)


class TestPictureService(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print(f'\n{"=" * 80}')
        print(f'КЛАСС ТЕСТОВ: {cls.__name__}'.center(80))
        print(f'{"=" * 80}')
    
    def setUp(self):
        self.picture_repo = PictureRepository()
        self.author_repo = AuthorRepository()
        self.service = PictureService(self.picture_repo, self.author_repo)
        print(f'\n{"-" * 80}')
        print(f'► Тест: {self._testMethodName}')
        print(f'{"-" * 80}')
    
    def tearDown(self):
        print(f'\n{"─" * 80}')
        print(f'✓ Тест завершён: {self._testMethodName}')
        print(f'{"─" * 80}')
        input('\n[Нажмите ENTER для следующего теста]')
    
    def test_add_author_to_picture_creates_bidirectional_link(self):
        print('\nОписание: Связывание должно обновить списки как у картины, так и у автора')
        
        picture_id = self.service.create_picture(name='Мона Лиза')
        author = Author(surname='да Винчи', name='Леонардо')
        author_id = self.author_repo.add(author)
        
        print('\nСостояние ДО связывания:')
        self._print_relationship_status(picture_id, author_id)
        
        success = self.service.add_author_to_picture(picture_id, author_id)
        
        print('\nСостояние ПОСЛЕ связывания:')
        self._print_relationship_status(picture_id, author_id)
        
        self.assertTrue(success, "Операция должна быть успешной")
        
        picture = self.picture_repo.get_by_id(picture_id)
        self.assertIn(author_id, picture.authors_ids, "ID автора должен быть в списке авторов картины")
        self.assertEqual(picture.main_author_id, author_id, "Автор должен стать главным (первый)")
        
        author = self.author_repo.get_by_id(author_id)
        self.assertIn(picture_id, author.pictures_ids, "ID картины должен быть в списке картин автора")
        
        print('\nПроверки:')
        print('  ✓ Двусторонняя связь установлена')
        print('  ✓ Автор назначен главным')
    
    def test_add_author_to_picture_with_invalid_ids(self):
        print('\nОписание: При попытке связать несуществующие объекты должна быть ошибка')
        
        picture_id = self.service.create_picture(name='Картина')
        invalid_author_id = 999
        
        print(f'\nПопытка связать:')
        print(f'  Картина: ID={picture_id} (существует)')
        print(f'  Автор: ID={invalid_author_id} (НЕ существует)')
        
        success = self.service.add_author_to_picture(picture_id, invalid_author_id)
        
        self.assertFalse(success, "Операция должна завершиться неудачей")
        
        picture = self.picture_repo.get_by_id(picture_id)
        self.assertEqual(len(picture.authors_ids), 0, "У картины не должно быть авторов")
        
        print('\nРезультат: ✗ Операция корректно отклонена')
        print('\nПроверки:')
        print('  ✓ Метод вернул False')
        print('  ✓ Картина не изменилась')
    
    def test_second_author_does_not_become_main(self):
        print('\nОписание: При добавлении второго автора главный не должен меняться')
        
        picture_id = self.service.create_picture(name='Картина')
        
        author1 = Author(surname='Первый', name='Автор')
        author2 = Author(surname='Второй', name='Автор')
        
        author1_id = self.author_repo.add(author1)
        author2_id = self.author_repo.add(author2)
        
        self.service.add_author_to_picture(picture_id, author1_id)
        
        print('\nПосле добавления первого автора:')
        self._print_relationship_status(picture_id, author1_id)
        
        self.service.add_author_to_picture(picture_id, author2_id)
        
        print('\nПосле добавления второго автора:')
        self._print_relationship_status(picture_id, author2_id)
        
        picture = self.picture_repo.get_by_id(picture_id)
        self.assertEqual(len(picture.authors_ids), 2, "Должно быть 2 автора")
        self.assertEqual(picture.main_author_id, author1_id, "Главный автор — первый добавленный")
        self.assertNotEqual(picture.main_author_id, author2_id, "Второй автор не должен быть главным")
        
        print('\nПроверки:')
        print(f'  ✓ У картины 2 автора')
        print(f'  ✓ Главный автор: ID={author1_id} (первый)')
        print(f'  ✓ Второй автор не стал главным')
    
    def _print_relationship_status(self, picture_id: int, author_id: int):
        picture = self.picture_repo.get_by_id(picture_id)
        author = self.author_repo.get_by_id(author_id)
        
        table = PrettyTable()
        table.field_names = ['Тип', 'Объект', 'Связанные ID', 'Главный автор']
        table.align['Объект'] = 'l'
        table.align['Связанные ID'] = 'l'
        table.align['Тип'] = 'c'
        
        if picture:
            table.add_row([
                'Картина',
                f'{picture.name} (ID={picture.id})',
                f'Авторы: {picture.authors_ids}' if picture.authors_ids else 'Нет связей',
                f'ID={picture.main_author_id}' if picture.main_author_id != 'Неизвестно' else 'Не назначен'
            ])
        
        if author:
            table.add_row([
                'Автор',
                f'{author.surname} {author.name} (ID={author.id})',
                f'Картины: {author.pictures_ids}' if author.pictures_ids else 'Нет связей',
                '—'
            ])
        
        print(table)


class TestPictureFormatter(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print(f'\n{"=" * 80}')
        print(f'КЛАСС ТЕСТОВ: {cls.__name__}'.center(80))
        print(f'{"=" * 80}')
    
    def setUp(self):
        self.author_repo = AuthorRepository()
        self.formatter = PictureFormatter(self.author_repo)
        print(f'\n{"-" * 80}')
        print(f'► Тест: {self._testMethodName}')
        print(f'{"-" * 80}')
    
    def tearDown(self):
        print(f'\n{"─" * 80}')
        print(f'✓ Тест завершён: {self._testMethodName}')
        print(f'{"─" * 80}')
        input('\n[Нажмите ENTER для следующего теста]')
    
    def test_format_empty_list(self):
        """Тест: форматирование пустого списка"""
        print('\nОписание: Пустой список должен быть обработан корректно')
        
        pictures = []
        
        result = self.formatter.format_table(pictures, 'Тестовые картины')
        
        print('\nРезультат форматирования:')
        print(result)
        
        self.assertIn('не найдено', result, "Должно быть сообщение 'не найдено'")
        self.assertIn('Тестовые картины', result, "Должен быть заголовок")
        
        print('\nПроверки:')
        print('  ✓ Есть сообщение "не найдено"')
        print('  ✓ Заголовок отображается')
    
    def test_format_picture_with_author(self):
        """Тест: форматирование картины с автором"""
        print('\nОписание: Картина с автором должна отображаться полностью')
        
        author = Author(surname='Пикассо', name='Пабло')
        author_id = self.author_repo.add(author)
        
        picture = Picture(
            name='Герника',
            year=1937,
            price=200000,
            country='Испания',
            size='349x776 см',
            is_available=True,
            main_author_id=author_id
        )
        picture.id = 0
        
        result = self.formatter.format_table([picture], 'Картины Пикассо')
        
        print('\nОтформатированная таблица:')
        print(result)
        
        self.assertIn('Герника', result, "Должно быть название картины")
        self.assertIn('Пикассо Пабло', result, "Должно быть имя автора")
        self.assertIn('1937', result, "Должен быть год")
        self.assertIn('Испания', result, "Должна быть страна")
        self.assertIn('✓', result, "Должна быть галочка доступности")
        
        print('\nПроверки:')
        print('  ✓ Название картины отображено')
        print('  ✓ Имя автора получено по ID')
        print('  ✓ Все поля заполнены')
    
    def test_format_picture_with_unknown_author(self):
        print('\nОписание: Картина без автора должна отображать "Неизвестно"')
        
        picture = Picture(name='Неизвестная картина', main_author_id='Неизвестно')
        picture.id = 0
        
        result = self.formatter.format_table([picture])
        
        print('\nОтформатированная таблица:')
        print(result)
        
        self.assertIn('Неизвестно', result, "Автор должен быть 'Неизвестно'")
        self.assertIn('Неизвестная картина', result, "Должно быть название")
        
        print('\nПроверки:')
        print('  ✓ Название картины отображено')
        print('  ✓ Автор указан как "Неизвестно"')

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPictureRepository))
    suite.addTests(loader.loadTestsFromTestCase(TestPictureService))
    suite.addTests(loader.loadTestsFromTestCase(TestPictureFormatter))
    
    runner = BeautifulTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)