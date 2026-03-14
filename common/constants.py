from enum import Enum

class ConstantMeta(type):
    def __call__(cls):
        return cls.__name__.lower()

class Constant(metaclass=ConstantMeta):
    ...

class Message(Constant):
    ACCOUNTS_USERNAME_PASSWORD_UNFILLED = 'user name and password fiends must be filled'
    ACCOUNTS_SUCCESS_LOGGED_IN = 'successfully logged in'
    ACCOUNTS_WRONG_PSW_OR_USERNAME = 'wrong password or username'
    ACCOUNTS_PASSWORDS_MUST_BE_SAME = 'password must be same'

class Result(Constant):
    SUCCESS = 'success'
    FAILURE = 'failure'


#Usage example

# response_data = {Result(): Result.FAILURE, Message(): Message.FOOBAR_MESSAGE}
# print(response_data) - {'result': 'failure', 'message': 'foobar'}
# Class() will return lowercase name of called class
