![GitHub](https://img.shields.io/github/license/LaGGgggg/yp_help_discord_bot?label=License)
![GitHub watchers](https://img.shields.io/github/watchers/LaGGgggg/yp_help_discord_bot?style=flat)
![GitHub last commit](https://img.shields.io/github/last-commit/LaGGgggg/yp_help_discord_bot)

# Дискорд бот для помощи в решении проблем студентам Яндекс практикума

# Как запустить проект?

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/LaGGgggg/yp_help_discord_bot.git
cd yp_help_discord_bot
```

### 2. Создайте виртуальное окружение

#### С помощью [pipenv](https://pipenv.pypa.io/en/latest/):

```bash
pip install --user pipenv
pipenv shell  # create and activate
```

#### Или классическим методом:

```bash
python -m venv .venv  # create
.venv\Scripts\activate.bat  # activate
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Установите переменные окружения (environment variables)

Создайте файл `.env`, это должно выглядеть так: `yp_help_discord_bot/.env`. После скопируйте это в `.env`

```dotenv
BOT_TOKEN=<your_bot_token>
HELP_FORUM_CHANNEL_ID=<your_help_forum_channel_id>
DB_URL=sqlite://db.sqlite3  # вы можете оставить значение по умолчанию
COGS_DIR_NAME=cogs  # вы можете оставить значение по умолчанию
SUPERUSERS_IDS=<your_superusers_ids>  # id следует разделять ",", например: "111,222" или "333"
ADMIN_ROLES=<your_admin_roles>  # роли следует разделять ",", например: "admin,superadmin" или "admin"
DEBUG=False
ANONYMOUS_MESSAGES_DAY_LIMIT=150
QUESTIONS_CREATIONS_DAY_LIMIT=20
QUESTIONS_SEARCHES_DAY_LIMIT=1000
DELETED_MESSAGES_LIMIT=5
DELETED_MESSAGES_PERIOD_HOURS=48
```
_**Не забудьте поменять значения на свои! (поставьте его после "=")**_

#### Больше о переменных:
BOT_TOKEN - API токен дискорд бота.<br>
HELP_FORUM_CHANNEL_ID - id канала-форума, где бот будет работать с вопросами
(канал должен быть типа [ForumChannel](https://discordpy.readthedocs.io/en/stable/api.html?#forumchannel)).<br>
DB_URL - обычный [url базы данных](https://tortoise.github.io/databases.html#db-url).<br>
COGS_DIR_NAME - название директории, в которой находятся файлы с
[cog-ами](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)
(файлы с отличным от ".py" расширением и начинающиеся с "_" игнорируются).<br>
SUPERUSERS_IDS - discord ids суперпользователей (пользователей бота с расширенными правами,
каждый id отделяется от другого при помощи ",", например: "SUPERUSERS_IDS=111,222" или "SUPERUSERS_IDS=333").<br>
ADMIN_ROLES - роли суперпользователей (пользователей бота с расширенными правами,
каждая роль отделяется от другой при помощи ",", например: "ADMIN_ROLES=admin,superadmin" или "ADMIN_ROLES=admin").<br>
DEBUG - "true" для True или любое другое значени для False, определяет тип логирования (в файл или в консоль).<br>
ANONYMOUS_MESSAGES_DAY_LIMIT - лимит анонимных сообщений, которые может отослать пользователь в сутки.<br>
QUESTIONS_CREATIONS_DAY_LIMIT - лимит на создание вопросов пользователем в сутки.<br>
QUESTIONS_SEARCHES_DAY_LIMIT - лимит на поиск похожих вопросов пользователем в сутки.<br>
DELETED_MESSAGES_LIMIT - лимит на удалённые анонимные сообщения пользователя (после превышения пользователь блокируется).<br>
DELETED_MESSAGES_PERIOD_HOURS - период, в течение которого не должен быть превышен лимит на удалённые сообщения.<br>

### 5. Запустите проект

```bash
python main.py
```

# Продакшен настройка

### 1. Установите [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### 2. Установите [docker](https://docs.docker.com/engine/install/)

### 3. Установите [docker compose plugin](https://docs.docker.com/compose/install/linux/)

### 4. Клонируйте репозиторий

```bash
git clone https://github.com/LaGGgggg/yp_help_discord_bot.git
cd yp_help_discord_bot
```

### 5. Установите переменные окружения (environment variables)

Создайте файл `.env`, это должно выглядеть так: `yp_help_discord_bot/.env`. После скопируйте это в `.env`

```dotenv
BOT_TOKEN=<your_bot_token>
HELP_FORUM_CHANNEL_ID=<your_help_forum_channel_id>
DB_URL=postgres://<username>:<password>@postgres:5432/<database_name>
COGS_DIR_NAME=cogs  # вы можете оставить значение по умолчанию
SUPERUSERS_IDS=<your_superusers_ids>  # id следует разделять ",", например: "111,222" или "333"
ADMIN_ROLES=<your_admin_roles>  # роли следует разделять ",", например: "admin,superadmin" или "admin"
DEBUG=False
ANONYMOUS_MESSAGES_DAY_LIMIT=150
QUESTIONS_CREATIONS_DAY_LIMIT=20
QUESTIONS_SEARCHES_DAY_LIMIT=1000
DELETED_MESSAGES_LIMIT=5
DELETED_MESSAGES_PERIOD_HOURS=48

# docker-compose section
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database_name>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data/pgdata
```
_**Не забудьте поменять значения на свои! (поставьте его после "=")**_

#### Больше о переменных:
BOT_TOKEN - API токен дискорд бота.<br>
HELP_FORUM_CHANNEL_ID - id канала-форума, где бот будет работать с вопросами
(канал должен быть типа [ForumChannel](https://discordpy.readthedocs.io/en/stable/api.html?#forumchannel)).<br>
DB_URL - обычный [url базы данных](https://tortoise.github.io/databases.html#db-url).<br>
COGS_DIR_NAME - название директории, в которой находятся файлы с
[cog-ами](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html)
(файлы с отличным от ".py" расширением и начинающиеся с "_" игнорируются).<br>
SUPERUSERS_IDS - discord ids суперпользователей (пользователей бота с расширенными правами,
каждый id отделяется от другого при помощи ",", например: "SUPERUSERS_IDS=111,222" или "SUPERUSERS_IDS=333").<br>
ADMIN_ROLES - роли суперпользователей (пользователей бота с расширенными правами,
каждая роль отделяется от другой при помощи ",", например: "ADMIN_ROLES=admin,superadmin" или "ADMIN_ROLES=admin").<br>
DEBUG - "true" для True или любое другое значени для False, определяет тип логирования (в файл или в консоль).<br>
ANONYMOUS_MESSAGES_DAY_LIMIT - лимит анонимных сообщений, которые может отослать пользователь в сутки.<br>
QUESTIONS_CREATIONS_DAY_LIMIT - лимит на создание вопросов пользователем в сутки.<br>
QUESTIONS_SEARCHES_DAY_LIMIT - лимит на поиск похожих вопросов пользователем в сутки.<br>
DELETED_MESSAGES_LIMIT - лимит на удалённые анонимные сообщения пользователя (после превышения пользователь блокируется).<br>
DELETED_MESSAGES_PERIOD_HOURS - период, в течение которого не должен быть превышен лимит на удалённые сообщения.<br>

POSTGRES_USER - [POSTGRES_USER](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_PASSWORD - [POSTGRES_PASSWORD](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_DB - [POSTGRES_DB](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_HOST - [POSTGRES_HOST](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
POSTGRES_PORT - [POSTGRES_PORT](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>
PGDATA - [PGDATA](https://hub.docker.com/_/postgres) стандартная переменная окружения docker<br>

### 6. Запустите docker compose

```bash
docker compose up -d
```

### 7. После успешного запуска проверьте сервер

```bash
docker compose logs -f
```

# Команды

`/help` или `/start` - вывод приветственного сообщения.<br>
`/new_question` - создание нового вопроса, доступна всем пользователям в личных сообщениях с ботом.<br>
`/complete_current_question` - завершение вопроса в ветке, где прописана команда, доступна создателю вопроса и
суперпользователям в ветке с вопросом.<br>
`/send_anonymous_message` - отправка анонимного сообщения через бота, доступна всем пользователям в личных сообщениях
с ботом (но посылать такие сообщения можно только в созданные пользователем вопросы).<br>
`/send_anonymous_photo` - отправка анонимного изображения через бота, доступна всем пользователям в личных сообщениях
с ботом (но посылать такие сообщения можно только в созданные пользователем вопросы).<br>
`/get_bot_statistics` - просмотр статистики бота, доступна только суперпользователям в личных сообщениях с ботом.<br>
`/sync` - [синхронизирует](https://discordpy.readthedocs.io/en/stable/interactions/api.html?highlight=sync#discord.app_commands.CommandTree.sync)
команды бота, доступна только суперпользователям в личных сообщениях с ботом.<br>

# Об архитектуре

### Система cog-ов

В проекте используется система [cog-ов](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html),
они хранятся в файлах модуля, задаваемого переменной окружения COGS_DIR_NAME и загружаются автоматически, при запуске
бота (файлы с отличным от ".py" расширением и начинающиеся с "_" при этом игнорируются). В каждом файле cog-а
должна быть (must) асинхронная функция get_cog, возвращающая класс cog-а.  Для создания нового cog-а
рекомендуется наследовать класс CogBase из [cogs/_cog_base.py](cogs/_cog_base.py).

# Для колобораторов

- Мы стараемся придерживаться [этого соглашения о коммитах](https://www.conventionalcommits.org/ru/v1.0.0/).
- Все коммиты и обсуждения мы проводим **по-русски**.
- В коде **всё**, кроме контента для пользователей (сообщения, которые бот отправляет пользователю и т.п.),
на **английском языке**.
- Коммиты первоначально осуществляются в **отдельную** ветку (специально созданную для этих коммитов из **dev** ветки), 
после отправляются в **dev** (посредством pull request-а), только потом в **main**.
