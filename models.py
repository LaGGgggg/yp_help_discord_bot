from typing import Type

from tortoise.models import Model
from tortoise import fields
from tortoise.exceptions import DoesNotExist


class User(Model):

    id = fields.IntField(pk=True)
    discord_id = fields.IntField(unique=True)

    def __str__(self) -> str:
        return f'Bot user (id: {self.id}, discord_id: {self.discord_id})'

# TODO Я бы вынес всю логику с базой в отдельный файл, в моделях обычно лежит только само описание данных
async def get_user_model_by_discord_id(discord_id: int) -> User:

    try:
        return await User.get(discord_id=discord_id) 

    except DoesNotExist: # TODO Больше вопрос чем замечание, никогда не работал с черепашкой. У нее нет встроенной возможности создать если не существует?
        return await User.create(discord_id=discord_id)


class QuestionBase(Model):
    """
    All subclasses must include:
    creator = fields.ForeignKeyField('models.User', related_name='<related_name>')
    QUESTION_TYPE = '<question_type>'
    sync function: get_thread_name(self) -> str
    """

    id = fields.IntField(pk=True)
    pub_date = fields.DatetimeField(auto_now_add=True)
    context = fields.TextField(null=True)
    is_completed = fields.BooleanField(default=False)
    discord_channel_id = fields.IntField(null=True, index=True, unique=True)

    def get_context_short(self) -> str:

        context_short = self.context

        if len(context_short) > 30:
            context_short = f'{context_short[:30]}...'

        return context_short

    def get_thread_description(self) -> str:
        return self.context

    class Meta:
        abstract = True


class QuestionThemeLesson(QuestionBase):

    creator = fields.ForeignKeyField('models.User', related_name='theme_lesson_questions')
    theme = fields.SmallIntField()
    lesson = fields.SmallIntField()

    QUESTION_TYPE = 'theme_lesson'

    def get_thread_name(self) -> str:
        return f'#{self.theme} тема #{self.lesson} урок, {self.get_context_short()}'

    def __str__(self) -> str:
        return f'Question of "theme lesson" type (theme: {self.theme}, lesson: {self.lesson})'

    class Meta:
        table = 'question_theme_lesson'


class QuestionProject(QuestionBase):

    creator = fields.ForeignKeyField('models.User', related_name='project_questions')
    project_name = fields.CharField(max_length=127)

    QUESTION_TYPE = 'project'

    def get_thread_name(self) -> str:
        return f'#{self.project_name} проект, {self.get_context_short()}'

    def __str__(self) -> str:
        return f'Question of "project" type (project: {self.project_name[:50]})'

    class Meta:
        table = 'question_project'


class QuestionAnother(QuestionBase):

    creator = fields.ForeignKeyField('models.User', related_name='another_questions')

    QUESTION_TYPE = 'another'

    def get_thread_name(self) -> str:
        return f'#другое, {self.get_context_short()}'

    def __str__(self) -> str:
        return f'Question of "another" type (context: {self.context[:50]})'

    class Meta:
        table = 'question_another'


async def get_question_by_discord_channel_id(discord_channel_id: int) -> Type[QuestionBase] | None:
    for question_model in (QuestionThemeLesson, QuestionProject, QuestionAnother):

        try:
            return await question_model.get(discord_channel_id=discord_channel_id)

        except DoesNotExist:
            continue # TODO Вот тут будто лучше бы логировать это дело


async def get_all_questions(**filter_kwargs) -> list[QuestionThemeLesson | QuestionProject | QuestionAnother]:

    result = []
    # TODO Как будто стоило сделать немного по другому, чтобы у таблицы Question было поле тип вопроса, которое бы тянулось из одной доп. таблицы,
    # сейчас для расширения нам надо будет писать еще одну модель, в моем предложенном случае мы бы просто добавили еще одну запись в бд
    result.extend(await QuestionThemeLesson.filter(**filter_kwargs))
    result.extend(await QuestionProject.filter(**filter_kwargs))
    result.extend(await QuestionAnother.filter(**filter_kwargs))

    return result


class QuestionStatistics(Model):

    id = fields.IntField(pk=True)
    pub_date = fields.DatetimeField(auto_now_add=True)
    discord_channel_id = fields.IntField(index=True, unique=True)
    requests = fields.IntField(default=1)

    async def get_question_object(self) -> Type[QuestionBase]:
        return await get_question_by_discord_channel_id(self.discord_channel_id)

    def __str__(self) -> str:
        return f'Question statistics requests: {self.requests} discord_channel_id: {self.discord_channel_id}'

    class Meta:
        table = 'question_statistics'
