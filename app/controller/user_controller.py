from ..repository.users_repository import UserRepository
from ..models.users import User

class UserController:
    def __init__(self):
        self.user_repository = UserRepository()

    def list_all(self):
        return self.user_repository.select_all(User)

    def create(self, data):
        return self.user_repository.create(User, data)

    def update(self, id, data):        
        return self.user_repository.update(User, id, data)

    def delete(self, id):
        return self.user_repository.delete(User, id)