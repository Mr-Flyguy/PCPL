from prettytable import PrettyTable
class Picture:
    pictures = []


    def __init__(self, name='Неизвестно', authors_IDs=[], main_author_ID='Неизвестно', year='Неизвестно', price='Неизвестно', contry='Неизвестно', size='Неизвестно', is_avalible=False, **kwargs):
        self.id = len(Picture.pictures)
        self.name = name
        self.authors_IDs = authors_IDs if isinstance(authors_IDs, list) else []
        self.main_author_ID = main_author_ID
        self.year = year
        self.price = price
        self.contry = contry
        self.size = size
        self.is_avalible = is_avalible
        self.additional_data = {}
        for key, value in kwargs.items():
            self.additional_data[key] = value
        Picture.pictures.append(self)
    
    @staticmethod
    def update_IDs():
        for i in range(len(Picture.pictures)):
            Picture.pictures[i].id = i


    @staticmethod
    def add_picture(name='Неизвестно', authors_IDs=[], main_author_ID='Неизвестно', year='Неизвестно', price='Неизвестно', contry='Неизвестно', size='Неизвестно', is_avalible=False, **kwargs):
        Picture(name=name, authors_IDs=authors_IDs, main_author_ID=main_author_ID, year=year, price=price, contry=contry, size=size, is_avalible=is_avalible, **kwargs)
    
    @staticmethod
    def delete_picture(id):
        if 0 <= id < len(Picture.pictures):
            Picture.pictures.pop(id)
            Picture.update_IDs()
            return True
        return False


    @staticmethod
    def get_all_pictures():
        return Picture.pictures


    @staticmethod
    def get_by_name(name):
        return [picture for picture in Picture.pictures if picture.name == name]


    @staticmethod
    def get_by_country(country):
        return [picture for picture in Picture.pictures if picture.contry == country]


    @staticmethod
    def get_by_year(year):
        return [picture for picture in Picture.pictures if picture.year == year]


    @staticmethod
    def get_by_price(from_price, to_price):
        return [picture for picture in Picture.pictures if isinstance(picture.price, int) and from_price <= picture.price <= to_price]


    @staticmethod
    def get_by_author(surname, name):
        authors = Author.get_by_surname(surname)
        if authors:
            author_id = authors[0].id
            return [picture for picture in Picture.pictures if author_id in picture.authors_IDs]
        return []


    @staticmethod
    def add_author_to_picture(picture_id, author_id):
        if 0 <= picture_id < len(Picture.pictures) and 0 <= author_id < len(Author.authors):
            picture = Picture.pictures[picture_id]
            author = Author.authors[author_id]
            if author_id not in picture.authors_IDs:
                picture.authors_IDs.append(author_id)
            if picture_id not in author.pictures_IDs:
                author.pictures_IDs.append(picture_id)
            if len(picture.authors_IDs) == 1:
                picture.main_author_ID = author_id


    @staticmethod
    def set_main_author(picture_id, author_id):
        if 0 <= picture_id < len(Picture.pictures) and 0 <= author_id < len(Author.authors):
            picture = Picture.pictures[picture_id]
            if author_id not in picture.authors_IDs:
                picture.authors_IDs.append(author_id)
            picture.main_author_ID = author_id
            author = Author.authors[author_id]
            if picture_id not in author.pictures_IDs:
                author.pictures_IDs.append(picture_id)


class Author:
    authors = []


    def __init__(self, surname='Неизвестно', name='Неизвестно', last_name='Неизвестно', birth_year='Неизвестно', death_year='Неизвестно', pictures_IDs=[], **kwargs):
        self.id = len(Author.authors)
        self.surname = surname
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year
        self.death_year = death_year
        self.pictures_IDs = pictures_IDs if isinstance(pictures_IDs, list) else []
        self.additional_data = {}
        for key, value in kwargs.items():
            self.additional_data[key] = value
        Author.authors.append(self)
    
    @staticmethod
    def update_IDs():
        for i in range(len(Author.authors)):
            Author.authors[i].id = i


    @staticmethod
    def add_author(surname='Неизвестно', name='Неизвестно', last_name='Неизвестно', birth_year='Неизвестно', death_year='Неизвестно', pictures_IDs=[], **kwargs):
        Author(surname=surname, name=name, last_name=last_name, birth_year=birth_year, death_year=death_year, pictures_IDs=pictures_IDs, **kwargs)
    
    @staticmethod
    def delete_author(id):
        if 0 <= id < len(Author.authors):
            Author.authors.pop(id)
            Author.update_IDs()
            return True
        return False


    @staticmethod
    def get_all_authors():
        return Author.authors


    @staticmethod
    def get_by_name(name):
        return [author for author in Author.authors if author.name == name]


    @staticmethod
    def get_by_surname(surname):
        return [author for author in Author.authors if author.surname == surname]


    @staticmethod
    def get_by_year(from_year, to_year):
        return [author for author in Author.authors if 
                (isinstance(author.birth_year, int) and from_year <= author.birth_year <= to_year) or
                (isinstance(author.death_year, int) and from_year <= author.death_year <= to_year)]


    @staticmethod
    def get_by_picture(name):
        pictures = Picture.get_by_name(name)
        if pictures:
            picture = pictures[0]
            result = []
            for author_id in picture.authors_IDs:
                if isinstance(author_id, int) and 0 <= author_id < len(Author.authors):
                    result.append(Author.authors[author_id])
            return result
        return []


    @staticmethod
    def add_picture_to_author(author_id, picture_id):
        if 0 <= author_id < len(Author.authors) and 0 <= picture_id < len(Picture.pictures):
            author = Author.authors[author_id]
            picture = Picture.pictures[picture_id]
            if picture_id not in author.pictures_IDs:
                author.pictures_IDs.append(picture_id)
            if author_id not in picture.authors_IDs:
                picture.authors_IDs.append(author_id)
            if len(picture.authors_IDs) == 1:
                picture.main_author_ID = author_id


def print_pictures_table(pictures, title='Картины'):
    if not pictures:
        print(f'\n{title}: не найдено')
        return
    table = PrettyTable()
    table.field_names = ['ID', 'Название', 'Главный автор', 'Год', 'Цена ($)', 'Страна', 'Размер', 'Доступна', 'Доп. данные']
    table.align['Название'] = 'l'
    table.align['Главный автор'] = 'l'
    table.align['Страна'] = 'l'
    table.align['Доп. данные'] = 'l'
    for picture in pictures:
        if isinstance(picture.main_author_ID, int) and 0 <= picture.main_author_ID < len(Author.authors):
            author = Author.authors[picture.main_author_ID]
            author_name = f"{author.surname} {author.name}"
        else:
            author_name = 'Неизвестно'
        additional = ', '.join([f"{k}: {v}" for k, v in picture.additional_data.items()]) if picture.additional_data else '-'
        table.add_row([
            picture.id,
            picture.name,
            author_name,
            picture.year,
            f'{picture.price:,}' if isinstance(picture.price, int) else picture.price,
            picture.contry,
            picture.size,
            '✓' if picture.is_avalible else '✗',
            additional
        ])
    print(f'\n{"=" * 100}')
    print(f'{title} (найдено: {len(pictures)})')
    print(f'{"=" * 100}')
    print(table)


def print_authors_table(authors, title='Авторы'):
    if not authors:
        print(f'\n{title}: не найдено')
        return
    table = PrettyTable()
    table.field_names = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Год рождения', 'Год смерти', 'Картин', 'Доп. данные']
    table.align['Фамилия'] = 'l'
    table.align['Имя'] = 'l'
    table.align['Отчество'] = 'l'
    table.align['Доп. данные'] = 'l'
    for author in authors:
        additional = ', '.join([f"{k}: {v}" for k, v in author.additional_data.items()]) if author.additional_data else '-'
        table.add_row([
            author.id,
            author.surname,
            author.name,
            author.last_name if author.last_name else '-',
            author.birth_year,
            author.death_year,
            len(author.pictures_IDs),
            additional
        ])
    print(f'\n{"=" * 100}')
    print(f'{title} (найдено: {len(authors)})')
    print(f'{"=" * 100}')
    print(table)


def beautiful_request():
    while True:
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
        try:
            choice = int(input('\nВыберите действие: '))
        except ValueError:
            print('Ошибка: введите число!')
            continue


        if choice == 1:
            print_pictures_table(Picture.get_all_pictures(), 'Все картины')
        elif choice == 2:
            print('\nДобавление новой картины')
            name = input('Название: ')
            year = input('Год: ')
            year = int(year) if year.isdigit() else year
            price = input('Цена ($): ')
            price = int(price) if price.isdigit() else price
            country = input('Страна: ')
            size = input('Размер: ')
            is_avalible = input('В наличии? (да/нет): ').lower() in ['да', 'yes', 'y', 'д']
            kwargs = {}
            while True:
                add_more = input('Добавить дополнительное поле? (да/нет): ').lower()
                if add_more in ['да', 'yes', 'y', 'д']:
                    key = input('Название поля: ')
                    value = input('Значение: ')
                    kwargs[key] = value
                else:
                    break
            Picture.add_picture(name=name, year=year, price=price, contry=country, size=size, is_avalible=is_avalible, **kwargs)
            new_picture_id = len(Picture.pictures) - 1
            if Author.authors:
                add_authors = input('Добавить авторов к картине? (да/нет): ').lower()
                if add_authors in ['да', 'yes', 'y', 'д']:
                    print_authors_table(Author.get_all_authors(), 'Список авторов')
                    while True:
                        try:
                            auth_id = input('ID автора (или "стоп" для завершения): ')
                            if auth_id.lower() in ['стоп', 'stop', 'нет', 'no']:
                                break
                            auth_id = int(auth_id)
                            Picture.add_author_to_picture(new_picture_id, auth_id)
                            print(f'Автор с ID {auth_id} добавлен!')
                        except ValueError:
                            print('Ошибка: введите число!')
            print('Картина добавлена!')
        elif choice == 3:
            print_pictures_table(Picture.get_all_pictures(), 'Список картин')
            try:
                id = int(input('\nВведите ID картины для удаления: '))
                if Picture.delete_picture(id):
                    print('Картина удалена!')
                else:
                    print('Картина с таким ID не найдена!')
            except ValueError:
                print('Ошибка: введите число!')
        elif choice == 4:
            print_pictures_table(Picture.get_all_pictures(), 'Список картин')
            try:
                pic_id = int(input('ID картины: '))
                print_authors_table(Author.get_all_authors(), 'Список авторов')
                auth_id = int(input('ID автора: '))
                Picture.add_author_to_picture(pic_id, auth_id)
                print('Автор добавлен картине!')
            except ValueError:
                print('Ошибка: введите число!')
        elif choice == 5:
            name = input('\nВведите название картины: ')
            print_pictures_table(Picture.get_by_name(name), f'Результаты поиска: "{name}"')
        elif choice == 6:
            country = input('\nВведите страну: ')
            print_pictures_table(Picture.get_by_country(country), f'Картины из страны: {country}')
        elif choice == 7:
            try:
                year = int(input('\nВведите год: '))
                print_pictures_table(Picture.get_by_year(year), f'Картины {year} года')
            except ValueError:
                print('Ошибка: введите число!')
        elif choice == 8:
            try:
                from_price = int(input('\nЦена от ($): '))
                to_price = int(input('Цена до ($): '))
                print_pictures_table(Picture.get_by_price(from_price, to_price),
                                    f'Картины в диапазоне ${from_price:,} - ${to_price:,}')
            except ValueError:
                print('Ошибка: введите число!')
        elif choice == 9:
            print('\nПоиск картин по автору')
            surname = input('Фамилия автора: ')
            name = input('Имя автора: ')
            print_pictures_table(Picture.get_by_author(surname, name),
                               f'Картины автора: {surname} {name}')
        elif choice == 10:
            print_authors_table(Author.get_all_authors(), 'Все авторы')
        elif choice == 11:
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
            Author.add_author(surname=surname, name=name, last_name=last_name,
                            birth_year=birth_year, death_year=death_year, **kwargs)
            new_author_id = len(Author.authors) - 1
            if Picture.pictures:
                add_pictures = input('Добавить картины автору? (да/нет): ').lower()
                if add_pictures in ['да', 'yes', 'y', 'д']:
                    print_pictures_table(Picture.get_all_pictures(), 'Список картин')
                    while True:
                        try:
                            pic_id = input('ID картины (или "стоп" для завершения): ')
                            if pic_id.lower() in ['стоп', 'stop', 'нет', 'no']:
                                break
                            pic_id = int(pic_id)
                            Author.add_picture_to_author(new_author_id, pic_id)
                            print(f'Картина с ID {pic_id} добавлена!')
                        except ValueError:
                            print('Ошибка: введите число!')
            print('Автор добавлен!')
        elif choice == 12:
            print_authors_table(Author.get_all_authors(), 'Список авторов')
            try:
                id = int(input('\nВведите ID автора для удаления: '))
                if Author.delete_author(id):
                    print('Автор удален!')
                else:
                    print('Автор с таким ID не найден!')
            except ValueError:
                print('Ошибка: введите число!')
        elif choice == 13:
            print_authors_table(Author.get_all_authors(), 'Список авторов')
            try:
                auth_id = int(input('ID автора: '))
                print_pictures_table(Picture.get_all_pictures(), 'Список картин')
                pic_id = int(input('ID картины: '))
                Author.add_picture_to_author(auth_id, pic_id)
                print('Картина добавлена автору!')
            except ValueError:
                print('Ошибка: введите число!')
        elif choice == 14:
            name = input('\nВведите имя автора: ')
            print_authors_table(Author.get_by_name(name), f'Результаты поиска: "{name}"')
        elif choice == 15:
            surname = input('\nВведите фамилию автора: ')
            print_authors_table(Author.get_by_surname(surname), f'Результаты поиска: "{surname}"')
        elif choice == 16:
            try:
                from_year = int(input('\nГод от: '))
                to_year = int(input('Год до: '))
                print_authors_table(Author.get_by_year(from_year, to_year),
                                  f'Авторы {from_year}-{to_year} гг.')
            except ValueError:
                print('Ошибка: введите число!')
        elif choice == 17:
            name = input('\nВведите название картины: ')
            print_authors_table(Author.get_by_picture(name), f'Авторы картины: "{name}"')
        elif choice == 0:
            print('\nAdios!')
            break
        else:
            print('Неверный выбор! Выберите число от 0 до 17.')


if __name__ == '__main__':
    Picture.add_picture(name='Мона Лиза', year=1503, price=570000, contry='Италия', size='77x53 см', is_avalible=True, техника='Масло')
    Picture.add_picture(name='Звёздная ночь', year=1889, price=80000, contry='Нидерланды', size='73x92 см', техника='Масло')
    Picture.add_picture(name='Девятый вал', year=1850, price=123000, contry='Россия', size='221x332 см', is_avalible=True, техника='Масло')
    Picture.add_picture(name='Сотворение Адама', year=1512, price=10000, contry='Италия', size='280x570 см', is_avalible=True, техника='Фреска')
    Picture.add_picture(name='Чёрный квадрат', year=1915, price=19000, contry='Россия', size='79x79 см', стиль='Супрематизм')


    Author.add_author(surname='да Винчи', name='Леонардо', last_name='', birth_year=1452, death_year=1519, страна='Италия')
    Author.add_author(surname='ван Гог', name='Винсент', last_name='', birth_year=1853, death_year=1890, страна='Нидерланды')
    Author.add_author(surname='Айвазовский', name='Иван', last_name='Константинович', birth_year=1817, death_year=1900, страна='Россия')
    Author.add_author(surname='Буонарроти', name='Микеланджело', last_name='', birth_year=1475, death_year=1564, страна='Италия')
    Author.add_author(surname='Малевич', name='Казимир', last_name='Северинович', birth_year=1879, death_year=1935, страна='Россия')


    for i in range(len(Picture.pictures)):
        Picture.add_author_to_picture(i, i)


    beautiful_request()
