from datetime import datetime, timedelta

from tortoise.models import Model
from tortoise import fields


class User(Model):

    id = fields.IntField(pk=True)
    discord_id = fields.BigIntField(unique=True)

    def __str__(self) -> str:
        return f'Bot user (id: {self.id}, discord_id: {self.discord_id})'


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
    discord_channel_id = fields.BigIntField(null=True, index=True, unique=True)

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


class QuestionStatistics(Model):

    id = fields.IntField(pk=True)
    pub_date = fields.DatetimeField(auto_now_add=True)
    discord_channel_id = fields.BigIntField(index=True, unique=True)
    requests = fields.IntField(default=1)

    def __str__(self) -> str:
        return f'Question statistics requests: {self.requests} discord_channel_id: {self.discord_channel_id}'

    class Meta:
        table = 'question_statistics'


class UserRequests(Model):

    id = fields.IntField(pk=True)
    date = fields.DatetimeField(auto_now_add=True)
    user = fields.ForeignKeyField('models.User', related_name='user_requests')
    anonymous_messages_counter = fields.IntField(default=0)
    questions_creations_counter = fields.IntField(default=0)
    questions_searches_counter = fields.IntField(default=0)

    def check_and_fix_date(self) -> None:
        """
        Checks the datetime of an object, if it is more than 24 hours, resets the counters and sets the datetime (now)
        """

        datetime_now = datetime.now()

        if (self.date + timedelta(hours=24)).timestamp() <= datetime_now.timestamp():

            self.date = datetime_now
            self.anonymous_messages_counter = 0
            self.questions_creations_counter = 0
            self.questions_searches_counter = 0

    def __str__(self) -> str:
        return (
            f'User requests: anonymous messages counter = {self.anonymous_messages_counter}, questions creations'
            f' counter = {self.questions_creations_counter}, questions searches counter ='
            f' {self.questions_searches_counter}'
        )

    class Meta:
        table = 'user_requests'
