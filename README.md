# Magic Tricks Shop
 

## Описание

**Magic Tricks Shop** – это проект, включающий в себя веб-приложение и телеграм-бота для управления магазином товаров для фокусников.  
Сайт реализован на Django, а бот – на Aiogram. Основные функции:  
- Для сайта:
  - Регистрация и авторизация пользователей.
  - Просмотр и управление заказами.
  - Панель аналитики для администратора.
- Для бота:
  - Верификация пользователей и администраторов.
  - Просмотр заказов и аналитики.

---

## Установка и запуск

### 1. Установка зависимостей
Сначала клонируйте репозиторий:
```bash
git clone <repo_url>
cd MagicTricksShop
```

Установите необходимые библиотеки для Django и Telegram-бота:

```bash
pip install -r requirements.txt
```

### 2. Настройка Django-приложения
2.1. Создайте `.env` файл

Создайте `.env` файл в директории `django_project/MagicTricksShop` и добавьте туда настройки:

```dotenv
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

2.2. Выполните миграции базы данных
```bash
cd django_project/MagicTricksShop
python manage.py makemigrations
python manage.py migrate
```

2.3. Создайте суперпользователя
```bash
python manage.py createsuperuser
```

2.4. Запустите сервер
```bash
python manage.py runserver
```
Сервер будет доступен по адресу: http://127.0.0.1:8000/.

### 3. Настройка и запуск Telegram-бота

3.1. Настройте токен бота

Создайте файл `config.py` в папке `telegram_bot` и добавьте туда токен:

```python
TOKEN = 'your_telegram_bot_token'
```

3.2. Запустите бота

```bash
cd telegram_bot
python main_tb.py
```

## Структура проекта

```plaintext
MagicTricksShop/
│
├── django_project/
│   ├── MagicTricksShop/
│   │   ├── shopUsers/       # Пользователи
│   │   ├── shopOrders/      # Заказы
│   │   ├── shopGoods/       # Товары
│   │   ├── templates/       # HTML-шаблоны
│   │   ├── manage.py        # Управление проектом Django
│   │   └── ...
│
├── telegram_bot/
│   ├── main_tb.py           # Основной бот
│   ├── database.py          # Взаимодействие с базой данных
│   ├── keyboards.py         # Клавиатуры для бота
│   └── test_bot.py          # Тесты бота
│
├── requirements.txt         # Зависимости
└── README.md                # Описание проекта
```

## Тестирование
Запустите юнит-тесты:

```bash
# Для Django:
set DJANGO_SETTINGS_MODULE=MagicTricksShop.settings
python manage.py test

# Для бота:
python -m unittest test_bot.py
```

## Скрипты запуска проекта

Создайте файл `run.sh` для автоматического запуска всех компонентов.

#### `run.sh`
```bash
#!/bin/bash

# Убедитесь, что скрипт выполнен с правами администратора
if [ "$EUID" -ne 0 ]; then 
    echo "Пожалуйста, запустите с правами администратора"
    exit
fi

echo "Запускаем сервер Django..."
cd django_project/MagicTricksShop
python manage.py runserver &

echo "Запускаем Telegram-бота..."
cd ../../telegram_bot
python main_tb.py &
```

### Использование скрипта
Сделайте скрипт исполняемым:

```bash
chmod +x run.sh
```

### Запустите скрипт:

```bash
./run.sh
```

Скрипт автоматически запустит сервер Django и бота в фоне.


## Контакты
**Автор:** Трушина Елизавета

**Email:** lizatrushina96@gmail.com
