from flask_script import Manager
from flask_migrate import  Migrate,MigrateCommand
from Flask_Movie import app
from exts import db
from models import User

manager = Manager(app)

#使用Migrate 绑定app,db

migrate = Migrate(app,db)

#添加迁移脚本的命令到manager中
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
