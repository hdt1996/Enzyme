from ..locals.globals_regex import *

class Categories:
    def checkAttribs(self, choose_group: str, keywords: list, custom_regex):
        if choose_group != '':
            self.choose_group = choose_group
        if len(keywords) != 0:
            self.keywords = keywords
        if custom_regex != "":
            self.custom_regex = custom_regex

class Balance(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                'NEW BALANCE ',
                'BALANCE AS OF',
                ''
            ]
        self.custom_regex = f"(\$?{ANY_FLOAT}{ANY_PHRASE}?\n)"
        self.choose_group = '2'
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)

class Name(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                'Name'
            ]
        self.custom_regex = 'Default'
        self.choose_group = '2'
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)
class Date(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                'Date'
            ]
        self.custom_regex = 'Default'
        self.choose_group = '2'
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)
class SSN(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                'SSN'
            ]
        self.custom_regex = 'Default'
        self.choose_group = '2'
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)
class Address(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                'Address'
            ]
        self.custom_regex = 'Default'
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)
class CreditCards(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                'CreditCards'
            ]
        self.custom_regex = 'Default'
        self.choose_group = '2'
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)
class Property_IDs(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                'Property_IDs'
            ]
        self.custom_regex = 'Default'
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)
class File_Numbers(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                'File_Numbers'
            ]
        self.custom_regex = 'Default'
        self.choose_group = '2'
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)
class Universal(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                ''
            ]
        self.custom_regex = ''
        self.choose_group = ''
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)
class CSS(Categories):
    def __init__(self, keywords: list, choose_group: str, custom_regex: str):
        self.keywords=\
            [
                ''
            ]
        self.custom_regex = fr"((?!{NONGREEDY_WILD}+\n*\{{)([{ANY_CH_HY_SP}]+(?<!(http))\:{NONGREEDY_WILD}+))"
        self.choose_group = ''
        super().__init__()
        self.checkAttribs(choose_group = choose_group, keywords = keywords, custom_regex = custom_regex)

