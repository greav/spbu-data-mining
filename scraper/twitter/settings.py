BOT_NAME = 'twitter'

SPIDER_MODULES = ['twitter.spiders']
NEWSPIDER_MODULE = 'twitter.spiders'

ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 1
# CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

DEFAULT_REQUEST_HEADERS = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
    'Host':
        "twitter.com",
    'Accept':
        "application/json, text/javascript, */*; q=0.01",
    'Accept-Language':
        "en-US,en;q=0.5",
    'X-Requested-With':
        "XMLHttpRequest",
    'Connection':
        "keep-alive"
}

# CLOSESPIDER_ITEMCOUNT = 200000

RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408, 429]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
}

PROXY_LIST = '/home/viktor_tolmachev/Projects/Information-Retrieval/scraper/proxies.txt'

PROXY_MODE = 0

ITEM_PIPELINES = {
    'twitter.pipelines.DataGatherPipeline': 300,
    'twitter.pipelines.FileSavePipeline': 400
}

SAVE_PATH = {'tweets': './data/raw/'}
