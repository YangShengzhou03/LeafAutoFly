import os
import click
from flask.cli import with_appcontext
from app import create_app
from app.utils.helpers import ensure_data_directories
from app.services.auth_service import create_user

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

@app.cli.command("init-data")
@with_appcontext
def init_data():
    """初始化数据目录和默认数据"""
    ensure_data_directories()
    click.echo("数据目录初始化完成")

@app.cli.command("create-admin")
@click.option("--username", prompt="管理员用户名", help="管理员用户名")
@click.option("--email", prompt="管理员邮箱", help="管理员邮箱")
@click.option("--password", prompt="管理员密码", hide_input=True, confirmation_prompt=True, help="管理员密码")
@with_appcontext
def create_admin(username, email, password):
    """创建管理员用户"""
    try:
        user = create_user(username, email, password)
        click.echo(f"管理员用户创建成功: {user.username} ({user.email})")
    except ValueError as e:
        click.echo(f"创建失败: {str(e)}", err=True)

if __name__ == '__main__':
    app.run()
