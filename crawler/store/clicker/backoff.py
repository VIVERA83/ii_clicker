import logging
from time import sleep, monotonic
from functools import wraps
from random import randint
from typing import Any, Callable

__all__ = ["before_execution"]


def delta_time() -> float:
    """Возвращает случайное число в миллисекундах.

    Применяется для того что бы минимизировать вероятность одномоментного
    обращение к одному сервису большого количества обращений.
    """
    return randint(100, 1000) / 1000


def before_execution(
        total_timeout=10,
        request_timeout: int = 3,
        logger: logging.Logger = logging.getLogger(name="before_execution"),
        raise_exception: bool = True,
) -> Any:
    """Декоратор, который пытается выполнить входящий вызываемый объект.

    В течении определенного времянки которое указано в параметре `total_timeout`,
    пытается выполнить функцию или другой вызываемый объект.
    В случае неудачной попытки, засыпает на время указанное в `request_timeout` + delta_time(),
    и делает следующею попытку до тех пор, пока не наступит одно из событий:
        1. Общее время выполнения превысило `total_timeout`, и тогда возвращается None
        2. Вызываемый объект `func` выполнился, и тогда возвращается результат выполнения `func`.
    `raise_exception` - True: в конце выполнения функции при неблагоприятных условии инициализируется исключение.
                      - False: в конце выполнения функции при неблагоприятных условии вернется None
    Неудачная попытка выводится в лог. В качестве люггера по умолчанию можно использовать logguru
    https://pypi.org/project/loguru/
    """

    def func_wrapper(func: Callable):

        @wraps(func)
        def inner(*args, **kwargs):
            # по сути засекаем время которое будет работать цикл
            error = None
            start = monotonic()
            while start + total_timeout > monotonic():
                try:
                    result = func(*args, **kwargs)
                    logger.info(f" success execution: {func.__name__}")
                    return result
                except Exception as ex:
                    error = ex
                    sec = randint(2, 4) + delta_time()
                    msg = (
                        f" an update error occurred...\n"
                        f" location: before_execution,  \n"
                        f" nested function: {func}\n"
                        f" Exception: {ex}\n"
                        f" next attempt to execute via: {sec} sec\n"
                        f" task: {func.__name__}\n"
                    )
                    logger.error(msg)
                    sleep(sec)
            logger.warning(f" Failed to execute: {func.__name__}", )
            if raise_exception:
                raise error
            return None

        return inner

    return func_wrapper


def create_link(params: dict[str, Any]):
    return "?" + "&".join([f"{k}={v}" for k, v in params.items()])


if __name__ == "__main__":
    print(create_link({"a": 1, "b": 2}))