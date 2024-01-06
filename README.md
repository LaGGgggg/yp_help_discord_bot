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

### 5. Запустите проект

```bash
python main.py
```

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
