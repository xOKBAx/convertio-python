"""ConvertIO Client tests"""
import unittest
from unittest import mock
import base64

import httpx

from . import client
from .languages import Languages
from .models import parameters


class TestConvertIOClient(unittest.TestCase):
    """Test ConvertIO Client"""
    def setUp(self) -> None:
        self.convertio_client = client.ConvertIO(api_key="test")
        self.httpx_request = mock.Mock()
        self.httpx_request_patcher = mock.patch.object(
            httpx,
            'request',
            new=self.httpx_request
        )
        self.httpx_request_patcher.start()

    def tearDown(self) -> None:
        self.httpx_request_patcher.stop()

    def mock_request(self, success: bool, expected_output: dict):
        """Mock Request"""
        response = mock.Mock()
        response.url = ""
        response.is_success = success
        response.json.return_value = expected_output
        self.httpx_request.return_value = response

    def test_new_conversion_fail(self):
        """test new_conversion response fail"""
        payload = parameters.NewConversionParameters(
            file="http://file_url",
            outputformat="png",
            options=parameters.OCRParameters(
                ocr_enabled=True,
                ocr_settings=parameters.OCRParameters.OCRSettings(
                    langs=[Languages.HEBREW.value]
                )
            )
        )
        expected_output = {
            "code": 401,
            "status": "error",
            "error": "This API Key is invalid"
        }

        self.mock_request(success=False, expected_output=expected_output)

        response = self.convertio_client.new_conversion(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    def test_new_conversion_success(self):
        """test new_conversion response success"""
        payload = parameters.NewConversionParameters(
            file="http://file_url",
            outputformat="png",
            options=parameters.OCRParameters(
                ocr_enabled=True,
                ocr_settings=parameters.OCRParameters.OCRSettings(
                    langs=[Languages.HEBREW.value]
                )
            )
        )
        expected_output = {
            "code": 200,
            "status": "ok",
            "data": {
                "id": "9712d01edc82e49c68d58ae6346d2013",
                "minutes": 107
            }
        }

        self.mock_request(success=True, expected_output=expected_output)

        response = self.convertio_client.new_conversion(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    @mock.patch('urllib.request.urlopen')
    def test_direct_file_upload_fail(self, _):
        """test direct_file_upload response fail"""
        payload = parameters.DirectFileParameters(
            id="9712d01edc82e49c68d58ae6346d2013",
            filename="file.png"
        )
        expected_output = {
            "code": 401,
            "status": "error",
            "error": "No convertion minutes left"
        }

        self.mock_request(success=False, expected_output=expected_output)

        response = self.convertio_client.direct_file_upload(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    @mock.patch('urllib.request.urlopen')
    def test_direct_file_upload_success(self, _):
        """test direct_file_upload response success"""
        payload = parameters.DirectFileParameters(
            id="9712d01edc82e49c68d58ae6346d2013",
            filename="file.png"
        )
        expected_output = {
            "code": 200,
            "status": "ok",
            "data": {
                "id": "9712d01edc82e49c68d58ae6346d2013",
                "file": "test.bmp",
                "size": "1025470"
            }
        }

        self.mock_request(success=True, expected_output=expected_output)

        response = self.convertio_client.direct_file_upload(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    def test_get_conversion_status_fail(self):
        """test get_conversion_status response fail"""
        payload = parameters.GetStatusParameters(
            id="9712d01edc82e49c68d58ae6346d2013"
        )
        expected_output = {
            "code": 422,
            "status": "error",
            "error": "Input file appears to be corrupted"
        }

        self.mock_request(success=False, expected_output=expected_output)

        response = self.convertio_client.get_conversion_status(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    def test_get_conversion_status_success(self):
        """test get_conversion_status response success"""
        payload = parameters.GetStatusParameters(
            id="9712d01edc82e49c68d58ae6346d2013"
        )
        expected_output = {
            "code": 200,
            "status": "ok",
            "data": {
                "id": "9712d01edc82e49c68d58ae6346d2013",
                "step": "finish",
                "step_percent": 100,
                "minutes": 1,
                "output": {
                    "url": ("https://lisa.convertio.me/d31c0ed50efd097e34c6b23fa555445d"
                            "/http-google-com_4.png"),
                    "size": "36102"
                }
            }
        }

        self.mock_request(success=True, expected_output=expected_output)

        response = self.convertio_client.get_conversion_status(payload=payload)

        self.assertDictEqual(
            response.dict(exclude_none=True),
            expected_output
        )

    def test_get_result_file_fail(self):
        """test get_result_file response fail"""
        payload = parameters.GetResultParameters(
            id="9712d01edc82e49c68d58ae6346d2013"
        )
        expected_output = {
            "code": 422,
            "status": "error",
            "error": ("File is not ready yet, finished with "
                      "errors or had been deleted (check file status)")
        }

        self.mock_request(success=False, expected_output=expected_output)

        response = self.convertio_client.get_result_file(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    def test_get_result_file_success(self):
        """test get_result_file response success"""
        payload = parameters.GetResultParameters(
            id="9712d01edc82e49c68d58ae6346d2013",
        )
        file_content = b"_FILE_CONTENT_"
        expected_output = {
            "code": 200,
            "status": "ok",
            "data": {
                "id": "9712d01edc82e49c68d58ae6346d2013",
                "encode": "base64",
                "content": base64.b64encode(file_content).decode()
            }
        }

        self.mock_request(success=True, expected_output=expected_output)

        response = self.convertio_client.get_result_file(payload=payload)

        expected_output["data"]["content"] = file_content # Reset to initial state

        self.assertDictEqual(
            response.dict(exclude_none=True),
            expected_output
        )

    def test_delete_or_cancel_conversion_fail(self):
        """test delete_or_cancel_conversion response fail"""
        payload = parameters.DeleteCancelParameters(
            id="9712d01edc82e49c68d58ae6346d2013"
        )
        expected_output = {
            "code": 404,
            "status": "error",
            "error": "File not found"
        }

        self.mock_request(success=False, expected_output=expected_output)

        response = self.convertio_client.delete_or_cancel_conversion(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    def test_delete_or_cancel_conversion_success(self):
        """test delete_or_cancel_conversion response success"""
        payload = parameters.DeleteCancelParameters(
            id="9712d01edc82e49c68d58ae6346d2013"
        )
        expected_output = {
            "code": 200,
            "status": "ok",
            "message": "File deleted"
        }

        self.mock_request(success=True, expected_output=expected_output)

        response = self.convertio_client.delete_or_cancel_conversion(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    def test_list_conversions_fail(self):
        """test list_conversions response fail"""
        payload = parameters.ListConversionParameters(
            status="finished",
            count=4
        )
        expected_output = {
            "code": 401,
            "status": "error",
            "error": "This API Key is invalid"
        }

        self.mock_request(success=False, expected_output=expected_output)

        response = self.convertio_client.list_conversions(payload=payload)

        self.assertDictEqual(
            response.dict(),
            expected_output
        )

    def test_list_conversions_success(self):
        """test list_conversions response success"""
        payload = parameters.ListConversionParameters(
            status="finished",
            count=4
        )
        expected_output = {
            "code": 200,
            "status": "ok",
            "data": [
                {
                    "id": "7d5c9dba440e618ed6eb1adae69c10d6",
                    "status": "finished",
                    "minutes": 1,
                    "inputformat": "DOC",
                    "outputformat": "PDF",
                    "filename": "report-94b97c5b.doc"
                },
                {
                    "id": "aa235eee271c5c4453890d7bca48b49a",
                    "status": "failed",
                    "minutes": 0,
                    "inputformat": "",
                    "outputformat": "PDF",
                    "filename": "report-9a497c5b.xlsb",
                    "error": ("CONVERTER: Can't determine Type of the "
                              "Input File [MIME: application/octet-stream]")
                },
                {
                    "id": "ce4d5442bd662b97c2a6456b3fa74b1d",
                    "status": "failed",
                    "minutes": 0,
                    "inputformat": "",
                    "outputformat": "MKV",
                    "filename": "video.avi",
                    "error": ("UPLOADER: Operation timed out after 600000 "
                              "milliseconds with 62290101 out of 72502797 bytes received")
                },
                {
                    "id": "712f2e88a46d3a0444e52cc7d7f602a6",
                    "status": "converting",
                    "minutes": 0,
                    "inputformat": "PDF",
                    "outputformat": "HTML",
                    "filename": "printable.pdf"
                }
            ]
        }

        self.mock_request(success=True, expected_output=expected_output)

        response = self.convertio_client.list_conversions(payload=payload)

        self.assertDictEqual(
            response.dict(exclude_none=True),
            expected_output
        )


if __name__ == "__main__":
    unittest.main()
