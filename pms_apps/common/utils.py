import random
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from remedizz.config import Configurations
from remedizz.constants import Constants
from typing import Union


class Utils:
    def __init__(self):
        super().__init__()
        self.validation_error = Constants.validation_error

    @staticmethod
    def success_response_data(message, data: Union[list, dict] = None, image=False):
        if image:
            return message
        if data is None and message is None:
            return {'status': True}
        if message is None:
            return {'status': True, 'data': data}
        if data is None:
            return {'status': True, 'message': message}
        return {'status': True, 'message': message, 'data': data}

    @staticmethod
    def error_response_data(message: str, error: list[str]):
        return {'status': False, 'message': message, 'error': error}

    @staticmethod
    def env_exception_handler(message: str):
        if Configurations.debug:
            return message
        return Constants.server_error

    @staticmethod
    def add_page_parameter(final_data: list, page_num: int, total_page: int, total_count: int, present_url: str,
                           next_page_required: bool = False):
        to_return = {
            'data': final_data,
            'presentPage': page_num,
            'totalPage': total_page,
            'totalCount': total_count
        }
        if next_page_required and total_page > 1:
            if 'pageNum' in present_url:
                to_return['nextPageUrl'] = present_url.replace('pageNum=' + str(page_num),
                                                               'pageNum=' + str(page_num + 1))
            else:
                if '?' in present_url:
                    params, base_url = Utils.extract_params(url=present_url)
                    present_url = base_url + '?' + '&'.join(params)
                    to_return['nextPageUrl'] = present_url + '&pageNum=' + str(page_num + 1)
                else:
                    to_return['nextPageUrl'] = present_url + '?pageNum=' + str(page_num + 1)
        return to_return

    @staticmethod
    def extract_params(url: str):
        query = url.split('?')
        if len(query) > 1:
            info = query[1]
        else:
            info = 'pageNum=1'
        return info.split('&'), query[0]

    @staticmethod
    def get_query_params(request: Request):
        query_params = {}
        try:
            url = request.get_full_path()
        except:
            url = request.path
        query, base_url = Utils.extract_params(url=url)
        for i in query:
            try:
                key, value = i.split('=')
            except:
                key = i
                value = ''
            query_params[key] = value
        return query_params

    def validator(self, serializer):
        if serializer.is_valid() is False:
            response_data = Utils.error_response_data(
                message=self.validation_error, error=[serializer.errors]
            )
            return Response(response_data, status.HTTP_400_BAD_REQUEST)
        return True

    @staticmethod
    def generate_otp(length: int = 6):
        """Generate a numeric OTP of the specified length."""
        if length < 4:
            raise ValueError("OTP length should be at least 4.")
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
