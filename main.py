import sys
from typing import List, Tuple

from classes import Entry, PhoneBook

def read_command() -> str:
    '''
    вспомогательная функция, убирает небольшой кусок дублирующегося кода
    предназначена для вывода стартового меню и получения от пользователя следующей команды

    :param: нет
    :return: str - строка с выбранным значением
    '''
    command = input('''\nВведите команду: 0 - выход, 
                 1 - добавить запись в телефонную книгу,
                 2 - обновить запись,
                 3 - вывести все записи,
                 4 - вывести записи по одной или нескольким характеристикам\n''')
    return command


def input_entry() -> Tuple[str, ...]:
        '''
        метод для ввода полного набора данных

        :param: нет
        :return: Tuple[str, ...]
        '''
        last_name = input('Введите фамилию: ').title()
        first_name = input('Введите имя: ').title()
        patronymic = input('Введите отчество: ').title()
        organisation = input('Введите организацию: ').title()
        if len(organisation.split()) > 1:
            organisation = '_'.join(organisation.split())
        work_phone = input_number('Введите рабочий телефон: ')
        personal_phone = input_number('Введите личный телефон: ')
        return last_name, first_name, patronymic, organisation, work_phone, personal_phone


def input_number(message: str) -> str:
    '''
    функция для преобразавания переданного номера к корректному формату
    можно выбрать любой другой; здесь применяется базовый: +7(xxx)xxx-xx-xx

    :param message: str - сообщение, которое будет выводиться при запросе номера телефона
    :return: str - итоговая версия телефонного номера в необходимом формате
    '''
    phone_number = input(message)
    if phone_number == '':
        return ''
    
    nums = [symbol for symbol in phone_number if symbol.isdigit()]
    while len(nums) != 11:
        phone_number = input('Номер некорректен - 11 символов! Введите корректный номер: ')
        nums = [symbol for symbol in phone_number if symbol.isdigit()]

    correct_number_format = '+7' + \
                            '(' + ''.join(nums[1: 4]) + ')' + \
                            ''.join(nums[4: 7]) + \
                            '-' + ''.join(nums[7: 9]) + '-' + ''.join(nums[9: 11])
    
    return correct_number_format


def main() -> None:
    '''
    главная функция программы
    в ней мы выполняем определение названия файла, в которую будем добавлять записи 
    (на каждый запуск программы файл свой)

    :param: нет
    :return: нет
    '''
    filename = sys.argv[1] if len(sys.argv) > 1 else 'base.txt'
    phone_book = PhoneBook(filename=filename)

    command = '-1'

    while command != '0':
        command = read_command()

        if command == '0':
            print('До свидания')
            sys.exit()

        if command == '1':
            print('\nВведите данные для внесения новой записи')
            entry = Entry(*input_entry())
            phone_book.add_entry(entry)

        elif command == '2':
            phone_book_has_entries = phone_book.show_entries()
            if phone_book_has_entries == False:
                print('Сначала добавьте в нее несколько записей')
                continue
            print('\nВведите данные записи, которую хотите обновить (фамилию, имя и отчество человека)')
            last_name = input('Введите фамилию: ').title()
            first_name = input('Введите имя: ').title()
            patronymic = input('Введите отчество: ').title()
            if phone_book.is_entry_exist(last_name, first_name, patronymic):
                print('Заполните только те поля дальше, которые хотите поменять, остальные пропустите')
                new_entry = Entry(*input_entry())
                phone_book.update_entry(last_name, first_name, patronymic, new_entry)
            else:
                # если не нашли нужную запись, предлагаем еще раз сделать выбор
                print('Такого человека в телефонном справочнике нет, попробуйте еще раз') 

        elif command == '3':
            phone_book.show_entries()

        elif command == '4':
            choice = input('''Введите параметр поиска: 1 - по фамилии, 
                         2 - по названию организации,
                         3 - по этим двум характеристикам одновременно\n''')
            
            def get_parameters(msg: str) -> List[str]:
                '''
                вспомогательная функция для преобразования ввода в список строк, каждая из которых начинется с большой буквы

                :param msg: str - строка, которая передается для отображения на экране при считывании
                :return: List[str] - итоговый список строк
                '''
                return list(map(lambda s: s.capitalize(), input(msg).split()))

            if choice == '1':
                last_names = get_parameters('Введите 1 или более фамилий, по которым хотите искать (в строчку через пробел): \n')
                phone_book.show_entries_by_characteristic(choice, last_names)
            elif choice == '2':
                organisations = get_parameters('Введите 1 или более организаций, по которым хотите искать (в строчку через пробел): \n')
                phone_book.show_entries_by_characteristic(choice, organisations)
            elif choice == '3':
                last_name_organisation = get_parameters('Введите фамилию и организацию (в строчку через пробел): \n')
                phone_book.show_entries_by_characteristic(choice, last_name_organisation)
            else:
                print('Неизвестный вариант')


        else:
            print('Неизвестная команда')


if __name__ == '__main__':
    main()