To use (with caution), simply do::

    $ pip install mementor
    $ memento <dirname>

Make sure you have a OCR tool like `tesseract` and certain data value for comparing OCR, eg `tesseract-data-eng` along with `Pillow` and `Wand` for image conversion and loading to draw along with `numpy` and `cv2` for all Image processing required to crop the image with border values defined which will be fetched during pip install.