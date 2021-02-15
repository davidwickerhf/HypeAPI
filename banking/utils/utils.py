#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, List
from lxml import html


def parse_form(data, **fields):
    """
    Parses and HTML form and returns data required to submit it.
    """
    page = html.fromstring(data)
    form = page.xpath("//form")[0]
    url = form.xpath("./@action")[0]
    post_data = {**fields}
    for field in form.xpath("./input"):
        post_data[field.xpath("./@name")[0]] = field.xpath("./@value")[0]
    return {"url": url, "post_data": post_data}


def loginrequired(func):
    """
    Decorator that ensures the user is authenticated.
    """
    def wrapper(self, *args, **kwargs):
        if self.token is None:
            raise Exception("Login required but not yet performed")
        return func(self, *args, **kwargs)
    return wrapper


def parse_movements(data:dict):
    """Parse the json response of the Hype API movements endpoint

    Args:
        data (dict): Data returned by the Hype API

    Returns:
        List[Dict]: A list of the parsed movements.
    """
    if not data:
        return None

    movements:List[Dict] = list()

    months = data.get('month')
    if not months:
        return None

    for month in months:
        movementsdata = month.get('movements')
        if not movementsdata: pass
        for movementdata in movementsdata:
            transaction = dict()
            transaction['id'] = movementdata.get('id')
            transaction['title'] = movementdata.get('title')
            transaction['date'] = movementdata.get('date')
            
            income = movementdata.get('income')
            amount = movementdata.get('amount')
            if not income: 
                amount *= -1

            transaction['income'] = income
            transaction['amount'] = amount
            transaction['subType'] = movementdata.get('subType')
            additional = movementdata.get('additionalInfo')
            transaction['category'] = additional.get('category').get('name') if additional else None
            transaction['reference'] = additional.get('reference') if additional else None
            transaction['name'] = additional.get('name') if additional else None
            transaction['surname'] = additional.get('surName') if additional else None
            movements.append(transaction)
    return movements


