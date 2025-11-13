import json
import uuid

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from pms.config import Configurations
from pms.constants import Constants
from pms_apps.common.utils import Utils

class SerializerValidations:

    def __init__(self, serializer, exec_func: str = ''):
        self.validation_error = Constants.validation_error
        self.serializer = serializer
        self.exec_func = exec_func
        self.message = "Request added to queue"

    def validate(self, func):
        def validator(*args, **kwargs):
            request: Request = args[0]

            
            data = request.data
            data.update(Utils.get_query_params(request=request))
            serializer = self.serializer(data=data)
            print(serializer.is_valid())
            validator = Utils().validator(serializer=serializer)
            if isinstance(validator, bool):
                params = serializer.create(serializer.validated_data)
                request.params = params
                if request.method == 'GET': request.params.present_url = request.build_absolute_uri()
                request.params.user_id = request.user.user_id

                return func(*args, **kwargs)
            return validator

        return validator
