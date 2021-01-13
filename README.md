 # SPbU Data Mining

 Simple ML project based on [The Most Followed Accounts on Twitter analysis](https://www.brandwatch.com/blog/most-twitter-followers/)

## Scraping

Data was obtained using [scrapy web crawler](https://scrapy.org/). To reproduce results you need to do the following:

1. Create file `users.txt` (in scraper folder) on each file of which should be a username.

    For example:
    ```
    jimmyfallon
    Cristiano
    narendramodi
    ```
2. Go to the scraper dir and run the following command:
    ```
    scrapy crawl twitter -a users_file=users.txt
    ```

3. The data will be located in the folder specified by SAVE_PATH variable in `settings.py`. For each user, the scraper will create jsonl file (for example, `jimmyfallon.jsonl`)

You can find and download scrapped and preprocessed data [here](https://drive.google.com/drive/folders/1JymKlpfqpqZxmh0XNrkqZtlBRLRLWr67?usp=sharing)

## Basic preprocessing

Basic preprocessing class located in `src/utils/preprocessing.py` script.

To do basic preprocessing run the following command:
```
make basic_preprocess
```
It will create a preprocessed file in `data/interim` folder.

Preprocessing is also demonstrated in `notebooks/001-Basic-Text-Preprocessing.ipynb` [nbviewer](https://nbviewer.jupyter.org/github/greav/spbu-data-mining/blob/main/notebooks/001-Basic-Text-Preprocessing.ipynb)

## EDA

Basic EDA is located in ``notebooks/002-EDA.ipynb`` [nbviewer](https://nbviewer.jupyter.org/github/greav/spbu-data-mining/blob/main/notebooks/002-EDA.ipynb)

## Training

Basic training examples (Logreg, SVC, KNN, LDA, KMeans) are located in `notebooks/003-Training.ipynb` [nbviewer](https://nbviewer.jupyter.org/github/greav/spbu-data-mining/blob/main/notebooks/003-Training.ipynb)
