import json
import os
import re

from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class DataGatherPipeline:
    """Extracts the necessary text-data from the Selectors."""

    REGEX = [
        # This matches urls starting in 'http'
        re.compile(
            r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
        ),

        # This are for the links included in tweets with images uploaded
        re.compile(r'(pic\.twitter\.com\/[a-zA-Z1-9]+)')
    ]

    def process_item(self, item, spider):
        """Processes an item returned by Spider.

        Args:
            item (scrapy.Item or dict): item to process.
            spider (scrapy.Spider): spider which returned an item.

        Returns:
            scrapy.Item or dict: a processed item to write.
            Example of a returned item:
            {
                'tweet_id': 3443534534543,
                'user': 'user1',
                'time_epoch': 123854343,
                'tweet': 'Some text with/without links',
                'n_likes': 10,
                'n_retweets': 20,
                'n_replies': 5,
                'n_emojis': 2,
                'quoted_tweet': {
                    'screen_name': 'user5',
                    'name': 'Full name',
                    'text': 'Quoted text of a tweet',
                    'hashtags': [],
                    'mentions': [],
                    'n_emojis': 0
                },
                'hashtags': ['hashtag1', 'hashtag2', 'hashtag3'],
                'mentions': ['user3', 'user4']
            }
        """

        data = {
            'tweet_id': self._get_tweet_id(item['tweet']),
            'user': item['user'],
            'time_epoch': self._get_time_epoch(item['tweet']),
            'tweet': self._get_tweet(item['tweet']),
            'n_likes': self._get_n_likes(item['tweet']),
            'n_retweets': self._get_n_retweets(item['tweet']),
            'n_replies': self._get_n_replies(item['tweet']),
            'n_emojis': self._get_n_emojis(item['tweet']),
            'quoted_tweet': self._get_quoted_tweet(item['tweet']),
            'hashtags': self._get_hashtags(item['tweet']),
            'mentions': self._get_mentions(item['tweet'])
        }

        return data

    def _get_hashtags(self, tweet):
        """Finds all hashtags for a tweet.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            list: list of hashtags.
        """
        return tweet.css('p.js-tweet-text a.twitter-hashtag b::text').getall()

    def _get_mentions(self, tweet):
        """Finds all mentions for a tweet.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            list: list of persons mentioned in the tweet.
        """
        mentions = tweet.css(
            'p.js-tweet-text  a[data-mentioned-user-id]::attr(href)').getall()
        mentions = [mention[1:] for mention in mentions]
        return mentions

    def _get_n_likes(self, tweet):
        """Finds number of likes for a tweet.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            int: number of likes.
        """
        try:
            n_likes = tweet.css(
                'span.ProfileTweet-action--favorite span.ProfileTweet-actionCount'
            ).attrib['data-tweet-stat-count']
            n_likes = int(n_likes)
        except (TypeError, ValueError):
            n_likes = 0
        return n_likes

    def _get_n_retweets(self, tweet):
        """Finds number of retweets for a tweet.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            int: number of retweets.
        """
        try:
            n_retweets = tweet.css(
                'span.ProfileTweet-action--retweet span.ProfileTweet-actionCount'
            ).attrib['data-tweet-stat-count']
            n_retweets = int(n_retweets)
        except (TypeError, ValueError):
            n_retweets = 0
        return n_retweets

    def _get_n_replies(self, tweet):
        """Finds number of replies for a tweet.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            int: nubmer of replies.
        """
        try:
            n_replies = tweet.css(
                'span.ProfileTweet-action--reply span.ProfileTweet-actionCount'
            ).attrib['data-tweet-stat-count']
            n_replies = int(n_replies)
        except (TypeError, ValueError):
            n_replies = 0
        return n_replies

    def _get_n_emojis(self, tweet):
        """Finds number of emojis contained in a tweet.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            int: number of emojis.
        """
        try:
            emojis = tweet.css('p.tweet-text img.Emoji').getall()
            n_emojis = len(emojis)
        except (TypeError, ValueError):
            n_emojis = 0
        return n_emojis

    def _get_quoted_tweet(self, tweet):
        """Gets quoted tweet.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            dict: quoted tweet which contains following fields:
            screen_name, name, text, hashtags, mentions, n_emojis.
        """
        if not tweet.css('div.QuoteTweet-text'):
            return {
                'screen_name': None,
                'name': None,
                'text': '',
                'hashtags': [],
                'mentions': [],
                'n_emojis': 0
            }
        text = tweet.css('div.QuoteTweet-text ::text').getall()
        text = ''.join(text) if text else ''
        text = self._add_space_to_urls(text)

        quoted_tweet = {
            'screen_name':
                tweet.css(
                    'div.QuoteTweet-innerContainer::attr(data-screen-name)'
                ).get(),
            'name':
                tweet.css('b.QuoteTweet-fullname::text').get(),
            'text':
                text,
            'hashtags':
                tweet.css('div.QuoteTweet-text span.twitter-hashtag b::text'
                         ).getall(),
            'mentions':
                tweet.css(
                    'div.QuoteTweet-text span[data-mentioned-user-id] b::text'
                ).getall(),
            'n_emojis':
                len(tweet.css('div.QuoteTweet-text img.Emoji').getall())
        }
        return quoted_tweet

    def _get_time_epoch(self, tweet):
        """Gets seconds since 1 Jan 1970.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            int: seconds since 1 Jan 1970.
        """
        try:
            time_epoch = int(
                tweet.css('span._timestamp::attr(data-time)').get())
        except (TypeError, ValueError):
            time_epoch = None
        return time_epoch

    def _get_tweet_id(self, tweet):
        """Gets tweet id.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            int: tweet id.
        """
        try:
            tweet_id = int(tweet.css('::attr(data-tweet-id)').get())
        except (TypeError, ValueError):
            tweet_id = None
        return tweet_id

    def _get_tweet(self, tweet):
        """Extracts text from a tweet.

        Args:
            tweet (scrapy.Selector): selector returned by item.

        Returns:
            str: tweet text.
        """
        text = tweet.css('p.tweet-text ::text').getall()
        text = ''.join(text) if text else ''
        text = self._add_space_to_urls(text)
        return text

    def _add_space_to_urls(self, text):
        """Add spaces before each url in the text.

        Args:
            text (str): text of tweet.

        Returns:
            str: tweet text in which spaces are added before each url.
        """
        text = text.replace(u'\xa0', u' ')
        for rgx in self.REGEX:
            text = rgx.sub(r' \1', text)
        return text


class FileSavePipeline:
    """Saves a processed item to a file with jsonl format.

    Creates a separate file for each scraped user. Besides, if scraper will
        be stopped, it will create the file `page_positions.txt` with users
        and min postions from which the scraper should continue scraping.
    """

    def __init__(self):
        self.file_map = {}
        self.save_path = settings['SAVE_PATH']['tweets']

        os.makedirs(self.save_path, exist_ok=True)

    def open_spider(self, spider):
        for user_name in spider.users_page_position:
            output_file = os.path.join(self.save_path, f'{user_name}.jsonl')
            self.file_map[user_name] = open(output_file, 'a')

    def close_spider(self, spider):
        for user_name in self.file_map:
            self.file_map[user_name].close()

        with open('page_positions.txt', 'w') as f:
            for user_name in spider.users_page_position:
                min_position = spider.users_page_position[user_name]
                f.write(f'{user_name} {min_position}\n')

    def process_item(self, item, spider):

        self._write_to_file(item)
        return item

    def _write_to_file(self, item):
        line = json.dumps(dict(item)) + "\n"
        self.file_map[item['user']].write(line)
