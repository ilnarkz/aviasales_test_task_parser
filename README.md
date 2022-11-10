# aviasales_test_task_parser


[![Maintainability](https://api.codeclimate.com/v1/badges/cc96e7a64226403cf534/maintainability)](https://codeclimate.com/github/ilnarkz/aviasales_test_task_parser/maintainability)

## Тестовое задание в команду гейтов (Python)

В папке два XML – это ответы на запросы, сделанные к API партнёра via.com.

Необходимо их распарсить и вывести списком отличия между результатами двух запросов по маршрутам (тег Flights).

* Какие рейсы входят в маршрут
* Время начала и время конца маршрута
* Цена маршрута
* Что изменилось по условиям?
* Добавился ли новый маршрут?

Язык реализации — python3
Используемые библиотеки и инструменты — всё на твой выбор.

Оценивать будем умение выполнять задачу имея неполные данные о ней,
умение самостоятельно принимать решения и качество кода.

## 1. Установка

### 1.1 Клонирование репозитория и установка зависимостей

```bash
git clone https://github.com/ilnarkz/aviasales_test_task_parser
cd aviasales_test_task_parser
```

Установка зависимостей (используйте **Poetry**)

```bash
make install
```

### 1.2 Активация виртуального окружения

```bash
python3 -m venv .venv
source .venv/bin/activate
```


## 2. Запуск утилиты

Для просмотра всех рейсов используйте:

```bash
get_flight -f
```

Для просмотра добавленных маршрутов используйте:

```bash
get_flight -a
```

Для просмотра изменений по условиям используйте:

```bash
get_flight -c
```

Для запуска справки используйте:

```bash
get_flight -h
```
