#-*- coding: utf-8 -*-
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
        if title not in self.apartments.keys():
            nao = datetime.datetime.now()
            print nao.hour, ":", nao.minute, "\t", url
            if not silence:
                system('say Something on ' + self.name)
            self.apartments[title] = Apartment(title, price, url)

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
            self.add_apartment(detail['href'], "", detail['href'], silence=silence)


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
            ending = len(detail['href'].split('-')[-1])
            title = detail['href'][:-ending]
            self.add_apartment(detail['href'], "", detail['href'], silence=silence)



class Otodom(Portal):

    def __init__(self):
        super(Otodom, self).__init__()
        self.name = "otodom"
        self.url = "http://otodom.pl/index.php?mod=listing&act=&" \
                   "source=main&Search=Search&objSearchQuery.ObjectName=Flat" \
                   "&objSearchQuery.OfferType=rent&Location=dolnośląskie" \
                   "%2C+Wrocław&objSearchQuery.Distance=0&objSearchQuery." \
                   "LatFrom=&objSearchQuery.LatTo=&objSearchQuery.LngFrom=" \
                   "&objSearchQuery.LngTo=&objSearchQuery.PriceFrom=1+000" \
                   "&objSearchQuery.PriceTo=2+500&objSearchQuery.AreaFrom=" \
                   "&objSearchQuery.AreaTo=&objSearchQuery.FlatRoomsNumFrom=" \
                   "3&objSearchQuery.FlatRoomsNumTo=3&objSearchQuery.FlatFloor" \
                   "From=&objSearchQuery.FlatFloorTo=&objSearchQuery.Flat" \
                   "FloorsNoFrom=&objSearchQuery.FlatFloorsNoTo=" \
                   "&objSearchQuery.FlatBuildingType=&objSearchQuery." \
                   "Heating=&objSearchQuery.BuildingYearFrom=&objSearchQuery" \
                   ".BuildingYearTo=&objSearchQuery.FlatFreeFrom=" \
                   "&objSearchQuery.CreationDate=&objSearchQuery." \
                   "Description=&objSearchQuery.offerId="

    def update_apartments(self, silence=True):
        page = urllib2.urlopen(self.url)
        soup = BeautifulSoup.BeautifulSoup(page.read())
        details = soup.findAll(
            'h1',
            {
                'class': re.compile(r".*\bod-listing_item-title\b.*")
            }
        )

        for detail in details:
            url = "http://otodom.pl" + detail.findAll('a')[0]['href']
            self.add_apartment(url, "", url, silence=silence)


portals = [Gumtree(), Olx(), Otodom()]

for portal in portals:
        portal.update_apartments()

while True:
    for portal in portals:
        portal.update_apartments(silence=False)

    time.sleep(60)