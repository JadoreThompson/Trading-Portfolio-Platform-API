from fastapi import Request


class DoesNotExist(Exception):
    """
    Resource does not exist
    e.g. User, Trade
    """
    def __init__(self, resource: str):
        self.resource = resource
        self.message = f"{resource} does not exist"
        super().__init__(self.message)
