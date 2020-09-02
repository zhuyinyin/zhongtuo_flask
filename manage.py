from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from utils.create_app import create_app
# 数据库模型
from app.models import db

app = create_app()
db.init_app(app=app)

migrate = Migrate(app, db)
# 初始化管理器
manager = Manager(app)
# 添加 db 命令，并与 MigrateCommand 绑定
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()