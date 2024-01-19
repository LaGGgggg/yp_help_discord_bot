from typing import Type

from tortoise.exceptions import DoesNotExist

from models import User, QuestionBase, QuestionThemeLesson, QuestionProject, QuestionAnother


async def get_user_model_by_discord_id(discord_id: int) -> User:

    try:
        return await User.get(discord_id=discord_id)

    except DoesNotExist:
        return await User.create(discord_id=discord_id)


async def get_question_by_discord_channel_id(discord_channel_id: int) -> Type[QuestionBase] | None:
    for question_model in (QuestionThemeLesson, QuestionProject, QuestionAnother):

        try:
            return await question_model.get(discord_channel_id=discord_channel_id)

        except DoesNotExist:
            continue


async def get_all_questions(**filter_kwargs) -> list[QuestionThemeLesson | QuestionProject | QuestionAnother]:

    result = []

    result.extend(await QuestionThemeLesson.filter(**filter_kwargs))
    result.extend(await QuestionProject.filter(**filter_kwargs))
    result.extend(await QuestionAnother.filter(**filter_kwargs))

    return result
