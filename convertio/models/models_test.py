"""Test Parameters"""
import unittest

from . import parameters, responses


# NOTE: Write test only for complex models


class TestParameters(unittest.TestCase):
    """Test ConverIO parameters"""

    def test_new_conversion_minimum(self):
        """Test NewConversionParameters with minimun values"""
        data = {
            "file": "test file",
            "outputformat": "txt"
        }
        new_conversion = parameters.NewConversionParameters(**data)

        self.assertDictEqual(
            new_conversion.dict(exclude_none=True),
            {"input": "url", **data}
        )

    def test_new_conversion_full(self):
        """Test NewConversionParameters all values"""
        data = {
            "file": "http://test_file_url",
            "filename": "test_file.pdf",
            "outputformat": "png",
            "options": {
                "ocr_enabled": True,
                "ocr_settings": {
                    "page_nums": "1,2,3",
                    "langs": ["ara", "heb"]
                }
            }
        }

        new_conversion = parameters.NewConversionParameters(**data)

        self.assertDictEqual(
            new_conversion.dict(),
            {"input": "url", **data}
        )


class TestResponses(unittest.TestCase):
    """Test ConverIO responses"""

    def test_get_status_minimun(self):
        """Test GetStatusResponse with minimum values"""
        data = {
            "code": 200,
            "status": "ok",
            "data": {
                "id": "abc",
                "step": "wait",
                "step_percent": 20,
                "minutes": 10,
                "output": {
                    "url": "http://output_url",
                    "size": '12'
                }
            }
        }

        get_conversion_status = responses.GetStatusResponse(**data)

        self.assertEqual(
            get_conversion_status.dict(exclude_none=True),
            data
        )

    def test_get_status_full(self):
        """Test GetStatusResponse with all values"""
        data = {
            "code": 200,
            "status": "ok",
            "data": {
                "id": "abc",
                "step": "wait",
                "step_percent": 20,
                "minutes": 10,
                "output": {
                    "url": "http://output_url",
                    "size": '12',
                    "files": {
                        "test": "exist"
                    }
                }
            }
        }

        get_conversion_status = responses.GetStatusResponse(**data)

        self.assertEqual(
            get_conversion_status.dict(exclude_none=True),
            data
        )


if __name__ == "__main__":
    unittest.main()
