# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from spacy.util import update_exc
from spacy.attrs import LANG
from spacy.symbols import ORTH, LEMMA
from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS

import spacy
from spacy.lang.pt.tokenizer_exceptions import TOKENIZER_EXCEPTIONS
from spacy.lang.pt.lex_attrs import LEX_ATTRS
from spacy.lang.pt.stop_words import STOP_WORDS

from .tokenizer_exceptions import _exc


TOKENIZER_EXCEPTIONS = _exc

class PortugueseDefaults(spacy.lang.pt.Portuguese.Defaults):
    lex_attr_getters = dict(spacy.lang.pt.Portuguese.Defaults.lex_attr_getters)
    lex_attr_getters[LANG] = lambda text: 'pt' # language ISO code

    # optional: replace flags with custom functions, e.g. like_num()
    lex_attr_getters.update(LEX_ATTRS)

    # merge base exceptions and custom tokenizer exceptions
    tokenizer_exceptions = update_exc(BASE_EXCEPTIONS, TOKENIZER_EXCEPTIONS)
    stop_words = STOP_WORDS

class Portuguese(spacy.lang.pt.Portuguese):
    lang = 'pt'
    Defaults = PortugueseDefaults

__all__ = [Portuguese]
