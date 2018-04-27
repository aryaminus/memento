# Memento - Meme organizer
Organize your memes by fetching the OCR from the meme and renaming it with the initial 60 characters with option to track all text from the image and store in `/OCR-text/` folder thus allowing to not only use `memento` for meme but for other scenarios too.

**Currently in alpha state**

[![memento features](https://i.imgur.com/wIFPRtU.gif)](https://i.imgur.com/wIFPRtU.gif)

**Note:**
Make sure you have a OCR tool like `tesseract` and certain data value for comparing OCR, eg `tesseract-data-eng` along with `Pillow` and `Wand` for image conversion and loading.

## Installation

Clone the source locally:
```
$ git clone https://github.com/aryaminus/memento
$ cd memento
$ git checkout feature/ocr
$ python main.py <dirname>
```

## Todo
- [x] Fix for subprocess to accept spaced directories
- [x] Add choice to fetch full OCR text into `/OCR-text/` directory
- [ ] Apply NLTK with window to edit the fetched text to modify and fix typos in meme
- [ ] Add GUI with tkinter to attach text to a meme image

## Reference
1. <a href="https://github.com/lucab85/PDFtoTXT" target="_blank">PDFtoTXT</a>
2. <a href="https://github.com/pySushi/OCR" target="_blank">OCR</a>
3. <a href="https://github.com/aryaminus/saram" target="_blank">Saram</a>


-----------------------------------------------------------------------------------------------------------

## Contributing

1. Fork it (<https://github.com/aryaminus/memento/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

**Enjoy!**