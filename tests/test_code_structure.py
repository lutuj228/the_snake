"""Тесты структуры классов и основных элементов игры «Змейка»."""

import pygame
import pytest


EXPECTED_GAME_OBJECT_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'body_color'),
    ('метод', 'draw'),
)


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_GAME_OBJECT_ATTRS,
    ids=[elem[1] for elem in EXPECTED_GAME_OBJECT_ATTRS]
)
def test_game_object_attributes(game_object, attr_type, attr_name):
    """Проверить наличие обязательных атрибутов класса GameObject.

    Args:
        game_object: Экземпляр класса GameObject.
        attr_type (str): Тип проверяемого элемента.
        attr_name (str): Название проверяемого элемента.

    Returns:
        None: Функция ничего не возвращает.
    """
    assert hasattr(game_object, attr_name), (
        f'Убедитесь, что у объектов класса `GameObject` определен {attr_type} '
        f'`{attr_name}`.'
    )


EXPECTED_APPLE_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'body_color'),
    ('метод', 'draw'),
    ('метод', 'randomize_position'),
)


def test_apple_inherits_from_game_object(_the_snake):
    """Проверить наследование класса Apple от GameObject.

    Args:
        _the_snake: Импортированный модуль игры.

    Returns:
        None: Функция ничего не возвращает.
    """
    assert issubclass(_the_snake.Apple, _the_snake.GameObject), (
        'Класс `Apple` должен наследоваться от класса `GameObject`.'
    )


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_APPLE_ATTRS,
    ids=[elem[1] for elem in EXPECTED_APPLE_ATTRS]
)
def test_apple_attributes(apple, attr_type, attr_name):
    """Проверить наличие обязательных атрибутов класса Apple.

    Args:
        apple: Экземпляр класса Apple.
        attr_type (str): Тип проверяемого элемента.
        attr_name (str): Название проверяемого элемента.

    Returns:
        None: Функция ничего не возвращает.
    """
    assert hasattr(apple, attr_name), (
        f'Убедитесь, что у объектов класса `Apple` определен {attr_type} '
        f'`{attr_name}`.'
    )


EXPECTED_SNAKE_ATTRS = (
    ('атрибут', 'position'),
    ('атрибут', 'body_color'),
    ('атрибут', 'positions'),
    ('атрибут', 'direction'),
    ('метод', 'draw'),
    ('метод', 'get_head_position'),
    ('метод', 'move'),
    ('метод', 'reset'),
    ('метод', 'update_direction'),
)


def test_snake_inherits_from_game_object(_the_snake):
    """Проверить наследование класса Snake от GameObject.

    Args:
        _the_snake: Импортированный модуль игры.

    Returns:
        None: Функция ничего не возвращает.
    """
    assert issubclass(_the_snake.Snake, _the_snake.GameObject), (
        'Класс `Snake` должен наследоваться от класса `GameObject`.'
    )


@pytest.mark.parametrize(
    'attr_type, attr_name',
    EXPECTED_SNAKE_ATTRS,
    ids=[elem[1] for elem in EXPECTED_SNAKE_ATTRS]
)
def test_snake_attributes(snake, attr_type, attr_name):
    """Проверить наличие обязательных атрибутов класса Snake.

    Args:
        snake: Экземпляр класса Snake.
        attr_type (str): Тип проверяемого элемента.
        attr_name (str): Название проверяемого элемента.

    Returns:
        None: Функция ничего не возвращает.
    """
    assert hasattr(snake, attr_name), (
        f'Убедитесь, что у объектов класса `Snake` определен {attr_type} '
        f'`{attr_name}`.'
    )


EXPECTED_MODULE_ELEMENTS = (
    ('константа', 'SCREEN_WIDTH'),
    ('константа', 'SCREEN_HEIGHT'),
    ('константа', 'GRID_SIZE'),
    ('константа', 'GRID_WIDTH'),
    ('константа', 'GRID_HEIGHT'),
    ('константа', 'BOARD_BACKGROUND_COLOR'),
    ('константа', 'UP'),
    ('константа', 'DOWN'),
    ('константа', 'LEFT'),
    ('константа', 'RIGHT'),
    ('переменная', 'screen'),
    ('переменная', 'clock'),
    ('функция', 'main'),
    ('функция', 'handle_keys'),
)


@pytest.mark.parametrize(
    'element_type, element_name',
    EXPECTED_MODULE_ELEMENTS,
    ids=[elem[1] for elem in EXPECTED_MODULE_ELEMENTS]
)
def test_elements_exist(element_type, element_name, _the_snake):
    """Проверить наличие обязательных элементов модуля игры.

    Args:
        element_type (str): Тип проверяемого элемента.
        element_name (str): Название проверяемого элемента.
        _the_snake: Импортированный модуль игры.

    Returns:
        None: Функция ничего не возвращает.
    """
    assert hasattr(_the_snake, element_name), (
        f'Убедитесь, что в модуле `the_snake` определена {element_type} '
        f'`{element_name}`.'
    )


@pytest.mark.parametrize(
    'expected_type, var_name',
    (
        (pygame.Surface, 'screen'),
        (pygame.time.Clock, 'clock'),
    ),
)
def test_vars_type(expected_type, var_name, _the_snake):
    """Проверить типы переменных screen и clock.

    Args:
        expected_type (type): Ожидаемый тип переменной.
        var_name (str): Название проверяемой переменной.
        _the_snake: Импортированный модуль игры.

    Returns:
        None: Функция ничего не возвращает.
    """
    assert isinstance(getattr(_the_snake, var_name, None), expected_type), (
        'Убедитесь, что в модуле `the_snake` есть переменная '
        f'`{var_name}` типа `{expected_type.__name__}`.'
    )


@pytest.mark.parametrize(
    'func_name',
    ('handle_keys', 'main'),
)
def test_vars_are_functions(func_name, _the_snake):
    """Проверить, что указанные элементы модуля являются функциями.

    Args:
        func_name (str): Название проверяемой функции.
        _the_snake: Импортированный модуль игры.

    Returns:
        None: Функция ничего не возвращает.
    """
    assert callable(getattr(_the_snake, func_name, None)), (
        f'Убедитесь, что переменная `{func_name}` - это функция.'
    )
