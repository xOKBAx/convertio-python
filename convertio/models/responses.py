"""Base Models"""
# pylint: disable=too-few-public-methods
import os
from typing import Optional, List
import base64

import pydantic


class ErrorResponse(pydantic.BaseModel):
    """ Error Response

    Args:
        code (int): HTTP Status Code
        status (str): Always 'error' on Error
        error (str): User-friendly Error String
    """
    code: int
    status: str
    error: str


class BaseSuccessResponse(pydantic.BaseModel):
    """ Base Success Response

    Args:
        code (int): HTTP Status Code
        status (str): Always 'ok' on Error
    """
    code: int
    status: str


class NewConversionResponse(BaseSuccessResponse):
    """ Start a New Conversion

    Args:
        code (int): HTTP Status Code
        status (str): Always 'ok' on Error
        data (Data): Result data
    """

    class Data(pydantic.BaseModel):
        """ Data

        Args:
            id (str): Your Conversion ID
            minutes (int): API conversion minutes available on the balance
        """
        id: str
        minutes: int

    data: Data


class DirectFileResponse(BaseSuccessResponse):
    """ Direct File Upload For Conversion

    Args:
        code (int): HTTP Status Code
        status (str): Always 'ok' on Error
        data (Data): Result data
    """

    class Data(pydantic.BaseModel):
        """ Data

        Args:
            id (str): Your Conversion ID
            file (str): Filename of your file
            size (str): Size of uploaded file in Bytes
        """
        id: str
        file: str
        size: str

    data: Data


class GetStatusResponse(BaseSuccessResponse):
    """ Get Status of the Conversion

    Args:
        code (int): HTTP Status Code
        status (str): Always 'ok' on Error
        data (Data): Result data
    """

    class Data(pydantic.BaseModel):
        """ Data

        Args:
            id (str): Your Conversion ID
            step (str): Conversion Step. Allowed Values: wait,finish,convert,upload
            step_percent (int): Step Progress in %
            minutes (int): API Minutes used by this conversion
            output (Output): Output file information
        """

        class Output(pydantic.BaseModel):
            """ Output

            Args:
                url (str): URL of the file to download
                size (str): Size of the file in bytes
                files (Optional[dict]): If there are multiple output files
                            (i.e. converting a multi-page DOC to JPG) data.output
                            will contain a link to a ZIP file, which contains all output files.
                            If you would like to get the output files individual,
                            you can use data.output.url/file.ext,
                            where file.ext - is the name of the individual file
            """
            url: str
            size: str
            files: Optional[dict]

        id: str
        step: str
        step_percent: int
        minutes: int
        output: Output

    data: Data


class GetResultResponse(BaseSuccessResponse):
    """ Get Result File Content

    Args:
        code (int): HTTP Status Code
        status (str): Always 'ok' on Error
        data (Data): Result data
    """

    class Data(pydantic.BaseModel):
        """ Data

        Args:
            id (str): Your Conversion ID
            type (Optional[str]): Content encoding. Allowed Values: base64
            encode (Optional[str]): Content encoding. Allowed Values: base64
            content (str): Content of the file
        """
        id: str
        type: Optional[str]
        encode: Optional[str]
        content: bytes

        @pydantic.validator("content")
        @classmethod
        def validate_content(cls, value: bytes) -> base64.b64decode:
            """Valdiate content"""
            if not isinstance(value, bytes):
                raise ValueError(f'Expected a BytesIO object, found {type(value)}.')
            return base64.b64decode(value)

        class Config:
            """Config"""
            arbitrary_types_allowed = True

        def save(self, output_dir: str = '', *, file_name: str) -> str:
            """Save file to dir
            
            Args:
                output_dir (Optiona[str]): Directory where to save the file
                file_name (str): File name with extention, example: file.txt
            """
            with open(os.path.join(output_dir, file_name), 'wb') as file:
                file.write(self.content)

    data: Data


class DeleteCancelResponse(BaseSuccessResponse):
    """ Delete File/Cancel Conversion

    Args:
        code (int): HTTP Status Code
        status (str): Always 'ok' on Error
        message (str): User-friendly Error String
    """
    message: str


class ListConversionResponse(BaseSuccessResponse):
    """ List of Conversions

    Args:
        code (int): HTTP Status Code
        status (str): Always 'ok' on Error
        data (List[Data]): Result data
    """

    class Data(pydantic.BaseModel):
        """ Data

        Args:
            id (str): Your Conversion ID
            status (str): Conversion Status.
                          Allowed Values:
                                uploading,
                                converting,
                                finished,
                                failed,
                                unknown.
            minutes (int): API Minutes used by this conversion
            inputformat (str): Input file format (detected by our converter)
            outputformat (str): Output file format (specified by the user)
            filename (str): File name, if applicable
            error (Optional[str]): User-friendly error string, in case of failed conversion
        """
        id: str
        status: str
        minutes: int
        inputformat: str
        outputformat: str
        filename: str
        error: Optional[str]

    data: List[Data]
