import json

import scrapy
from scrapy.selector import Selector


class TwiterUserSpider(scrapy.Spider):
    name = "twitter"
    allowed_domains = ["twitter.com"]

    def __init__(self, users_file=None):
        self.query = 'https://twitter.com/i/search/timeline?' \
                  'f=tweets&vertical=news&q=from:{user}' \
                  '&src=typd&&include_available_features=1' \
                  '&include_entities=1&max_position={page_position}' \
                  '&reset_error_state=false'

        self.users_page_position = self._read_users_file(users_file)

    def start_requests(self):
        for user, page_position in self.users_page_position.items():
            url = self.query.format(user=user, page_position=page_position)
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['user'] = user
            yield request

    def parse(self, response):
        """Parses a response.

        Args:
            response (object): response received from the scraper.

        Yields:
            dict: scrapy item to be processed.
        """
        user = response.meta['user']

        try:
            raw_data = json.loads(response.body)
        except json.decoder.JSONDecodeError:
            self.logger.exception(f'Error during decoding json for {user}')
            return

        html_page = Selector(text=raw_data['items_html'])
        page_position = raw_data['min_position']
        self.users_page_position[user] = page_position

        yield from self._yield_tweets(user, html_page)

        if not raw_data['has_more_items']:
            self.logger.info(
                f'There are no more items for {user}. Scraping stopped.')
            return

        yield from self._load_scroll_content(user, response, page_position)

    def _load_scroll_content(self, user, response, page_position=None):
        """Generates request based on the user, previous response
            and page position.

        Args:
            user (str): user to be scraped:
            response (object): previous received response.
            page_position (str, optional): position from which to start
                scraping. Defaults to None.

        Yields:
            object: scrapy.Request
        """
        url = self.query.format(user=user, page_position=page_position)

        request = scrapy.Request(url=url, callback=self.parse)
        request.meta['user'] = user
        yield request

    def _yield_tweets(self, user, response):
        for tweet in response.css('div.tweet'):
            yield {'tweet': tweet, 'user': user}

    def _read_users_file(self, users_file):
        """Reads users to be scraped from the file passed to a scraper.

        The file has the following format:
            user1 `min_position`
            user2 `min_position`
            user3
            ...

        Position argument can be ommited (if ommited, a spider will scrap from
            the first tweet)

        Args:
            users_file (str): path to the file.

        Returns:
            dict: object whose keys are users, and the values are the position
            from which spider will be scraping.
        """
        users_page_position = {}
        with open(users_file) as f:
            for line in f:
                line = line.strip()
                if len(line.split()) == 2:
                    user, page_position = line.split()
                    users_page_position[user] = page_position
                else:
                    users_page_position[line] = ''

        return users_page_position
