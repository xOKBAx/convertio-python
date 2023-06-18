"""Conversion models"""
# pylint: disable=too-few-public-methods
from typing import Optional
from enum import Enum

import pydantic


class AllowedConversionInputs(Enum):
    """Allowed conversion inputs"""
    URL = "url"
    RAW = "raw"
    BASE64 = "base64"
    UPLOAD = "upload"


class GetResultsInputs(Enum):
    """Get results inputs"""
    NONE = ""
    BASE64 = "base64-encoded"


class ConversionStatus(Enum):
    """Conversion Status"""
    ALL = "all"
    UPLOADING = "uploading"
    CONVERTING = "converting"
    FINISHED = "finished"
    FAILED = "failed"


class OCRParameters(pydantic.BaseModel):
    """ Conversion Options [OCR]
    
    Args:
        ocr_enabled (Optional[bool]): Setting it to true enables OCR
        ocr_settings (Optional[Settings]): Required, if ocr_enable = True
    """
    class OCRSettings(pydantic.BaseModel):
        """ Settings
        
        Args:
            page_nums (Optional[str]): Page numbers to extract from input file.
                                        Rich syntax supported, i.e.: "1-3,5,7-9,4"
            langs (list): This is the array of language codes.
                            The more languages you set - the slower the recognition.
                            Use the minimal set you can.
        """
        page_nums: Optional[str]
        langs: list

    ocr_enabled: Optional[bool]
    ocr_settings: Optional[OCRSettings]


class NewConversionParameters(pydantic.BaseModel):
    """ Start a New Conversion

    Args:
        input (AllowedConversionInputs):
                    Method of providing the input file. (default: url)
                     Allowed Values:
                        url,
                        raw,
                        base64,
                        upload
        file (str): URL of the input file (if input=url),
                    or file content (if input = raw/base64)
        filename (Optional[str]): Input filename including extension (file.ext).
                                  Required if input = raw/base64
        outputformat (str): Output format, to which the file should be converted to.
        options (Optional[OCRParameters]): Used to define callback URL,
                                  enable OCR and setting up its options.
                                  You may find available OCR conversion options here:
                                   https://developers.convertio.co/tr/api/docs/#options
                                  and callback example here:
                                   https://developers.convertio.co/tr/api/docs/#options_callback
    """
    file: str
    filename: Optional[str]
    outputformat: str
    options: Optional[OCRParameters]
    input: AllowedConversionInputs = AllowedConversionInputs.URL.value

    class Config:
        """Config"""
        use_enum_values = True


class DirectFileParameters(pydantic.BaseModel):
    """ Direct File Upload For Conversion

    Args:
        id (str): Conversion ID, obtained on POST call to /convert
        filename (str): Input filename including extension (file.ext)
    """
    id: str
    filename: str


class GetStatusParameters(pydantic.BaseModel):
    """ Get Status of the Conversion

    Args:
        id (str): Conversion ID, obtained on POST call to /convert
    """
    id: str


class GetResultParameters(pydantic.BaseModel):
    """ Get Result File Content

    Args:
        id (str): Conversion ID, obtained on POST call to /convert
        type (Optional[str]): File Format, always base64-encoded.
                              Allowed Values:
                                <empty value>
                                base64
    """
    id: str


class DeleteCancelParameters(pydantic.BaseModel):
    """ Delete File/Cancel Conversion

    Args:
        id (str): Conversion ID, obtained on POST call to /convert
    """
    id: str


class ListConversionParameters(pydantic.BaseModel):
    """ List of Conversions

    Args:
        status (ConversionStatus):
                    Filter by file status. Default Value: all
                      Allowed Values:
                        all,
                        uploading,
                        converting,
                        finished,
                        failed
        count (int): Latest {count} files
    """
    status: ConversionStatus = ConversionStatus.ALL.value
    count: int

    class Config:
        """Config"""
        use_enum_values = True
