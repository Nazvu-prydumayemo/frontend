class APIError(Exception):
    """
    - Used as base class of all API Errors
    """

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(f"[{status_code}] {message}")
