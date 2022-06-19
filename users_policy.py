from flask_login import current_user
from config import MODER_ROLE_ID

class UsersPolicy:
    def __init__(self):
        pass

    def create(self):
        return current_user.is_admin

    def delete(self):
        return current_user.is_admin

    def update(self):
        return current_user.is_admin or current_user.is_moder
    
    # def show(self):
    #     is_showing_user = current_user.id == self.record.id
    #     return current_user.is_admin or is_showing_user