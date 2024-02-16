# Телефонная книга

Запускется программа с помощью следующей команды:
`python main.py <filename>.txt`
Последний аргумент с названием файла можно опустить, в этом случае будет создан файл base.txt.

На экране появляется меню:
```
Введите команду: 0 - выход,
                 1 - добавить запись в телефонную книгу,
                 2 - обновить запись,
                 3 - вывести все записи,
                 4 - вывести записи по одной или нескольким характеристикам
```

1) При выборе пункта `0` программа завершает свою работу.
2) При выборе пункта `1` предлагается ввести данные для записи:
```
Введите данные для внесения новой записи
Введите фамилию: сергеев
Введите имя: иван
Введите отчество: юрьевич
Введите организацию: яндекс
Введите рабочий телефон: 894545645645
Введите личный телефон: 89996544534
```
* При разработке программы принято допущение - каждый человек однозначно определяется по своим фамилии, имени и отчеству. Если в файле уже есть человек с такими данными, то будет выведено соответствующее сообщение, и новая запись не будет добавлена.
* Все фамилии, имена, отчества и названия организаций можно вводить в любом регистре, они потом автоматически приводятся к нужной форме.
* Лучше не вводить названия организаций, состоящие из более чем одного слова. Если все таки такая необходимость есть, то название будет выводиться через нижнее подчеркивание.
* Важно: при заполнении полей для добавления новой записи все поля должны быть заполнены.

3) При выборе пункта `2` предлагается обновить данные записи. По аналогии с прошлым пунктом, комбинации фамилии, имени и отчества достаточно для однозначного определения записи.
```
Введите данные для внесения новой записи
Введите фамилию: сергеев
Введите имя: иван
Введите отчество: николаевич
```
Если такого человека нет, на экран будет выведено соответствующее сообщение. В ином случае - будет предложено обновить данные. Те поля, которые менять не нужно, оставляем пустыми. Остальные заполняем.

4) При выборе пункта `3` просто отображается таблица содержащая в себе все данные в отсортированном виде. (Для корректного отображения консоль следует развернуть на полный экран)

5) При выборе пункта `4` представлен выбор характеристик, по которым будет осуществляться поиск.
```
Введите параметр поиска: 1 - по фамилии,
                         2 - по названию организации,
                         3 - по этим двум характеристикам одновременно
```
Для первых двух вариантов нужно ввести список фамилий/организаций, поиск выполняется по их объединению, в третьем варианте - по пересечению введенных фамилии и организации.

Также предусмотрена проверка на существование файла, с которым ведется работа. Она выполняется перед каждым сеансом работы с файлом. В случае его отсутствия создается новый файл с тем же именем, который был у удаленного.
