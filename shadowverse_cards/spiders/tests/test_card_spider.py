# import unittest

# for storing/ mocking http requests
# Betamax intercepts every request you make and attempts to find a matching
# request that has already been intercepted and recorded.
# To get the latest version of the site, delete the cassettes dir and rerun tests
from betamax import Betamax
from betamax.fixtures.unittest import BetamaxTestCase
import requests
from scrapy.http import HtmlResponse

from ..card_spider import CardSpider


with Betamax.configure() as config:
    config.cassette_library_dir = 'cassettes'
    config.preserve_exact_body_bytes = True


class CardSpiderTest(BetamaxTestCase):

    @classmethod
    def setUpClass(cls):
        cls.spider = CardSpider()
        # elf child may
        cls.follower_url = 'https://shadowverse-portal.com/card/101111010'
        # bloodfed flowerbed
        cls.amulet_url = 'https://shadowverse-portal.com/card/101623010'
        # executioner's axe
        cls.spell_url = 'https://shadowverse-portal.com/card/103614010'

    def get_and_store_response(self, url):
        # response = requests.Session().get(url)
        headers = {"Accept-Language": "en-US,en;q=0.5"}
        response = self.session.get(url, headers=headers)
        return HtmlResponse(body=response.content, url=url)

    def test_parse_card_name(self):
        follower_resp = self.get_and_store_response(self.follower_url)
        follower_name = self.spider.parse_card_name(follower_resp)
        self.assertEquals(follower_name, 'Elf Child May')
        amulet_resp = self.get_and_store_response(self.amulet_url)
        amulet_name = self.spider.parse_card_name(amulet_resp)
        self.assertEquals(amulet_name, 'Bloodfed Flowerbed')
        spell_resp = self.get_and_store_response(self.spell_url)
        spell_name = self.spider.parse_card_name(spell_resp)
        self.assertEquals(spell_name, 'Executioner\'s Axe')
