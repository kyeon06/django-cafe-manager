from rest_framework.response import Response
from rest_framework import status

# Custom Response Format
class CustomResponse(Response):
    def __init__(self, data=None, code=None, message=None, status=None, **kwargs):
        super().__init__(**kwargs)
        self.status = status or status.HTTP_200_OK
        self.code = code or self.status
        self.message = message or 'ok'
        self.data = {
            'meta' : {
                'code' : self.code,
                'message' : self.message,
            },
            "data" : data or None
        }

        self.status_code = self.status
        self.content_type = kwargs.get('content_type', None)