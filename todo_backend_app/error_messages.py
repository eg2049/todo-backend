# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Сообщения с текстами ошибок
"""

from config.config import PASSWORD_MIN_LENGTH


def error_message_get_common(message_name: str) -> str or None:
    """Получение общих сообщений об ошибках

    Args:
        message_name (str): короткое название сообщения

    Returns:
        str or None: текст сообщения или None
    """

    if message_name == 'internal_server_error':
        result = 'Internal server error.'

    elif message_name == 'forbidden':
        result = "You don't have permission to access."

    else:
        result = None

    return result


def error_message_get_auth(message_name: str) -> str or None:
    """Получение сообщений об ошибках связанных с аутентификацией

    Args:
        message_name (str): короткое название сообщения

    Returns:
        str or None: текст сообщения или None
    """

    if message_name == 'invalid_credentials':
        result = 'Invalid credentials.'

    elif message_name == 'email_invalid':
        result = 'Invalid email.'

    if message_name == 'email_already_exists':
        result = 'A user with that email already exists.'

    elif message_name == 'username_already_exists':
        result = 'A user with that username already exists.'

    elif message_name == 'password_too_short':
        result = f'Password length less than {PASSWORD_MIN_LENGTH} characters.'

    elif message_name == 'confirm_token_not_found':
        result = 'Confirm token not found.'

    elif message_name == 'profile_already_confirmed':
        result = 'Profile already confirmed.'

    else:
        result = None

    return result


def error_message_get_todo(message_name: str) -> str or None:
    """Получение сообщений об ошибках связанных с todo

    Args:
        message_name (str): короткое название сообщения

    Returns:
        str or None: текст сообщения или None
    """

    if message_name == 'title_already_exists':
        result = 'Title already exists.'

    elif message_name == 'title_is_empty':
        result = 'Title is empty.'

    else:
        result = None

    return result


if __name__ == '__main__':
    pass
