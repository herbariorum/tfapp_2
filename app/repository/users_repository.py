import json
from peewee import DoesNotExist, IntegrityError


class UserRepository:

    @staticmethod
    def select_all(model):
        try:
            usuarios = model.select()          
        except DoesNotExist:
            return False
        
        return usuarios

    @staticmethod
    def create(model, data):
        try:
            model.create(**data)
            return True
        except IntegrityError as e:
            # Captura erros de banco (como email duplicado) e retorna JSON formatado
            return json.dumps({
                "error": "database_error",
                "message": str(e).split('DETAIL:')[0].strip(), # Mensagem amigável
                "detail": str(e).split('DETAIL:')[-1].strip() if 'DETAIL:' in str(e) else ""
            })
        except Exception as e:
            # Captura qualquer outro erro inesperado
            return json.dumps({
                "error": "system_error",
                "message": str(e)
            })

    @staticmethod
    def update(model, id, data):        
        try:
            usuario = model.update(**data).where(model.id == id)   
            usuario.execute()        
            return True
        except Exception as e:
            return False

    @staticmethod
    def delete(model, id):
        try:
            usuario = model.delete().where(model.id == id)
            usuario.execute()
            return True
        except Exception as e:
            return False