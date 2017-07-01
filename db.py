from app import manager
from app import db
from seed import seed_data

from app.module.models import User


@manager.command
def seed():
    seed_data()


if __name__ == '__main__':
    manager.run()
