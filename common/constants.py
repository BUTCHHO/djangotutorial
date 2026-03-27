from enum import Enum

class ConstantMeta(type):
    def __call__(cls):
        return cls.__name__.lower()

class Constant(metaclass=ConstantMeta):
    ...

class Message(Constant):

    # example
    # %APP_NAME%_%MESSAGE_NAME% = '%message detail%'

    ACCOUNTS_USERNAME_PASSWORD_UNFILLED = 'user name and password fiends must be filled'
    ACCOUNTS_SUCCESS_LOGGED_IN = 'successfully logged in'
    ACCOUNTS_WRONG_PSW_OR_USERNAME = 'wrong password or username'
    ACCOUNTS_PASSWORDS_MUST_BE_SAME = 'password must be same'

    COMMUNITY_NO_POSTS = "No posts are available"
    COMMUNITY_EMPTY_COMMENT_CONTENT = "Comment content cant be empty"

    POLLS_NO_POLLS_AVAILABLE = "No polls available."
    POLLS_NO_CHOICE_AVAILABLE = "No choices available for this question"
    POLLS_NO_CHOICE_MADE = 'You did not make choice'
    POLLS_INVALID_QUESTION_FIELD = 'Question form was not filled correctly'
    POLLS_INVALID_CHOICE_FIELD = 'Make sure that all choices are filled correctly'
    POLLS_LESS_THAN_ALLOWED_CHOICES = "Question cant have less than 2 choices"
    POLLS_REMOVED_CHOICE = "Your choice has been removed"

    FRIENDS_USER_DONT_EXISTS = 'User does not exists'
    FRIENDS_CANT_SEND_REQUEST_TO_USER = "You cant send friend request to this user"
    FRIENDS_REQUEST_ALREADY_SENT = "Friend request is already sent"

class Result(Constant):
    SUCCESS = 'success'
    FAILURE = 'failure'


#Usage example

# response_data = {Result(): Result.FAILURE, Message(): Message.FOOBAR_MESSAGE}
# print(response_data) - {'result': 'failure', 'message': 'foobar'}
# Class() will return lowercase name of called class
