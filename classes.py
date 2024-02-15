import os

from typing import Any, Callable, List

# константа для отображения "шапки" таблицы
FIELDS = ['Фамилия', 'Имя', 'Отчество', 'Организация', 'Рабочий телефон', 'Личный телефон']

class Entry:
    '''
    класс, представляющий запись в файле
    '''
    def __init__(self, last_name: str,
                    first_name: str,
                    patronymic: str,
                    organisation: str,
                    work_phone: str,
                    personal_phone: str
    ) -> None:
        '''
        :param last_name: str - фамилия
        :param first_name: str - имя
        :param patronymic: str - отчество
        :param organisation: str - организация
        :param work_phone: str - рабочий телефон
        :param personal_phone: str - личный телефон
        :return: нет
        '''
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.organisation = organisation
        self.work_phone = work_phone
        self.personal_phone = personal_phone


class PhoneBook:
    '''
    класс, предназначенный для создания объекта-"базы данных"
    '''
    def __init__(self, filename: str) -> None:
        '''
        зададим название файла-базы и кодировку (нужна для нормального отображения кириллицы)
        '''
        self.filename = filename
        open(file=self.filename, mode='w').close()
        self.encoding = 'utf-8'

    def check_if_file_exist(method: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(self, *args, **kwargs):
            if not os.path.exists(path=self.filename):
                print('Неполадки с файлом, возможно он удален. Сейчас он будет пересоздан')
                open(file=self.filename, mode='w').close()
            return method(self, *args, **kwargs)
        return wrapper

    @check_if_file_exist
    def show_entries(self) -> None:
        '''
        метод для вывода всех записей из телефонной книги в алфавитном порядке

        :param: нет
        :return: нет
        '''
        entries = []
        with open(file=self.filename, mode='r', encoding=self.encoding) as phone_book:
            entry_line = phone_book.readline()
            while entry_line:
                entries.append(entry_line)
                entry_line = phone_book.readline()
            
            if len(entries) == 0:
                print('Телефонная книга пуста')
                return
            
            self.draw_table_header()

            for entry_line in sorted(entries):
                print('{:<20} | {:<20} | {:<20} | {:^20} | {:^20} | {:^20}'.format(*entry_line.split()))

    @check_if_file_exist
    def add_entry(self, entry: Entry) -> None:
        '''
        метод для добавления записи в телефонную книгу
        будем хранить записи в формате: <фамилия> <имя> <отчество> <организация> <рабочий телефон> <личный телефон>

        :param entry: Entry - объект класса, в который при создании мы заносим части записи
        :return: нет
        '''
        with open(file=self.filename, mode='a+', encoding=self.encoding) as phone_book:
            fields = [entry.__dict__[field] for field in entry.__dict__]
            entry_for_insert = ' '.join(fields)
            phone_book.seek(0)
            entry_line = phone_book.readline()
            while entry_line:
                if self.entries_equal(entry_line, entry_for_insert):
                    print('Такой человек уже есть в базе')
                    return
                entry_line = phone_book.readline()
            
            phone_book.write(entry_for_insert + '\n')
            print('Запись добавлена')

    @check_if_file_exist
    def update_entry(self, last_name: str, first_name: str, patronymic: str, entry: Entry) -> None:
        '''
        метод для обновления записи из телефонного справочника
        будем исходить из расчета, что человек однозначно определяется по фамилии, имени и отчеству

        :param last_name: str - фамилия человека
        :param first_name: str - имя человека
        :param patronymic: str - отчество человека
        :param entry: Entry - объект, содержащий новые значения для полей записи или пустые строки
        :return: нет
        '''

        entries = []
        with open(file=self.filename, mode='r', encoding='utf-8') as phone_book:
            entry_line = phone_book.readline()
            while entry_line:
                print(entry_line, ' '.join([last_name, first_name, patronymic]))
                if self.entries_equal(entry_line, ' '.join([last_name, first_name, patronymic])):
                    default_values = entry_line.split()
                    values = entry.__dict__.keys()

                    # проверяем - если аттрибут передан как пустая строка (мы пропустили его при вводе),
                    # то оставляем значение, которое было до этого (выделяем из считанной из файла строки)
                    entry_obj = Entry(*(getattr(entry, attr) if getattr(entry, attr) else default for attr, default in zip(values, default_values)))
                    entry_line = ' '.join(entry_obj.__dict__[field] for field in entry_obj.__dict__) 

                entries.append(entry_line)

                entry_line = phone_book.readline()
                          

        with open(file=self.filename, mode='w', encoding='utf-8') as phone_book:
            for entry_line in entries:
                phone_book.write(entry_line)
        
        print('Данные обновлены')


    @check_if_file_exist
    def show_entries_by_characteristic(self, characteristic: str, arguments: List[str]) -> None:
        '''
        метод для отображения записей по характеристикам
        самым логичным представляется вариант - искать по фамилии и/или названию организации

        :param characteristic: str - параметр, который определяет характеристику или характеристики поиска
        :return: нет
        '''
        self.draw_table_header()
        with open(file=self.filename, mode='r', encoding='utf-8') as phone_book:
            entry_line = phone_book.readline()
            while entry_line:
                entry_line_elements = entry_line.split()
                if (characteristic == '1' and entry_line_elements[0] in arguments) or \
                   (characteristic == '2' and entry_line_elements[3] in arguments) or \
                   (characteristic == '3' and entry_line_elements[0] == arguments[0] and entry_line_elements[3] == arguments[1]):
                    print('{:<20} | {:<20} | {:<20} | {:^20} | {:^20} | {:^20}'.format(*entry_line.split()))

                entry_line = phone_book.readline()

        print()

    @check_if_file_exist
    def is_entry_exist(self, last_name: str, first_name: str, patronymic: str) -> bool:
        '''
        вспомогательый метод
        проверяет, существует ли человек с данными фамилией, именем и отчеством в телефонной книге

        :param last_name: str - фамилия человека
        :param first_name: str - имя человека
        :param patronymic: str - отчество человека
        :return: bool - результат проверки на существование
        '''
        with open(file=self.filename, mode='r', encoding=self.encoding) as phone_book:
            entry_line = phone_book.readline()
            while entry_line:
                if self.entries_equal(entry_line, ' '.join([last_name, first_name, patronymic])):
                    return True
                
        return False


    @staticmethod
    def entries_equal(line1: str, line2: str) -> bool:
        '''
        вспомогательный метод, используется для выяснения равенства двух записей (по фамилии, имени и отчеству)

        :param line1: str - первая строка для сравнения
        :param line2: str - вторая строка для сравнения
        :return: bool - булевское значение, показывающее результат сравнения двух записей
        '''
        last_name1, first_name1, patronymic1 = line1.split()[:3]
        last_name2, first_name2, patronymic2 = line2.split()[:3]
        return last_name1 == last_name2 and first_name1 == first_name2 and patronymic1 == patronymic2 
    
    @staticmethod
    def draw_table_header() -> None:
        '''
        простой метод для отрисовки шапки таблицы при показе набора записей из справочника 
        (или всех или отобранных по характеристикам)

        :param: нет
        :return: нет
        '''
        print('{:^20} | {:^20} | {:^20} | {:^20} | {:^20} | {:^20}'.format(*FIELDS))
        print('_' * 135)
    
