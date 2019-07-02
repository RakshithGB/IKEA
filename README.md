# IKEA Scrapper + Classifier

A web scrapper written in `Selenium` using a chrome driver to scrape through IKEA US website for 4 unique product categories.

## Prerequisites

1. Selenium
2. BeautifulSoup - `pip install bs4`
3. Pyexcel - `pip install pyexcel`
4. Keras
5. Tensorflow
6. OpenCV
7. Scikit-Learn
8. Split-Folders - `pip install split-folders`

### Google Chrome Driver

1. Check google chrome browser version with this [link](https://www.whatismybrowser.com/detect/what-version-of-chrome-do-i-have).
2. Based on the version download the correct one from [here](http://chromedriver.chromium.org/downloads).
3. Please paste the correct Chrome Driver version in the correct OS folder.

**Example:**
If windows the final location: `IKEA-master/Driver/Windows/Chromedriver.exe`

## Scrapping

The first step is to scrape the website, this results in populating the folders in Downloads folder.

```bash
python scrapper.py
```

By default four classes namely: Bed, Chair, Lamp, Wardrobe will be downloaded. This can be modified at **line 22** keys variable. Necessary ignore keywords can also be added at **line 23** ignore variable.

## Cleaning

There could be a chances of junk images being downloaded, to clean this us and split the data into train, test and val (generated in Dataset):

```bash
python cleaner.py
```

## Training

Xception base network with a few extra layers are used to build the model. To train:

```bash
python trainer.py
```

The CNN is set to use 30 epoch by default with a batch size of 32. This can be changed in **line 22** and **line 23** respectively of **trainer.py** script.

## Evaluation

After training, the model can be evaluated with predictor.py script and the confusion matrix plotted:

```bash
python predictor.py
```

By default the evaluation is done on the “Test” set and can be changed to “Val” in **line 10** of **predictor.py**.

## Results

Accuracy: 93.75%

|  | **Bed** | **Chair** | **Lamp** | **Wardrobe** |
| --- | --- | --- | --- | --- |
| **Bed** | 17 | 0 | 0 | 0 |
| **Chair** | 1 | 20 | 0 | 0 |
| **Lamp** | 1 | 0 | 19 | 1 |
| **Wardrobe** | 1 | 1 | 0 | 19 |
