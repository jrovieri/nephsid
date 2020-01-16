# -*- coding: utf-8 -*-
from scrapy.utils import project
from scrapy.utils.log import configure_logging
from scrapy.utils.python import garbage_collect
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from pyparsing import (Regex, Or, Optional, replaceWith, Word, OneOrMore, Group,
    StringStart, StringEnd)

#
# Parsing any number format
#

# Catch any integer or float with dot or comma
numbers = Regex(r"\d+((\.|\,)\d*)?")\
    .setParseAction(lambda t: t[0].replace(u',', u'.'), lambda t: float(t[0]))

# Unicode fractions
unicode_fractions = Or([Word(c).setParseAction(replaceWith(v))
    for c, v in [(u'½', 0.5), (u'¼', 0.25), (u'¾', 0.75), (u'⅛', 0.125)]])

# String fractions
string_fractions = numbers("numerator") + "/" + numbers("denominator")
string_fractions.setParseAction(lambda t: t.numerator / t.denominator)

# Fractions
fractions = Optional(numbers) + Or(unicode_fractions ^ string_fractions)
frac0 = numbers + unicode_fractions
frac1 = numbers + string_fractions
fracs = frac0 ^ frac1 ^ unicode_fractions ^ string_fractions

# String cardinals
string_cardinals = Or([Word(c).setParseAction(replaceWith(v))
    for c, v in [(u'um', 1), (u'dois', 2), (u'três', 3), (u'quatro', 4),
        (u'cinco', 5)]])

# Partitive numerals
partitive_numerals = Or([Word(c).setParseAction(replaceWith(v))
    for c, v in [(u'meio', 0.5), (u'meia', 0.5), (u'um quarto', 0.25)]])

# The pattern
num = Or(fracs ^ numbers ^ string_cardinals) \
    .setParseAction(lambda n: sum(n)) \
    .setResultsName('value')


@inlineCallbacks
def crawl(spider, settings):
    runner = CrawlerRunner(settings)

    yield runner.crawl(spider)
    reactor.stop()

def execute_crawler(identifier):
    # Runs a crawler from command-line (not working)
    configure_logging()
    settings = project.get_project_settings()

    try:
        crawl(spider, settings)
        reactor.run()
    finally:
        garbage_collect()
