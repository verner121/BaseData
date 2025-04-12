class RequestsAPIError(Exception):
    """
    Класс пользовательского исключения при ошибках API запросов
    """

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message)
