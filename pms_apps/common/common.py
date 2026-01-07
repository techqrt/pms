from rest_framework import status
from rest_framework.response import Response
import jwt
from pms_apps.helper_apis.models.city import City
from pms.constants import Constants
from pms_apps.common.exceptions.token_errors import TokenErrors
from pms_apps.common.exceptions.validation_errors import ValidationErrors
from pms_apps.common.utils import Utils
from rest_framework.exceptions import ValidationError


class Common:
    def __init__(self, response_handler=None):
        self.db_error = "Database Error"
        self.error = "Something went wrong"
        self.file_error = "File Error"
        self.token_error = "Unauthorized"
        self.foreign_key_error = "It is not possible to delete this record as it is connected with other records"
        self.response_handler = response_handler

    @staticmethod
    def mapper_value_error(mapped_column_names: dict, columns_required: list):
        for column in columns_required:
            if column not in mapped_column_names.values():
                raise ValueError(f'{column} not a proper column name')
            
    def country_city_validation(self,func):
        def wrapper(*args, **kwargs):
            params = kwargs.get("params")

            city_id = getattr(params, 'city_id', None)
            country_id = getattr(params, 'country_id', None)

            if city_id and country_id:
                if not City.objects.filter(
                    city_id=city_id,
                    country_id=country_id
                ).exists():
                    raise ValidationError("City does not belong to country")

            return func(*args, **kwargs)
        return wrapper
    
    def exception_handler(self, func):
        def exceptions(*args, **kwargs):
            try:
                fun = func(*args, **kwargs)
                if self.response_handler is not None:
                    serializer = self.response_handler(data=fun.data)
                    serializer.is_valid(raise_exception=True)
            except ValueError as e:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=Utils.error_response_data(message='Value Error ' + str(e), error=[str(e)])
                )
            except FileExistsError as e:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=Utils.error_response_data(message='File Error ' + str(e), error=[self.file_error])
                )
            except ValidationErrors as e:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=Utils.error_response_data(message=Constants.validation_error, error=e.errors)
                )
            except TokenErrors as e:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data=Utils.error_response_data(message=self.token_error, error=e.errors)
                )
            except jwt.exceptions.InvalidSignatureError:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data=Utils.error_response_data(
                        message=self.token_error,
                        error=["Signature Verification Error", "You have logged into another device"]
                    )
                )
            except Exception as e:
                if 'foreign key constraint' in str(e):
                    return Response(
                        status=status.HTTP_400_BAD_REQUEST,
                        data=Utils.error_response_data(
                            error=[self.foreign_key_error],
                            message='Foreign Key Error ' + Utils.env_exception_handler(message=str(e))
                        )
                    )
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data=Utils.error_response_data(
                        error=[self.db_error],
                        message='Exception Error ' + Utils.env_exception_handler(message=str(e))
                    )
                )
            return fun
        return exceptions
