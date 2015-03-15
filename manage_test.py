from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os


app = Flask(__name__)
# app.config.from_object("config.TestingConfig")
db = SQLAlchemy(app)


# app.config.from_object(os.environ['APP_SETTINGS'])

# migrate = Migrate(app, db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)

# if __name__ == '__main__':
#     manager.run()
