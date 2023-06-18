Convertio APIs Client Library for Python
=======================

Inspired by the original [PHP Package](https://github.com/convertio/convertio-php) but Pythonic.

This is a lightweight wrapper for the [Convertio](https://convertio.co/api/) API.

Feel free to use, improve or modify this wrapper! If you have questions contact us or open an issue on GitHub.

Requirements
-------------------
* [Python 3.9 or above](https://www.python.org/downloads/)

Developer Documentation
-------------------
You can find full API reference here: https://convertio.co/api/docs/

Quickstart
-------------------
Following example will render remote web page into PNG image:
```python

```

Following example will convert local DOCX file to PDF:
```python

```

Following example will extract clean text from DOCX:
```python

```

Following example will override default API parameters in case you don't have SSL enabled in your PHP installation or want to limit execution time:
```python

```

OCR Quickstart
-------------------
Following example will convert pages 1-3,5,7 of PDF into editable DOCX, using OCR (Optical Character Recognition) for English and Arabic languages (<a href="https://convertio.co/api/docs/#ocr_langs">Full list of available languages</a>):
```python

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

Example with exceptions catching
-------------------
The following example shows how to catch the different exception types which can occur at conversions:

```python

```

Example of conversion process with callback URL
-------------------
The following example is usable for conversions that is not instant and may require some time to complete. 
In this case you may define the callback URL (<a href="https://convertio.co/api/docs/#options_callback">More info</a>), which gets notified when the conversion is over (either successful or not):

##### Start conversion:
```python

```
##### Callback handler example:
The exception handling in this code snippet is essential. Conversion errors throw APIException which have to be handled properly. Please, read <a href="https://convertio.co/api/docs/#options_callback">more info about step parameter</a>.  
```python

```


Example of conversion process being split on steps
-------------------
The following example is usable for conversions that is not instant and may require some time to complete. 
In this case you may get the conversion ID and check the conversion status later, omitting "->wait()" call and making conversion starting process instant:

##### Start conversion:
```python

```
##### Check conversion status and download the result:
The exception handling in this code snippet is essential. Conversion errors throw APIException which have to be handled properly.  
```python

```

Resources
---------

* [API Documentation](https://convertio.co/api/docs/)
* [Conversion Types](https://convertio.co/formats)