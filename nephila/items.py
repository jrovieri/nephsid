# -*- coding: utf-8 -*-
import unicodedata
from w3lib.html import remove_tags

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity, Join, MapCompose, TakeFirst

remove_extra_spaces = lambda s: " ".join(s.split())
remove_control_characters = lambda s: "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")


class DefaultItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class Recipe(Item):
    _id = Field()
    dateModified = Field()
    datePublished = Field()
    description = Field(output_processor=Join('\n'))
    image = Field()
    isPartOf = Field()
    language = Field(input_processor=MapCompose(lambda s: s[:2].lower()))
    name = Field(input_processor=MapCompose(remove_extra_spaces,
        remove_tags, remove_control_characters))
    recipeIngredient = Field(input_processor=MapCompose(remove_extra_spaces,
        remove_tags, remove_control_characters), output_processor=Identity())
    recipeInstructions = Field(input_processor=MapCompose(remove_extra_spaces,
        remove_tags, remove_control_characters), output_processor=Join('\n'))
    url = Field()
