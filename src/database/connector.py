from src.utils import logger_create
from src.database.orm import Session, TelegramUser, BackendData


class Connector:
    @property
    def __name__(self):
        return 'DBConnector'

    def __init__(self,  **kwargs):
        self.logger = logger_create(self.__name__)
        self.logger.debug("Initialized")
        self.session = Session()

    def add_new_telegram_user(self, **kwargs):
        try:
            kwargs.pop('is_bot'), kwargs.pop('language_code')
            _new_user = TelegramUser(**kwargs)
            self.session.add(_new_user)
            self.logger.debug(f"New user {_new_user.id} registered")
            self.session.commit()
        except:
            pass

    def add_new_backend_data(self, user, data):
        try:
            _user = TelegramUser(id=user.id)
            _new_data = BackendData(telegram_id=_user.id, data=data)
            self.session.add(_new_data)
            self.session.commit()
        except:
            pass

    def get_backend_data(self, user):
        data = self.session.query(BackendData.data) \
            .filter(BackendData.telegram_id == user.id).all()
        return data
