# Memento - Meme organizer
Organize your memes by having the window to:

- Fix the meme orientation
- Fetching the OCR from the meme and renaming the particular image with the initial 60 characters 
- Option to track all text from the image and store in `/OCR-text/`
- Using OpenCV to segment Image and text to get the recognized text to edit the meme and store in `/Memento/`
- Single or multiple option choosing support

**Demo run:**  <a href="https://youtu.be/5Zt52ZxJJ0Y" target="_blank"> Youtube</a> 

**Currently in beta state**

[![memento features](https://i.imgur.com/A8nZo21.gif)](https://youtu.be/5Zt52ZxJJ0Y)

**Note:**
Make sure you have a OCR tool like `tesseract` and certain data value for comparing OCR, eg `tesseract-data-eng` along with `Pillow` and `Wand` for image conversion and loading to draw along with `numpy` and `cv2` for all Image processing required to crop the image with border values defined

## Installation

Install using PIP:
```
$ sudo pip install mementor
$ memento <dirname>
```
***else***

Clone the source locally:
```
$ git clone https://github.com/aryaminus/memento
$ cd memento
$ git checkout feature/CV-UI
$ python3 memento.py <dirname>
```
## Stepwise working
<p align="center">
    <img src="https://i.imgur.com/8w5kADL.png">
<p>

## Todo
- [x] Fix for subprocess to accept spaced directories
- [x] Add choice to fetch full OCR text
- [x] String stream to allow user to choose the particular feature of memento
- [x] Using OpenCV to partition image and text section to edit the text
- [ ] Listing the images in the directory to edit a particular image only
- [ ] Apply NLTK with window to edit the fetched text to modify and fix typos in meme
- [ ] Apply Classification to organize the memes baised on the image category template for prediction model
- [ ] Add GUI with tkinter to attach text to a meme image

## Reference
1. <a href="https://github.com/lucab85/PDFtoTXT" target="_blank">PDFtoTXT</a>
2. <a href="https://github.com/pySushi/OCR" target="_blank">OCR</a>
3. <a href="https://github.com/aryaminus/saram" target="_blank">Saram</a>
4. <a href="https://github.com/evmarts/meme-maker" target="_blank">Meme-maker</a>


-----------------------------------------------------------------------------------------------------------

## Contributing

1. Fork it (<https://github.com/aryaminus/memento/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

**Enjoy!**