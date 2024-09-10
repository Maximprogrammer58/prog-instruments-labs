import random

from typing import Any
from typing import Callable


def singleton(cls) -> Callable[[], Any]:
    """
    A decorator that ensures a class has only one instance.

    Args:
        cls (type): The class for which a single instance will be created.

    Returns:
        function: A function that returns the single instance of the class.
    """
    instances = {}

    def getinstance() -> Any:
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


def div_by_zero(x: float, y: float) -> float:
    """
    Divides x by y, returning 0 if y is zero.

    Args:
        x (float): The numerator.
        y (float): The denominator.

    Returns:
        float: The result of x divided by y or 0 if y is zero.
    """
    if y == 0:
        return 0
    else:
        return x / y


def limited_inc(base: float, limit: float, inc: float = 1) -> float:
    """
    Increases the value of base by inc, without exceeding limit.

    Args:
        base (float): The initial value.
        limit (float): The maximum allowable value.
        inc (float, optional): The increment. Defaults to 1.

    Returns:
        float: The new value, which does not exceed limit.
    """
    res = base + inc
    if res > limit:
        return limit
    else:
        return res


def random_mod(x: float, a: float) -> float:
    """
    Modifies x randomly within a%.

    Args:
        x (float): The original value.
        a (float): The percentage deviation.

    Returns:
        float: The modified value of x.
    """
    return x * (1 + float(random.randrange(-a, a)) / 100)
