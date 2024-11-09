import logging


def setup_logging() -> None:
    """Настраивает базовую конфигурацию логирования.

    Устанавливает уровень логирования на INFO и задает формат сообщений.
    Сообщения будут выводиться в стандартный поток вывода.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
