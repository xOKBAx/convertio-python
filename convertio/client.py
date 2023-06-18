"""
    ConvertIO Client
    For more details visit:
        https://developers.convertio.co/api/docs/
"""
from typing import Union
from urllib.parse import urljoin
import urllib.request
import logging

import httpx

from .models import parameters, responses


# Constants
REQUEST_TIMEOUT = 30

# ConvertIO Base URL
BASE_API_URL = 'http://api.convertio.co'

# API Endpoints
NEW_CONVERSION_ENDPOINT = '/convert'
DIRECT_FILE_ENDPOINT = '/convert/%s/%s' # '/convert/<id>/<filename>'
GET_STATUS_ENDPOINT = '/convert/%s/status' # '/convert/<id>/status'
GET_RESULT_ENDPOINT = '/convert/%s/dl/base64' # '/convert/<id>/dl/<OPTIONAL type>'
DELETE_CANCEL_ENDPOINT = '/convert/%s' # '/convert/<id>
LIST_CONVERSION_ENDPOINT = '/convert/list'


class ConvertIO: # pylint: disable=too-few-public-methods
    """ConvertIO Client"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def new_conversion(
        self,
        payload: parameters.NewConversionParameters
    ) -> Union[responses.NewConversionResponse, responses.ErrorResponse]:
        """
            Start a New Conversion
        
            Example Result:
                code=200
                status='ok'
                data=Data(id='5ad5ea6f719178beff43cca991ed1109', minutes=994)
        """
        url = urljoin(BASE_API_URL, NEW_CONVERSION_ENDPOINT)
        data = {"apikey": self.api_key, **payload.dict(exclude_none=True)}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = httpx.request(
            method='POST',
            url=url,
            headers=headers,
            json=data,
            timeout=REQUEST_TIMEOUT
        )
        logging.debug("new_conversion: %s %s %s", response, response.url, data)
        if response.is_success:
            return responses.NewConversionResponse(**response.json())
        return responses.ErrorResponse(**response.json())

    def direct_file_upload(
        self,
        payload: parameters.DirectFileParameters
    ) -> Union[responses.DirectFileResponse, responses.ErrorResponse]:
        """ Direct File Upload For Conversion

            This step required only if chooses input = 'upload' on previous step.
            In order to upload file for conversion.
        """
        url = urljoin(
            BASE_API_URL,
            DIRECT_FILE_ENDPOINT % (payload.id, payload.filename)
        )
        with urllib.request.urlopen(url) as response:
            data = response.read()
        response = httpx.request(
            method='PUT',
            url=url,
            json=data,
            timeout=REQUEST_TIMEOUT
        )
        logging.debug("direct_file_upload: %s %s %s", response, response.url, data)
        if response.is_success:
            return responses.DirectFileResponse(**response.json())
        return responses.ErrorResponse(**response.json())

    def get_conversion_status(
        self,
        payload: parameters.GetStatusParameters
    ) -> Union[responses.GetStatusResponse, responses.ErrorResponse]:
        """ Get Status of the Conversion

            In order to get status of a conversion you need to do this request
            with <id>, obtained on previous step.
        """
        url = urljoin(
            BASE_API_URL,
            GET_STATUS_ENDPOINT % payload.id
        )
        response = httpx.request(
            method='GET',
            url=url,
            timeout=REQUEST_TIMEOUT
        )
        logging.debug("get_conversion_status: %s %s", response, response.url)
        if response.is_success:
            return responses.GetStatusResponse(**response.json())
        return responses.ErrorResponse(**response.json())

    def get_result_file(
        self,
        payload: parameters.GetResultParameters
    ) -> Union[responses.GetResultResponse, responses.ErrorResponse]:
        """ Get Result File Content

            In order to get result file of a conversion you need to do the following request.

            As an alternative to this step you may use output URL from previous step,
            but be advised, that this URL is bounded to the host IP address and
            can't be hotlinked or shared with third parties.
        """
        url = urljoin(
            BASE_API_URL,
            GET_RESULT_ENDPOINT % payload.id
        )
        response = httpx.request(
            method='GET',
            url=url,
            timeout=REQUEST_TIMEOUT
        )
        logging.debug("get_result_file: %s %s", response, response.url)
        if response.is_success:
            return responses.GetResultResponse(**response.json())
        return responses.ErrorResponse(**response.json())

    def delete_or_cancel_conversion(
        self,
        payload: parameters.DeleteCancelParameters
    ) -> Union[responses.DeleteCancelResponse, responses.ErrorResponse]:
        """Delete File/Cancel Conversion"""
        url = urljoin(
            BASE_API_URL,
            DELETE_CANCEL_ENDPOINT % payload.id
        )
        response = httpx.request(
            method='DELETE',
            url=url,
            timeout=REQUEST_TIMEOUT
        )
        logging.debug("delete_or_cancel_conversion: %s %s", response, response.url)
        if response.is_success:
            return responses.DeleteCancelResponse(**response.json())
        return responses.ErrorResponse(**response.json())

    def list_conversions(
        self,
        payload: parameters.ListConversionParameters
    ) -> Union[responses.ListConversionResponse, responses.ErrorResponse]:
        """
            List of Conversions

            Example Result:
                code=200
                status='ok'
                data=[
                    Data(
                        id='5ad5ea6f719178beff43cca991ed1109',
                        status='finished',
                        minutes=1,
                        inputformat='PNG',
                        outputformat='JPEG',
                        filename='SCAN_20140710_090651322.png',
                        error=None
                    )
                ]    
        """
        url = urljoin(BASE_API_URL, LIST_CONVERSION_ENDPOINT)
        data = {"apikey": self.api_key, **payload.dict(exclude_none=True)}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        response = httpx.request(
            method='POST',
            url=url,
            headers=headers,
            json=data,
            timeout=REQUEST_TIMEOUT
        )
        logging.debug("list_conversions: %s %s %s", response, response.url, data)
        if response.is_success:
            return responses.ListConversionResponse(**response.json())
        return responses.ErrorResponse(**response.json())
