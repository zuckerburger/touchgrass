from src.backend.api import API

api = API()
print(api.get_state())
print(api.get_legal_moves())