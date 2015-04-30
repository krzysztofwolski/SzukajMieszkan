__author__ = 'krzyh'
from collections import namedtuple
import urllib2
import re
import datetime
import time
from os import system
import BeautifulSoup

Apartment = namedtuple('Apartment', ['title', 'price', 'url'])


class Portal(object):

    def __init__(self):
        self.url = ""
        self.name = ""
        self.apartments = {}

    def update_apartments(self, silence=True):
        return

    def add_apartment(self, title, price, url, silence=True):
        if url not in self.apartments.keys():
            nao = datetime.datetime.now()
            print nao.hour, ":", nao.minute, "\t", url
            if not silence:
                system('say Something on ' + self.name)
            self.apartments[url] = Apartment(title, price, url)

    def __str__(self):
        for i, apartment in enumerate(self.apartments):
            print "{} - {} - {}\n{}".format(
                i,
                apartment.price,
                apartment.title,
                apartment.url
            )


class Olx(Portal):

    def __init__(self):
        super(Olx, self).__init__()
        self.name = "o.l.x."
        self.url = "http://olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/" \
                   "?search%5Bfilter_float_price%3Ato%5D=2500&search%5B" \
                   "filter_enum_rooms%5D%5B0%5D=three&search%5Bphotos%5D=1" \
                   "&search%5Bdist%5D=5"

    def update_apartments(self, silence=True):
        page = urllib2.urlopen(self.url)
        soup = BeautifulSoup.BeautifulSoup(page.read())
        details = soup.findAll(
            'a',
            {
                'class': re.compile(r".*\bdetailsLink\b.*")
            }
        )

        for detail in details:
            self.add_apartment("", "", detail['href'], silence=silence)


class Gumtree(Portal):

    def __init__(self):
        super(Gumtree, self).__init__()
        self.name = "gumtree"
        self.url = "http://www.gumtree.pl/fp-mieszkania-i-domy-do-wynajecia/" \
                   "wroclaw/c9008l3200114?A_DwellingType=flat&" \
                   "A_NumberRooms=3&maxPrice=2600&minPrice=1000"

    def update_apartments(self, silence=True):
        page = urllib2.urlopen(self.url)
        soup = BeautifulSoup.BeautifulSoup(page.read())
        details = soup.findAll(
            'a',
            {
                'class': re.compile(r".*\badLinkSB\b.*")
            }
        )

        for detail in details:
            self.add_apartment("", "", detail['href'], silence=silence)



portals = [Gumtree(), Olx()]

for portal in portals:
        portal.update_apartments()

while True:
    for portal in portals:
        portal.update_apartments(silence=False)

    time.sleep(60)