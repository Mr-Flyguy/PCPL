import unittest
from prettytable import PrettyTable
from typing import List
import sys
import random
import cowsay
import emoji
from art import text2art
from rich.console import Console
from rich.table import Table
from rich import box
import textwrap


from art_gallery import (
    Picture, Author,
    PictureRepository, AuthorRepository,
    PictureService, AuthorService,
    PictureFormatter, AuthorFormatter
)

console = Console()

ANIMALS = [
    "cow",
    "tux",
    "dragon",
    "turkey",
    "ghostbusters",
    "kitty",
    "stegosaurus",
]

MAX_COW_WIDTH = 55
MAX_LINES_IN_COW = 15
_animal_pool = []


def format_for_cowsay(message: str) -> str:
    wrapped_lines = []
    for line in message.splitlines():
        if not line.strip():
            wrapped_lines.append("")
            continue
        wrapped_lines.extend(textwrap.wrap(line, width=MAX_COW_WIDTH))
    if len(wrapped_lines) > MAX_LINES_IN_COW:
        wrapped_lines = wrapped_lines[:MAX_LINES_IN_COW - 1] + ["(continued...)"]
    return "\n".join(wrapped_lines)


def cowsay_random(message: str):
    global _animal_pool
    if not _animal_pool:
        _animal_pool = ANIMALS[:]
        random.shuffle(_animal_pool)
    animal = _animal_pool.pop()
    func = getattr(cowsay, animal, cowsay.cow)
    text = func(format_for_cowsay(message))
    print(text)


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
            'status': '✓ PASS ' + emoji.emojize(":check_mark_button:"),
            'message': ''
        })

    def addError(self, test, err):
        super().addError(test, err)
        self.test_results.append({
            'class': test.__class__.__name__,
            'test': test._testMethodName,
            'status': '✗ ERROR ' + emoji.emojize(":collision:"),
            'message': str(err[1])[:50]
        })

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_results.append({
            'class': test.__class__.__name__,
            'test': test._testMethodName,
            'status': '✗ FAIL ' + emoji.emojize(":cross_mark:"),
            'message': str(err[1])[:50]
        })

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_results.append({
            'class': test.__class__.__name__,
            'test': test._testMethodName,
            'status': '○ SKIP ' + emoji.emojize(":zzz:"),
            'message': reason[:50]
        })

    def print_beautiful_results(self):
        banner = text2art("TEST RESULTS", font='big')
        console.print(banner, style="bold cyan")

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

        self._print_summary()

    def _print_summary(self):
        total = len(self.test_results)
        passed = len([r for r in self.test_results if 'PASS' in r['status']])
        failed = len([r for r in self.test_results if 'FAIL' in r['status']])
        errors = len([r for r in self.test_results if 'ERROR' in r['status']])
        skipped = len([r for r in self.test_results if 'SKIP' in r['status']])

        success_rate = (passed / total * 100) if total > 0 else 0.0

        banner = text2art("STATISTICS", font='big')
        console.print("\n" + banner, style="bold magenta")

        table = Table(
            title="Статистика тестирования",
            box=box.ROUNDED,
            show_lines=True
        )
        table.add_column("Всего", justify="right", style="bold white")
        table.add_column("Пройдено", justify="right", style="bold green")
        table.add_column("Провалено", justify="right", style="bold red")
        table.add_column("Ошибок", justify="right", style="bold red")
        table.add_column("Пропущено", justify="right", style="bold yellow")
        table.add_column("Успешность", justify="right", style="bold cyan")

        def f_part(n):
            if total == 0:
                return "0"
            return f"{n} ({n/total*100:.1f}%)"

        table.add_row(
            str(total),
            f_part(passed),
            f_part(failed),
            f_part(errors),
            f_part(skipped),
            f"{success_rate:.1f}%"
        )

        console.print(table)

        if success_rate == 100:
            msg = text2art("ALL PASS!", font='small')
            console.print("\n" + msg, style="bold green")
            console.print("Все тесты успешно пройдены " + emoji.emojize(":party_popper:"), style="bold green")
        elif success_rate >= 80:
            msg = text2art("MOSTLY OK", font='small')
            console.print("\n" + msg, style="bold yellow")
            console.print("Большинство тестов пройдено " + emoji.emojize(":thinking_face:"), style="bold yellow")
        else:
            msg = text2art("NEEDS FIX", font='small')
            console.print("\n" + msg, style="bold red")
            console.print("Требуется исправление " + emoji.emojize(":skull:"), style="bold red")

        console.print("\n", style="bold")


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
        self.output_buffer = []
        self.output_buffer.append(f'Тест: {self._testMethodName}')

    def tearDown(self):
        cowsay_random('\n'.join(self.output_buffer))
        input('\n[Нажмите ENTER для следующего теста]')

    def test_add_picture_assigns_correct_id(self):
        self.output_buffer.append('Проверяем присваивание ID')

        picture1 = Picture(name='Мона Лиза', year=1503)
        picture2 = Picture(name='Звёздная ночь', year=1889)

        id1 = self.repo.add(picture1)
        id2 = self.repo.add(picture2)

        self.assertEqual(id1, 0)
        self.assertEqual(id2, 1)
        self.assertEqual(picture1.id, 0)
        self.assertEqual(picture2.id, 1)

        self.output_buffer.append('✓ ID присваиваются последовательно')
        self.output_buffer.append('✓ ID сохраняются в объекте')

    def test_delete_picture_updates_ids(self):
        self.output_buffer.append('При удалении пересчитываются ID')

        picture1 = Picture(name='Картина 1')
        picture2 = Picture(name='Картина 2')
        picture3 = Picture(name='Картина 3')

        self.repo.add(picture1)
        self.repo.add(picture2)
        self.repo.add(picture3)

        self.output_buffer.append(f'Было картин: {len(self.repo.get_all())}')

        success = self.repo.delete(1)

        self.output_buffer.append(f'Стало картин: {len(self.repo.get_all())}')

        self.assertTrue(success)
        self.assertEqual(len(self.repo.get_all()), 2)

        remaining_pictures = self.repo.get_all()
        self.assertEqual(remaining_pictures[0].id, 0)
        self.assertEqual(remaining_pictures[1].id, 1)
        self.assertEqual(remaining_pictures[1].name, 'Картина 3')

        self.output_buffer.append('✓ Удаление и пересчёт работает')

    def test_find_by_price_range(self):
        self.output_buffer.append('Поиск картин в диапазоне цен')

        self.repo.add(Picture(name='Дешёвая', price=1000))
        self.repo.add(Picture(name='Средняя', price=5000))
        self.repo.add(Picture(name='Дорогая', price=10000))

        results = self.repo.find_by_price_range(2000, 8000)

        self.output_buffer.append(f'Найдено: {len(results)}')

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Средняя')

        self.output_buffer.append('✓ Поиск работает корректно')


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
        self.output_buffer = []
        self.output_buffer.append(f'Тест: {self._testMethodName}')

    def tearDown(self):
        cowsay_random('\n'.join(self.output_buffer))
        input('\n[Нажмите ENTER для следующего теста]')

    def test_add_author_to_picture_creates_bidirectional_link(self):
        self.output_buffer.append('Двусторонняя связь автор-картина')

        picture_id = self.service.create_picture(name='Мона Лиза')
        author = Author(surname='да Винчи', name='Леонардо')
        author_id = self.author_repo.add(author)

        success = self.service.add_author_to_picture(picture_id, author_id)

        self.assertTrue(success)

        picture = self.picture_repo.get_by_id(picture_id)
        self.assertIn(author_id, picture.authors_ids)
        self.assertEqual(picture.main_author_id, author_id)

        author = self.author_repo.get_by_id(author_id)
        self.assertIn(picture_id, author.pictures_ids)

        self.output_buffer.append('✓ Связь установлена')
        self.output_buffer.append('✓ Автор главный')

    def test_add_author_to_picture_with_invalid_ids(self):
        self.output_buffer.append('Ошибка при несуществующем ID')

        picture_id = self.service.create_picture(name='Картина')
        invalid_author_id = 999

        success = self.service.add_author_to_picture(picture_id, invalid_author_id)

        self.assertFalse(success)

        picture = self.picture_repo.get_by_id(picture_id)
        self.assertEqual(len(picture.authors_ids), 0)

        self.output_buffer.append('✓ Ошибка корректна')

    def test_second_author_does_not_become_main(self):
        self.output_buffer.append('Второй автор не главный')

        picture_id = self.service.create_picture(name='Картина')

        author1 = Author(surname='Первый', name='Автор')
        author2 = Author(surname='Второй', name='Автор')

        author1_id = self.author_repo.add(author1)
        author2_id = self.author_repo.add(author2)

        self.service.add_author_to_picture(picture_id, author1_id)
        self.service.add_author_to_picture(picture_id, author2_id)

        picture = self.picture_repo.get_by_id(picture_id)
        self.assertEqual(len(picture.authors_ids), 2)
        self.assertEqual(picture.main_author_id, author1_id)
        self.assertNotEqual(picture.main_author_id, author2_id)

        self.output_buffer.append(f'✓ У картины {len(picture.authors_ids)} авторов')
        self.output_buffer.append('✓ Главный: первый')


class TestPictureFormatter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print(f'\n{"=" * 80}')
        print(f'КЛАСС ТЕСТОВ: {cls.__name__}'.center(80))
        print(f'{"=" * 80}')

    def setUp(self):
        self.author_repo = AuthorRepository()
        self.formatter = PictureFormatter(self.author_repo)
        self.output_buffer = []
        self.output_buffer.append(f'Тест: {self._testMethodName}')

    def tearDown(self):
        cowsay_random('\n'.join(self.output_buffer))
        input('\n[Нажмите ENTER для следующего теста]')

    def test_format_empty_list(self):
        self.output_buffer.append('Форматирование пустого списка')

        pictures = []
        result = self.formatter.format_table(pictures, 'Тестовые картины')

        self.assertIn('не найдено', result)
        self.assertIn('Тестовые картины', result)

        self.output_buffer.append('✓ Пустой список обработан')

    def test_format_picture_with_author(self):
        self.output_buffer.append('Форматирование с автором')

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

        self.assertIn('Герника', result)
        self.assertIn('Пикассо Пабло', result)
        self.assertIn('1937', result)

        self.output_buffer.append('✓ Картина отформатирована')
        self.output_buffer.append('✓ Автор получен по ID')

    def test_format_picture_with_unknown_author(self):
        self.output_buffer.append('Картина без автора')

        picture = Picture(name='Неизвестная картина', main_author_id='Неизвестно')
        picture.id = 0

        result = self.formatter.format_table([picture])

        self.assertIn('Неизвестно', result)
        self.assertIn('Неизвестная картина', result)

        self.output_buffer.append('✓ Автор: "Неизвестно"')


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestPictureRepository))
    suite.addTests(loader.loadTestsFromTestCase(TestPictureService))
    suite.addTests(loader.loadTestsFromTestCase(TestPictureFormatter))

    runner = BeautifulTestRunner(verbosity=0)
    result = runner.run(suite)

    sys.exit(0 if result.wasSuccessful() else 1)
