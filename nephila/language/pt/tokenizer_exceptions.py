# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from spacy.symbols import ORTH, LEMMA

_exc = {}
for n in range(1, 100):
    _exc["%d%%" % n] = [
        {ORTH : "%d%%" % n, LEMMA : "%d%%" % n}]

_exc["1lata"] = [
    {ORTH : "1"},
    {ORTH : "lata", LEMMA : "lata"}]
_exc["2colheres"] = [
    {ORTH : "2"},
    {ORTH : "colheres", LEMMA : "colheres"}]
_exc["mlde"] = [
    {ORTH : "ml"},
    {ORTH : "de", LEMMA : "de"}]
_exc["4ovos"] = [
    {ORTH : "4"},
    {ORTH : "ovos", LEMMA : "ovos"}]
_exc["3gemas"] = [
    {ORTH : "3"},
    {ORTH : "gemas", LEMMA : "gemas"}]
_exc["Branco1"] = [
    {ORTH : "Branco", LEMMA : "Branco"},
    {ORTH : "1"}]
_exc["1KG"] = [
    {ORTH : "1"},
    {ORTH : "KG", LEMMA : "KG"}]
_exc["Vermelho100"] = [
    {ORTH : "Vermelho", LEMMA : "Vermelho"},
    {ORTH : "100"}]
_exc["Kalassi100"] = [
    {ORTH : "Kalassi", LEMMA : "Kalassi"},
    {ORTH : "100"}]
_exc["1litro"] = [
    {ORTH : "1"},
    {ORTH : "litro", LEMMA : "litro"}]
_exc["1-1/2copo"] = [
    {ORTH : "1"},
    {ORTH : "-"},
    {ORTH : "1/2"},
    {ORTH : "copo", LEMMA : "copo"}]
_exc["1kg(Tapioca"] = [
    {ORTH : "1"},
    {ORTH : "kg", LEMMA : "kg"},
    {ORTH : "(", LEMMA : "("},
    {ORTH : "Tapioca", LEMMA : "Tapioca"}]
_exc["Preço/100"] = [
    {ORTH : "Preço", LEMMA : "Preço"},
    {ORTH : "/", LEMMA : "/"},
    {ORTH : "100"}]
_exc["congelado(descongelado"] = [
    {ORTH : "congelado", LEMMA : "congelado"},
    {ORTH : "(", LEMMA : "("},
    {ORTH : "descongelado", LEMMA : "descongelado"}]
_exc["/kg"] = [
    {ORTH : "/"},
    {ORTH : "kg", LEMMA : "kg"}]
_exc["½kg"] = [
    {ORTH : "½"},
    {ORTH : "kg", LEMMA : "kg"}]
_exc["Hart's"] = [
    {ORTH : "Hart's", LEMMA : "Hart's"}]
_exc["Sea's"] = [
    {ORTH : "Sea's", LEMMA : "Sea's"}]
_exc["arrozcozido"] = [
    {ORTH : "arroz"},
    {ORTH : "cozido", LEMMA : "cozido"}]
_exc["xícarade"] = [
    {ORTH : "xícara"},
    {ORTH : "de", LEMMA : "de"}]
_exc["oréganoseco"] = [
    {ORTH : "orégano"},
    {ORTH : "seco", LEMMA : "seco"}]
_exc["minisuflês"] = [
    {ORTH : "mini"},
    {ORTH : "suflês", LEMMA : "suflês"}]
_exc["gde"] = [
    {ORTH : "g"},
    {ORTH : "de", LEMMA : "de"}]
_exc["(chá)de"] = [
    {ORTH : "(chá)"},
    {ORTH : "de", LEMMA : "de"}]
_exc["delentilha"] = [
    {ORTH : "de"},
    {ORTH : "lentilha", LEMMA : "lentilha"}]
_exc["1/2l"] = [
    {ORTH : "1/2"},
    {ORTH : "l", LEMMA : "l"}]
