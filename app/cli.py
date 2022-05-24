import click
from flask.cli import with_appcontext
from app.models import User
from app.task import add_together


@click.command('get_users')
@with_appcontext
def get_users_command():  # test only
    print(__name__)
    users = User.objects()
    click.echo(users.to_json())


@click.command('example_task')
@with_appcontext
def example_task_command():
    task = add_together.delay(23, 2)
    click.echo(task.get())


def init_app(app):
    app.cli.add_command(get_users_command)
    app.cli.add_command(example_task_command)
