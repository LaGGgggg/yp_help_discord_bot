![GitHub](https://img.shields.io/github/license/LaGGgggg/yp_help_discord_bot?label=License)
![GitHub watchers](https://img.shields.io/github/watchers/LaGGgggg/yp_help_discord_bot)
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
```
_**Не забудьте поменять значения на свои! (поставьте его после "=")**_

#### Больше о переменных:
BOT_TOKEN - API токен дискорд бота.<br>
HELP_FORUM_CHANNEL_ID - id канала-форума, где бот будет работать с вопросами
(канал должен быть типа [ForumChannel](https://discordpy.readthedocs.io/en/stable/api.html?#forumchannel)).

### 5. Запустите проект

```bash
python main.py
```

# Для колобораторов

- Мы стараемся придерживаться [этого соглашения о коммитах](https://www.conventionalcommits.org/ru/v1.0.0/).
- Все коммиты и обсуждения мы проводим **по-русски**.
- В коде **всё**, кроме контента для пользователей (сообщения, которые бот отправляет пользователю и т.п.),
на **английском языке**.
- Коммиты первоначально осуществляются в **отдельную** ветку (специально созданную для этих коммитов из **dev** ветки), 
после отправляются в **dev** (посредством pull request-а), только потом в **main**.
