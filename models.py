from tortoise.models import Model
from tortoise import fields
from tortoise.exceptions import DoesNotExist


class User(Model):

    id = fields.IntField(pk=True)
    discord_id = fields.IntField(unique=True)

    def __str__(self) -> str:
        return f'Bot user (id: {self.id}, discord_id: {self.discord_id})'


async def get_user_model_by_discord_id(discord_id: int) -> User:

    try:
        return await User.get(discord_id=discord_id)

    except DoesNotExist:
        return await User.create(discord_id=discord_id)


class QuestionBase(Model):

    id = fields.IntField(pk=True)
    pub_date = fields.DatetimeField(auto_now_add=True)
    context = fields.TextField(null=True)
    is_completed = fields.BooleanField(default=False)

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

    def get_thread_name(self) -> str:
        return f'#{self.theme} тема #{self.lesson} урок, {self.get_context_short()}'

    def __str__(self) -> str:
        return f'Question of "theme lesson" type (theme: {self.theme}, lesson: {self.lesson})'

    class Meta:
        table = 'question_theme_lesson'


class QuestionProject(QuestionBase):

    creator = fields.ForeignKeyField('models.User', related_name='project_questions')
    project_name = fields.CharField(max_length=127)

    def get_thread_name(self) -> str:
        return f'#{self.project_name} проект, {self.get_context_short()}'

    def __str__(self) -> str:
        return f'Question of "project" type (project: {self.project_name[:50]})'

    class Meta:
        table = 'question_project'


class QuestionAnother(QuestionBase):

    creator = fields.ForeignKeyField('models.User', related_name='another_questions')

    def get_thread_name(self) -> str:
        return f'#другое, {self.get_context_short()}'

    def __str__(self) -> str:
        return f'Question of "another" type (context: {self.context[:50]})'

    class Meta:
        table = 'question_another'
