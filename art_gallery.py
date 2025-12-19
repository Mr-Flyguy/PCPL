from prettytable import PrettyTable
from typing import List, Dict, Any, Optional


class PictureRepository:
    def __init__(self):
        self._pictures: List['Picture'] = []
    
    def add(self, picture: 'Picture') -> int:
        picture.id = len(self._pictures)
        self._pictures.append(picture)
        return picture.id
    
    def get_by_id(self, picture_id: int) -> Optional['Picture']:
        if 0 <= picture_id < len(self._pictures):
            return self._pictures[picture_id]
        return None
    
    def delete(self, picture_id: int) -> bool:
        if 0 <= picture_id < len(self._pictures):
            self._pictures.pop(picture_id)
            self._update_ids()
            return True
        return False
    
    def get_all(self) -> List['Picture']:
        return self._pictures.copy()
    
    def find_by_name(self, name: str) -> List['Picture']:
        return [p for p in self._pictures if p.name == name]
    
    def find_by_country(self, country: str) -> List['Picture']:
        return [p for p in self._pictures if p.country == country]
    
    def find_by_year(self, year: int) -> List['Picture']:
        return [p for p in self._pictures if p.year == year]
    
    def find_by_price_range(self, from_price: int, to_price: int) -> List['Picture']:
        return [p for p in self._pictures if isinstance(p.price, int) and from_price <= p.price <= to_price]
    
    def find_by_author(self, author_id: int) -> List['Picture']:
        return [p for p in self._pictures if author_id in p.authors_ids]
    
    def clear(self):
        self._pictures.clear()
    
    def _update_ids(self):
        for i, picture in enumerate(self._pictures):
            picture.id = i


class AuthorRepository:
    def __init__(self):
        self._authors: List['Author'] = []
    
    def add(self, author: 'Author') -> int:
        author.id = len(self._authors)
        self._authors.append(author)
        return author.id
    
    def get_by_id(self, author_id: int) -> Optional['Author']:
        if 0 <= author_id < len(self._authors):
            return self._authors[author_id]
        return None
    
    def delete(self, author_id: int) -> bool:
        if 0 <= author_id < len(self._authors):
            self._authors.pop(author_id)
            self._update_ids()
            return True
        return False
    
    def get_all(self) -> List['Author']:
        return self._authors.copy()
    
    def find_by_name(self, name: str) -> List['Author']:
        return [a for a in self._authors if a.name == name]
    
    def find_by_surname(self, surname: str) -> List['Author']:
        return [a for a in self._authors if a.surname == surname]
    
    def find_by_year_range(self, from_year: int, to_year: int) -> List['Author']:
        return [a for a in self._authors if 
                (isinstance(a.birth_year, int) and from_year <= a.birth_year <= to_year) or
                (isinstance(a.death_year, int) and from_year <= a.death_year <= to_year)]
    
    def clear(self):
        self._authors.clear()
    
    def _update_ids(self):
        for i, author in enumerate(self._authors):
            author.id = i


class Picture:
    def __init__(self, 
                 name: str = 'Неизвестно',
                 authors_ids: List[int] = None,
                 main_author_id: Any = 'Неизвестно',
                 year: Any = 'Неизвестно',
                 price: Any = 'Неизвестно',
                 country: str = 'Неизвестно',
                 size: str = 'Неизвестно',
                 is_available: bool = False,
                 **kwargs):
        self.id: int = -1
        self.name = name
        self.authors_ids = authors_ids if authors_ids is not None else []
        self.main_author_id = main_author_id
        self.year = year
        self.price = price
        self.country = country
        self.size = size
        self.is_available = is_available
        self.additional_data = kwargs


class Author:
    def __init__(self,
                 surname: str = 'Неизвестно',
                 name: str = 'Неизвестно',
                 last_name: str = 'Неизвестно',
                 birth_year: Any = 'Неизвестно',
                 death_year: Any = 'Неизвестно',
                 pictures_ids: List[int] = None,
                 **kwargs):
        self.id: int = -1
        self.surname = surname
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.pictures_ids = pictures_ids if pictures_ids is not None else []
        self.additional_data = kwargs


class PictureService:
    def __init__(self, picture_repo: PictureRepository, author_repo: AuthorRepository):
        self.picture_repo = picture_repo
        self.author_repo = author_repo
    
    def create_picture(self, name: str = 'Неизвестно', year: Any = 'Неизвестно',
                      price: Any = 'Неизвестно', country: str = 'Неизвестно',
                      size: str = 'Неизвестно', is_available: bool = False,
                      **kwargs) -> int:
        picture = Picture(name=name, year=year, price=price, country=country,
                         size=size, is_available=is_available, **kwargs)
        return self.picture_repo.add(picture)
    
    def delete_picture(self, picture_id: int) -> bool:
        return self.picture_repo.delete(picture_id)
    
    def add_author_to_picture(self, picture_id: int, author_id: int) -> bool:
        picture = self.picture_repo.get_by_id(picture_id)
        author = self.author_repo.get_by_id(author_id)
        
        if picture is None or author is None:
            return False
        
        if author_id not in picture.authors_ids:
            picture.authors_ids.append(author_id)
        
        if picture_id not in author.pictures_ids:
            author.pictures_ids.append(picture_id)
        
        if len(picture.authors_ids) == 1:
            picture.main_author_id = author_id
        
        return True
    
    def set_main_author(self, picture_id: int, author_id: int) -> bool:
        picture = self.picture_repo.get_by_id(picture_id)
        author = self.author_repo.get_by_id(author_id)
        
        if picture is None or author is None:
            return False
        
        if author_id not in picture.authors_ids:
            picture.authors_ids.append(author_id)
        
        picture.main_author_id = author_id
        
        if picture_id not in author.pictures_ids:
            author.pictures_ids.append(picture_id)
        
        return True
    
    def get_pictures_by_author(self, surname: str, name: str) -> List[Picture]:
        authors = self.author_repo.find_by_surname(surname)
        if authors:
            author_id = authors[0].id
            return self.picture_repo.find_by_author(author_id)
        return []


class AuthorService:
    def __init__(self, author_repo: AuthorRepository, picture_repo: PictureRepository):
        self.author_repo = author_repo
        self.picture_repo = picture_repo
    
    def create_author(self, surname: str = 'Неизвестно', name: str = 'Неизвестно',
                     last_name: str = 'Неизвестно', birth_year: Any = 'Неизвестно',
                     death_year: Any = 'Неизвестно', **kwargs) -> int:
        author = Author(surname=surname, name=name, last_name=last_name,
                       birth_year=birth_year, death_year=death_year, **kwargs)
        return self.author_repo.add(author)
    
    def delete_author(self, author_id: int) -> bool:
        return self.author_repo.delete(author_id)
    
    def add_picture_to_author(self, author_id: int, picture_id: int) -> bool:
        author = self.author_repo.get_by_id(author_id)
        picture = self.picture_repo.get_by_id(picture_id)
        
        if author is None or picture is None:
            return False
        
        if picture_id not in author.pictures_ids:
            author.pictures_ids.append(picture_id)
        
        if author_id not in picture.authors_ids:
            picture.authors_ids.append(author_id)
        
        if len(picture.authors_ids) == 1:
            picture.main_author_id = author_id
        
        return True
    
    def get_authors_by_picture(self, picture_name: str) -> List[Author]:
        pictures = self.picture_repo.find_by_name(picture_name)
        if pictures:
            picture = pictures[0]
            result = []
            for author_id in picture.authors_ids:
                author = self.author_repo.get_by_id(author_id)
                if author is not None:
                    result.append(author)
            return result
        return []


class PictureFormatter:
    def __init__(self, author_repo: AuthorRepository):
        self.author_repo = author_repo
    
    def format_table(self, pictures: List[Picture], title: str = 'Картины') -> str:
        if not pictures:
            return f'\n{title}: не найдено'
        
        table = PrettyTable()
        table.field_names = ['ID', 'Название', 'Главный автор', 'Год', 'Цена ($)', 
                            'Страна', 'Размер', 'Доступна', 'Доп. данные']
        table.align['Название'] = 'l'
        table.align['Главный автор'] = 'l'
        table.align['Страна'] = 'l'
        table.align['Доп. данные'] = 'l'
        
        for picture in pictures:
            author_name = self._get_author_name(picture.main_author_id)
            additional = self._format_additional_data(picture.additional_data)
            
            table.add_row([
                picture.id,
                picture.name,
                author_name,
                picture.year,
                f'{picture.price:,}' if isinstance(picture.price, int) else picture.price,
                picture.country,
                picture.size,
                '✓' if picture.is_available else '✗',
                additional
            ])
        
        result = f'\n{"=" * 100}\n'
        result += f'{title} (найдено: {len(pictures)})\n'
        result += f'{"=" * 100}\n'
        result += str(table)
        return result
    
    def _get_author_name(self, author_id: Any) -> str:
        if isinstance(author_id, int):
            author = self.author_repo.get_by_id(author_id)
            if author:
                return f"{author.surname} {author.name}"
        return 'Неизвестно'
    
    def _format_additional_data(self, additional_data: Dict[str, Any]) -> str:
        if additional_data:
            return ', '.join([f"{k}: {v}" for k, v in additional_data.items()])
        return '-'


class AuthorFormatter:
    def format_table(self, authors: List[Author], title: str = 'Авторы') -> str:
        if not authors:
            return f'\n{title}: не найдено'
        
        table = PrettyTable()
        table.field_names = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Год рождения', 
                            'Год смерти', 'Картин', 'Доп. данные']
        table.align['Фамилия'] = 'l'
        table.align['Имя'] = 'l'
        table.align['Отчество'] = 'l'
        table.align['Доп. данные'] = 'l'
        
        for author in authors:
            additional = self._format_additional_data(author.additional_data)
            
            table.add_row([
                author.id,
                author.surname,
                author.name,
                author.last_name if author.last_name else '-',
                author.birth_year,
                author.death_year,
                len(author.pictures_ids),
                additional
            ])
        
        result = f'\n{"=" * 100}\n'
        result += f'{title} (найдено: {len(authors)})\n'
        result += f'{"=" * 100}\n'
        result += str(table)
        return result
    
    def _format_additional_data(self, additional_data: Dict[str, Any]) -> str:
        if additional_data:
            return ', '.join([f"{k}: {v}" for k, v in additional_data.items()])
        return '-'


class ConsoleUI:
    def __init__(self, 
                 picture_service: PictureService,
                 author_service: AuthorService,
                 picture_repo: PictureRepository,
                 author_repo: AuthorRepository,
                 picture_formatter: PictureFormatter,
                 author_formatter: AuthorFormatter):
        self.picture_service = picture_service
        self.author_service = author_service
        self.picture_repo = picture_repo
        self.author_repo = author_repo
        self.picture_formatter = picture_formatter
        self.author_formatter = author_formatter
    
    def run(self):
        while True:
            self._print_menu()
            try:
                choice = int(input('\nВыберите действие: '))
            except ValueError:
                print('Ошибка: введите число!')
                continue
            
            if choice == 0:
                print('\nAdios!')
                break
            
            self._handle_choice(choice)
    
    def _print_menu(self):
        print('\n' + '=' * 80)
        print('МЕНЮ'.center(80))
        print('=' * 80)
        print('┌─ КАРТИНЫ ─────────────────────────┐')
        print('│ 1  - Показать все картины         │')
        print('│ 2  - Добавить картину             │')
        print('│ 3  - Удалить картину              │')
        print('│ 4  - Назначить автора картине     │')
        print('│ 5  - Найти по названию            │')
        print('│ 6  - Найти по стране              │')
        print('│ 7  - Найти по году                │')
        print('│ 8  - Найти по цене                │')
        print('│ 9  - Найти по автору              │')
        print('└───────────────────────────────────┘')
        print('┌─ АВТОРЫ ──────────────────────────┐')
        print('│ 10 - Показать всех авторов        │')
        print('│ 11 - Добавить автора              │')
        print('│ 12 - Удалить автора               │')
        print('│ 13 - Назначить картину автору     │')
        print('│ 14 - Найти по имени               │')
        print('│ 15 - Найти по фамилии             │')
        print('│ 16 - Найти по году жизни          │')
        print('│ 17 - Найти по картине             │')
        print('└───────────────────────────────────┘')
        print('│ 0  - Выход                        │')
        print('└───────────────────────────────────┘')
    
    def _handle_choice(self, choice: int):
        handlers = {
            1: self._show_all_pictures,
            2: self._add_picture,
            3: self._delete_picture,
            4: self._assign_author_to_picture,
            5: self._find_pictures_by_name,
            6: self._find_pictures_by_country,
            7: self._find_pictures_by_year,
            8: self._find_pictures_by_price,
            9: self._find_pictures_by_author,
            10: self._show_all_authors,
            11: self._add_author,
            12: self._delete_author,
            13: self._assign_picture_to_author,
            14: self._find_authors_by_name,
            15: self._find_authors_by_surname,
            16: self._find_authors_by_year,
            17: self._find_authors_by_picture,
        }
        
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print('Неверный выбор! Выберите число от 0 до 17.')
    
    def _show_all_pictures(self):
        pictures = self.picture_repo.get_all()
        print(self.picture_formatter.format_table(pictures, 'Все картины'))
    
    def _add_picture(self):
        print('\nДобавление новой картины')
        name = input('Название: ')
        year = input('Год: ')
        year = int(year) if year.isdigit() else year
        price = input('Цена ($): ')
        price = int(price) if price.isdigit() else price
        country = input('Страна: ')
        size = input('Размер: ')
        is_available = input('В наличии? (да/нет): ').lower() in ['да', 'yes', 'y', 'д']
        
        kwargs = {}
        while True:
            add_more = input('Добавить дополнительное поле? (да/нет): ').lower()
            if add_more in ['да', 'yes', 'y', 'д']:
                key = input('Название поля: ')
                value = input('Значение: ')
                kwargs[key] = value
            else:
                break
        
        picture_id = self.picture_service.create_picture(
            name=name, year=year, price=price, country=country,
            size=size, is_available=is_available, **kwargs
        )
        
        if self.author_repo.get_all():
            add_authors = input('Добавить авторов к картине? (да/нет): ').lower()
            if add_authors in ['да', 'yes', 'y', 'д']:
                authors = self.author_repo.get_all()
                print(self.author_formatter.format_table(authors, 'Список авторов'))
                while True:
                    try:
                        auth_id = input('ID автора (или "стоп" для завершения): ')
                        if auth_id.lower() in ['стоп', 'stop', 'нет', 'no']:
                            break
                        auth_id = int(auth_id)
                        self.picture_service.add_author_to_picture(picture_id, auth_id)
                        print(f'Автор с ID {auth_id} добавлен!')
                    except ValueError:
                        print('Ошибка: введите число!')
        
        print('Картина добавлена!')
    
    def _delete_picture(self):
        pictures = self.picture_repo.get_all()
        print(self.picture_formatter.format_table(pictures, 'Список картин'))
        try:
            picture_id = int(input('\nВведите ID картины для удаления: '))
            if self.picture_service.delete_picture(picture_id):
                print('Картина удалена!')
            else:
                print('Картина с таким ID не найдена!')
        except ValueError:
            print('Ошибка: введите число!')
    
    def _assign_author_to_picture(self):
        pictures = self.picture_repo.get_all()
        print(self.picture_formatter.format_table(pictures, 'Список картин'))
        try:
            pic_id = int(input('ID картины: '))
            authors = self.author_repo.get_all()
            print(self.author_formatter.format_table(authors, 'Список авторов'))
            auth_id = int(input('ID автора: '))
            self.picture_service.add_author_to_picture(pic_id, auth_id)
            print('Автор добавлен картине!')
        except ValueError:
            print('Ошибка: введите число!')
    
    def _find_pictures_by_name(self):
        name = input('\nВведите название картины: ')
        pictures = self.picture_repo.find_by_name(name)
        print(self.picture_formatter.format_table(pictures, f'Результаты поиска: "{name}"'))
    
    def _find_pictures_by_country(self):
        country = input('\nВведите страну: ')
        pictures = self.picture_repo.find_by_country(country)
        print(self.picture_formatter.format_table(pictures, f'Картины из страны: {country}'))
    
    def _find_pictures_by_year(self):
        try:
            year = int(input('\nВведите год: '))
            pictures = self.picture_repo.find_by_year(year)
            print(self.picture_formatter.format_table(pictures, f'Картины {year} года'))
        except ValueError:
            print('Ошибка: введите число!')
    
    def _find_pictures_by_price(self):
        try:
            from_price = int(input('\nЦена от ($): '))
            to_price = int(input('Цена до ($): '))
            pictures = self.picture_repo.find_by_price_range(from_price, to_price)
            print(self.picture_formatter.format_table(
                pictures, f'Картины в диапазоне ${from_price:,} - ${to_price:,}'
            ))
        except ValueError:
            print('Ошибка: введите число!')
    
    def _find_pictures_by_author(self):
        print('\nПоиск картин по автору')
        surname = input('Фамилия автора: ')
        name = input('Имя автора: ')
        pictures = self.picture_service.get_pictures_by_author(surname, name)
        print(self.picture_formatter.format_table(
            pictures, f'Картины автора: {surname} {name}'
        ))
    
    def _show_all_authors(self):
        authors = self.author_repo.get_all()
        print(self.author_formatter.format_table(authors, 'Все авторы'))
    
    def _add_author(self):
        print('\nДобавление нового автора')
        surname = input('Фамилия: ')
        name = input('Имя: ')
        last_name = input('Отчество: ')
        birth_year = input('Год рождения: ')
        birth_year = int(birth_year) if birth_year.isdigit() else birth_year
        death_year = input('Год смерти: ')
        death_year = int(death_year) if death_year.isdigit() else death_year
        
        kwargs = {}
        while True:
            add_more = input('Добавить дополнительное поле? (да/нет): ').lower()
            if add_more in ['да', 'yes', 'y', 'д']:
                key = input('Название поля: ')
                value = input('Значение: ')
                kwargs[key] = value
            else:
                break
        
        author_id = self.author_service.create_author(
            surname=surname, name=name, last_name=last_name,
            birth_year=birth_year, death_year=death_year, **kwargs
        )
        
        if self.picture_repo.get_all():
            add_pictures = input('Добавить картины автору? (да/нет): ').lower()
            if add_pictures in ['да', 'yes', 'y', 'д']:
                pictures = self.picture_repo.get_all()
                print(self.picture_formatter.format_table(pictures, 'Список картин'))
                while True:
                    try:
                        pic_id = input('ID картины (или "стоп" для завершения): ')
                        if pic_id.lower() in ['стоп', 'stop', 'нет', 'no']:
                            break
                        pic_id = int(pic_id)
                        self.author_service.add_picture_to_author(author_id, pic_id)
                        print(f'Картина с ID {pic_id} добавлена!')
                    except ValueError:
                        print('Ошибка: введите число!')
        
        print('Автор добавлен!')
    
    def _delete_author(self):
        authors = self.author_repo.get_all()
        print(self.author_formatter.format_table(authors, 'Список авторов'))
        try:
            author_id = int(input('\nВведите ID автора для удаления: '))
            if self.author_service.delete_author(author_id):
                print('Автор удален!')
            else:
                print('Автор с таким ID не найден!')
        except ValueError:
            print('Ошибка: введите число!')
    
    def _assign_picture_to_author(self):
        authors = self.author_repo.get_all()
        print(self.author_formatter.format_table(authors, 'Список авторов'))
        try:
            auth_id = int(input('ID автора: '))
            pictures = self.picture_repo.get_all()
            print(self.picture_formatter.format_table(pictures, 'Список картин'))
            pic_id = int(input('ID картины: '))
            self.author_service.add_picture_to_author(auth_id, pic_id)
            print('Картина добавлена автору!')
        except ValueError:
            print('Ошибка: введите число!')
    
    def _find_authors_by_name(self):
        name = input('\nВведите имя автора: ')
        authors = self.author_repo.find_by_name(name)
        print(self.author_formatter.format_table(authors, f'Результаты поиска: "{name}"'))
    
    def _find_authors_by_surname(self):
        surname = input('\nВведите фамилию автора: ')
        authors = self.author_repo.find_by_surname(surname)
        print(self.author_formatter.format_table(authors, f'Результаты поиска: "{surname}"'))
    
    def _find_authors_by_year(self):
        try:
            from_year = int(input('\nГод от: '))
            to_year = int(input('Год до: '))
            authors = self.author_repo.find_by_year_range(from_year, to_year)
            print(self.author_formatter.format_table(authors, f'Авторы {from_year}-{to_year} гг.'))
        except ValueError:
            print('Ошибка: введите число!')
    
    def _find_authors_by_picture(self):
        name = input('\nВведите название картины: ')
        authors = self.author_service.get_authors_by_picture(name)
        print(self.author_formatter.format_table(authors, f'Авторы картины: "{name}"'))


def create_app() -> ConsoleUI:
    picture_repo = PictureRepository()
    author_repo = AuthorRepository()
    picture_service = PictureService(picture_repo, author_repo)
    author_service = AuthorService(author_repo, picture_repo)
    picture_formatter = PictureFormatter(author_repo)
    author_formatter = AuthorFormatter()
    
    return ConsoleUI(
        picture_service=picture_service,
        author_service=author_service,
        picture_repo=picture_repo,
        author_repo=author_repo,
        picture_formatter=picture_formatter,
        author_formatter=author_formatter
    )


def seed_data(picture_service: PictureService, author_service: AuthorService):
    picture_service.create_picture(
        name='Мона Лиза', year=1503, price=570000, 
        country='Италия', size='77x53 см', is_available=True, техника='Масло'
    )
    picture_service.create_picture(
        name='Звёздная ночь', year=1889, price=80000,
        country='Нидерланды', size='73x92 см', техника='Масло'
    )
    picture_service.create_picture(
        name='Девятый вал', year=1850, price=123000,
        country='Россия', size='221x332 см', is_available=True, техника='Масло'
    )
    picture_service.create_picture(
        name='Сотворение Адама', year=1512, price=10000,
        country='Италия', size='280x570 см', is_available=True, техника='Фреска'
    )
    picture_service.create_picture(
        name='Чёрный квадрат', year=1915, price=19000,
        country='Россия', size='79x79 см', стиль='Супрематизм'
    )
    
    author_service.create_author(
        surname='да Винчи', name='Леонардо', last_name='',
        birth_year=1452, death_year=1519, страна='Италия'
    )
    author_service.create_author(
        surname='ван Гог', name='Винсент', last_name='',
        birth_year=1853, death_year=1890, страна='Нидерланды'
    )
    author_service.create_author(
        surname='Айвазовский', name='Иван', last_name='Константинович',
        birth_year=1817, death_year=1900, страна='Россия'
    )
    author_service.create_author(
        surname='Буонарроти', name='Микеланджело', last_name='',
        birth_year=1475, death_year=1564, страна='Италия'
    )
    author_service.create_author(
        surname='Малевич', name='Казимир', last_name='Северинович',
        birth_year=1879, death_year=1935, страна='Россия'
    )
    
    for i in range(5):
        picture_service.add_author_to_picture(i, i)


if __name__ == '__main__':
    app = create_app()
    seed_data(app.picture_service, app.author_service)
    app.run()
