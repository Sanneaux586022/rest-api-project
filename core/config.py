import os 


class DevConfigLocal:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL_1")
    DEBUG = True

class DevConfigRemote:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = False


configs = {
    "development": DevConfigLocal,
    "development_remote": DevConfigRemote
}