#from distutils.core import setup
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name = 'mementor',
    packages = ['mementor'], # this must be the same as the name above
    version = '1.0.1',
    description = 'A library to fetch images from directory to fix orientation and pull OCR from the images along with editing the text inside images, primarily focusing on memes',
    long_description = readme(),
    author = 'Sunim Acharya',
    author_email = 'sunim.54@gmail.com',
    url = 'https://github.com/aryaminus/memento', # use the URL to the github repo
    keywords = ['ocr', 'image', 'opencv', 'tesseract', 'orientation'], # arbitrary keywords
    classifiers = [],
    install_requires=[
        'pillow', 'pyocr', 'numpy'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
    'console_scripts': [
        'memento = mementor.memento:start'
    ]},
)