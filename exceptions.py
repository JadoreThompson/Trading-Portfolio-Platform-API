from fastapi import Request


class DoesNotExist(Exception):
    def __init__(self, request: Request, resource: str):
        self.request = request
        self.resource = resource
        self.message = f"{resource} does not exist"
        super().__init__(self.message)