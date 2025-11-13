import json
import uuid

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from pms.config import Configurations
from pms.constants import Constants
from pms_apps.common.utils import Utils
# from kafka_consumer_producer.producer import KafkaTopicProducer


class SerializerValidations:

    def __init__(self, serializer, exec_func: str = ''):
        self.validation_error = Constants.validation_error
        self.serializer = serializer
        self.exec_func = exec_func
        self.message = "Request added to queue"

    def validate(self, func):
        def validator(*args, **kwargs):
            request: Request = args[0]

            if request.method in ['POST', 'PUT', 'PATCH']:
                data = json.loads(request.body)
            else:
                data = Utils.get_query_params(request=request)
            serializer = self.serializer(data=data)
            validator = Utils().validator(serializer=serializer)
            if isinstance(validator, bool):
                params = serializer.create(serializer.validated_data)
                request.params = params
                if Configurations.kafka['enable'] and request.method in ['POST', 'PUT', 'DELETE']:
                    key_id = str(uuid.uuid1())
                    # KafkaTopicProducer.push(path=request.build_absolute_uri(), method=request.method,
                    #                         body=request.body.decode('utf-8'),
                    #                         key=self.exec_func, uuid=key_id)
                    return Response(status=status.HTTP_202_ACCEPTED,
                                    data=Utils.success_response_data(message=self.message,
                                                                     data={'statusId': key_id}))
                return func(*args, **kwargs)
            return validator

        return validator
