# Citation network project

## 2022 fall VKM project

## team 15

[public googlesheet](https://docs.google.com/spreadsheets/d/1rfngbj1W42-KzUHuT28uXmEwZg7bM-FE/edit) с результатами команд

- - - 

## Описание проекта/проектной задачи
Участникам необходимо построить ряд ML моделей и вывести их в production. Основой для проекта является открытый датасет [https://www.aminer.cn/citation](https://www.aminer.cn/citation)

Работа разбита на 2 трека, 3 этапа и 6 спринтов.

В треке **ML** необходимо реализовать 3 типа моделей: 
* классификатор тем статей (topic modelling)
* рекомендация соавторов для автора 
* рекомендация статей для пользователя

В треке **engineering** необходимо реализовать web-сервис с:
* фронт- и 
* бэк-эндом, 
* подключением БД и 
* моделей ML, 
* логированием, 
* с достаточным performance

- - -
### Структура хранилища

* 00_init - входные данные по проекту
* 01_artefacts - то, что показываем <del>заказчику</del> ассессору
    * 01_sprint - папки для каждого спринта
        * 01_eng - для engineering
        * 02_ds - для data science
    * 02_sprint ...
* 02_process - рабочие материалы
    * 01_eng
    * 02_ds
* 20_contacts - контакты участников, тьютора, ассессоров...

Папки с лидирующими номерами образуют скелет (каркас) хранилища. Добавлять новые папки с номерами следует разумно. Названия остальных папок нужно начинать с букв (латиница, кириллица). Структура хранилища формируется командой. Удобство > правил.

Файл .lock используется для создания структуры папок с пустым содержимым. Если в папке с .lock вы комитите файл, то файл .lock нужно удалить.
