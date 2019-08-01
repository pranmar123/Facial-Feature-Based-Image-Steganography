# Multi-Facial-Steganography

<Title of REU Project>
=================


Information
-----------

LSBSteg module is based on OpenCV to hide data in images. It uses the first bit of every pixel, and every colour
of an image. The code is quite simple to understand; If every first bit has been used, the module starts using the second bit, so the larger the data, the more the image is altered.
The program can hide all of the data if there is enough space in the image. The main functions are:

* encode_text: You provide a string and the program hides it


JPEG and otehr lossy compression formats are not supported. 

Installation
------------

This tool only require OpenCV and its dependencies.

```bash
pip install -r requirements.txt
```

Usage
-----
