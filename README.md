Convertio APIs Client Library for Python
=======================

Inspired by the original [PHP Package](https://github.com/convertio/convertio-php) but Pythonic.

This is a lightweight wrapper for the [Convertio](https://convertio.co/api/) API.

Feel free to use, improve or modify this wrapper! If you have questions contact us or open an issue on GitHub.

Requirements
-------------------
* [Python 3.8 or above](https://www.python.org/downloads/)

Developer Documentation
-------------------
You can find full API reference here: https://convertio.co/api/docs/

Quickstart
-------------------
Initialize `convertio` client:
```python
import os
from convertio import client

convertio = client.ConvertIO(api_key=os.environ.get('CONVERTIO_API_KEY'))
```

Following example will convert PNG file to PDF:
```python
from convertio.models import parameters

# Example of converting a file
payload = parameters.NewConversionParameters(
    file="https://files.jotform.com/jotformapps/proforma-invoice-template-18a679482c789d2acf0db2d6f9324d94_og.png",
    outputformat="PDF"
)
response = convertio.new_conversion(payload=payload)
```

OCR Quickstart
-------------------
Following example will convert pages 1-3,5,7 of PDF into editable DOCX, using OCR (Optical Character Recognition) for English and Arabic languages (<a href="https://convertio.co/api/docs/#ocr_langs">Full list of available languages</a>):
```python
from convertio.models import parameters
from convertio.languages import Languages

# OCR Example
OCR_SETTINGS = parameters.OCRParameters.OCRSettings(langs=[Languages.ARABIC.value, Languages.ENGLISH.value])
payload = parameters.NewConversionParameters(
    file="https://files.jotform.com/jotformapps/proforma-invoice-template-18a679482c789d2acf0db2d6f9324d94_og.png",
    outputformat="txt",
    options=parameters.OCRParameters(ocr_enabled=True, ocr_settings=OCR_SETTINGS)
)

response = convertio.new_conversion(payload=payload)
```

Installation
-------------------
You can use **poetry** or simply **pip**

#### pip
```bash
pip install convertio-python
```

#### Poetry
```bash
poetry add convertio-python
```

Resources
---------
* [Source Code](https://github.com/BeleganStartup/convertio-python)
* [API Documentation](https://convertio.co/api/docs/)
* [Conversion Types](https://convertio.co/formats)