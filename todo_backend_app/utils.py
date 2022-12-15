# -*- coding: utf-8 -*-

"""
Use Python 3.10.0

Полезные утилиты
"""

from re import compile, search


def email_regex(email: str) -> bool:
    """Проверка валидности email

    Args:
        email (str): email

    Returns:
        bool: валиден ли email
    """

    re_email = compile(r'[^@]+@[^@]+\.[^@]+')

    match = search(re_email, email)

    return True if match else False


if __name__ == '__main__':
    pass
