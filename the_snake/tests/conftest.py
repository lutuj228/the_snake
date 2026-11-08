"""Фикстуры и вспомогательные функции для тестирования игры «Змейка»."""

import importlib
import os
import sys
from multiprocessing import Process
from pathlib import Path
from typing import Any

import pytest
import pytest_timeout
from pygame.time import Clock


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

# Скрытие игрового окна Pygame во время тестирования.
os.environ['SDL_VIDEODRIVER'] = 'dummy'

TIMEOUT_ASSERT_MSG = (
    'Проект работает некорректно, проверка прервана.\n'
    'Вероятные причины ошибки:\n'
    '1. Исполняемый код (например, вызов функции `main()`) оказался в '
    'глобальной зоне видимости. Как исправить: вызов функции `main` поместите '
    'внутрь конструкции `if __name__ == "__main__":`.\n'
    '2. В цикле `while True` внутри функции `main` отсутствует вызов метода '
    '`tick` объекта `clock`. Не изменяйте прекод в этой части.'
)


def import_the_snake():
    """Импортировать модуль игры для проверки корректности его загрузки."""
    importlib.import_module('the_snake')


@pytest.fixture(scope='session')
def snake_import_test():
    """Проверить импорт модуля игры в отдельном процессе.

    Raises:
        AssertionError: Если процесс импорта не завершился за одну секунду.
    """
    check_import_process = Process(target=import_the_snake)
    check_import_process.start()
    pid = check_import_process.pid
    check_import_process.join(timeout=1)

    if check_import_process.is_alive():
        os.kill(pid, 9)
        raise AssertionError(TIMEOUT_ASSERT_MSG)


@pytest.fixture(scope='session')
def _the_snake(snake_import_test):
    """Импортировать модуль игры и проверить наличие необходимых классов.

    Args:
        snake_import_test: Фикстура проверки импорта модуля.

    Returns:
        module: Импортированный модуль игры.

    Raises:
        AssertionError: Если модуль не импортируется или отсутствует класс.
    """
    try:
        import the_snake
    except ImportError as error:
        raise AssertionError(
            'При импорте модуль `the_snake` произошла ошибка:\n'
            f'{type(error).__name__}: {error}'
        )

    for class_name in ('GameObject', 'Snake', 'Apple'):
        assert hasattr(the_snake, class_name), (
            f'Убедитесь, что в модуле `{the_snake}`'
            f'определен класс `{class_name}`.'
        )

    return the_snake


def write_timeout_reasons(text, stream=None):
    """Вывести сообщение с возможными причинами превышения времени теста.

    Args:
        text: Исходный текст сообщения об ошибке.
        stream: Поток для вывода сообщения. По умолчанию sys.stderr.

    Returns:
        None: Функция ничего не возвращает.
    """
    if stream is None:
        stream = sys.stderr

    text = TIMEOUT_ASSERT_MSG
    stream.write(text)


pytest_timeout.write = write_timeout_reasons


def _create_game_object(class_name, module):
    """Создать экземпляр указанного класса из модуля игры.

    Args:
        class_name (str): Название класса, экземпляр которого нужно создать.
        module: Модуль, содержащий необходимый класс.

    Returns:
        object: Созданный экземпляр класса.

    Raises:
        AssertionError: Если конструктор класса требует аргументы.
    """
    try:
        return getattr(module, class_name)()
    except TypeError as error:
        raise AssertionError(
            f'При создании объекта класса `{class_name}` произошла ошибка:\n'
            f'`{type(error).__name__}: {error}`\n'
            f'Если в конструктор класса `{class_name}` помимо параметра '
            '`self` передаются какие-то ещё параметры - убедитесь, что для '
            'них установлены значения по умолчанию. Например:\n'
            '`def __init__(self, <параметр>=<значение_по_умолчанию>):`'
        )


@pytest.fixture
def game_object(_the_snake):
    """Создать экземпляр класса GameObject.

    Args:
        _the_snake: Импортированный модуль игры.

    Returns:
        GameObject: Экземпляр базового игрового объекта.
    """
    return _create_game_object('GameObject', _the_snake)


@pytest.fixture
def snake(_the_snake):
    """Создать экземпляр класса Snake.

    Args:
        _the_snake: Импортированный модуль игры.

    Returns:
        Snake: Экземпляр змейки.
    """
    return _create_game_object('Snake', _the_snake)


@pytest.fixture
def apple(_the_snake):
    """Создать экземпляр класса Apple.

    Args:
        _the_snake: Импортированный модуль игры.

    Returns:
        Apple: Экземпляр яблока.
    """
    return _create_game_object('Apple', _the_snake)


class StopInfiniteLoop(Exception):
    """Исключение для принудительного завершения игрового цикла."""


def loop_breaker_decorator(func):
    """Ограничить количество вызовов функции двумя.

    Args:
        func (callable): Функция, вызовы которой необходимо ограничить.

    Returns:
        callable: Функция-обёртка со счётчиком вызовов.

    Raises:
        StopInfiniteLoop: Если количество вызовов превышает два.
    """
    call_counter = 0

    def wrapper(*args, **kwargs):
        """Вызвать функцию и увеличить счётчик её вызовов.

        Args:
            *args: Позиционные аргументы функции.
            **kwargs: Именованные аргументы функции.

        Returns:
            Any: Результат выполнения исходной функции.
        """
        result = func(*args, **kwargs)
        nonlocal call_counter
        call_counter += 1

        if call_counter > 1:
            raise StopInfiniteLoop

        return result

    return wrapper


@pytest.fixture
def modified_clock(_the_snake):
    """Временно заменить игровой таймер на таймер с ограничением вызовов.

    Args:
        _the_snake: Импортированный модуль игры.

    Yields:
        None: Управление тесту с временно заменённым таймером.
    """

    class _Clock:
        """Обёртка над таймером Pygame для ограничения игрового цикла."""

        def __init__(self, clock_obj: Clock) -> None:
            """Сохранить исходный объект таймера.

            Args:
                clock_obj (Clock): Исходный таймер Pygame.
            """
            self.clock = clock_obj

        @loop_breaker_decorator
        def tick(self, *args, **kwargs):
            """Вызвать метод tick исходного таймера.

            Args:
                *args: Позиционные аргументы метода tick.
                **kwargs: Именованные аргументы метода tick.

            Returns:
                int: Время в миллисекундах с предыдущего вызова.
            """
            return self.clock.tick(*args, **kwargs)

        def __getattribute__(self, name: str) -> Any:
            """Получить атрибут обёртки или исходного таймера.

            Args:
                name (str): Название запрашиваемого атрибута.

            Returns:
                Any: Значение запрашиваемого атрибута.
            """
            if name in ['tick', 'clock']:
                return super().__getattribute__(name)

            return self.clock.__getattribute__(name)

    original_clock = _the_snake.clock
    modified_clock_obj = _Clock(original_clock)
    _the_snake.clock = modified_clock_obj

    yield

    _the_snake.clock = original_clock
