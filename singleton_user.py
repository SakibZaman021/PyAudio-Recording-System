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
from datetime import datetime

class UserSingleton:
    _instance = None
    _lock = Lock()

    def __init__(self, user_id, hospital, doctor_id):
        print(user_id, hospital,doctor_id + "qqq")
        if UserSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.userId = user_id
            self.hospital = hospital
            self.doctorId = doctor_id

    # @staticmethod
    # def getInstance(user_id_x, hospital_y, doctor_id_z):
    #     print(user_id_x, hospital_y, doctor_id_z + "aaa")
    #     with UserSingleton._lock:
    #         if UserSingleton._instance is None:
    #             UserSingleton._instance = UserSingleton(user_id_x, hospital_y, doctor_id_z)
    #         return UserSingleton._instance
    
    
    @classmethod
    def getInstance(cls, user_id=None, hospital=None, doctor_id=None):
        with cls._lock:
            if cls._instance is None:
                if user_id is None or hospital is None or doctor_id is None:
                    raise ValueError("UserSingleton requires user_id, hospital, and doctor_id for initialization")
                cls._instance = cls(user_id, hospital, doctor_id)
            else:
                if user_id is not None:
                    cls._instance.userId = user_id
                if hospital is not None:
                    cls._instance.hospital = hospital
                if doctor_id is not None:
                    cls._instance.doctorId = doctor_id
                cls._instance.start = datetime.now().strftime("%H:%M")  # Update start time each time instance is modified
            return cls._instance

    @staticmethod
    def delInstance():
        with UserSingleton._lock:
            UserSingleton._instance = None
