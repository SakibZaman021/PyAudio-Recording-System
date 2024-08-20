# from datetime import datetime
# from threading import Lock

# class UserSingleton:
#     _instance = None
#     _lock = Lock()

#     @staticmethod
#     def getInstance(id=None, hospital=None, doc_id=None):
#         with UserSingleton._lock:
#             if UserSingleton._instance is None:
#                 if id is None or hospital is None or doc_id is None:
#                     raise ValueError("UserSingleton requires id, hospital, and doc_id for initialization")
#                 UserSingleton(id, doc_id, hospital)
#             return UserSingleton._instance
    
#     @staticmethod
#     def delInstance():
#         with UserSingleton._lock:
#             UserSingleton._instance = None
        
#     def __init__(self, id, doc_id, hospital):
#         if UserSingleton._instance is not None:
#             raise Exception("Singleton class already exists")
#         else:
#             UserSingleton._instance = self
#             self.userId = id
#             self.doctorId = doc_id
#             self.hospital = hospital
#             self.start = datetime.now().strftime("%H:%M")
from threading import Lock

class UserSingleton:
    _instance = None
    _lock = Lock()

    def __init__(self, user_id, hospital, doctor_id):
        if UserSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.userId = user_id
            self.hospital = hospital
            self.doctorId = doctor_id

    @staticmethod
    def getInstance(user_id, hospital, doctor_id):
        with UserSingleton._lock:
            if UserSingleton._instance is None:
                UserSingleton._instance = UserSingleton(user_id, hospital, doctor_id)
            return UserSingleton._instance

    @staticmethod
    def delInstance():
        with UserSingleton._lock:
            UserSingleton._instance = None
