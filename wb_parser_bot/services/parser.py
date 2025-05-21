from typing import List
from wb_parser import WbAsyncParser, AIOHTTPConnection, UrlParserV13
from wb_parser.schemas import ProductGet, ProductFind
from wb_parser.services.validator import wb_id_validator

from wb_parser_bot.config import settings

class ParserService:
    def __init__(self):
        connection = AIOHTTPConnection()
        url_parser = UrlParserV13(
            base_url_get=settings.parser.url_get_str,
            base_url_find=settings.parser.url_find_str
        )
        self._parser = WbAsyncParser(
            connection=connection,
            url_parser=url_parser
        )
    
    async def get_product(self, product_id: int) -> ProductGet:
        return await self._parser.get_product(product_id)
    
    async def find_products(self, query: str) -> List[ProductFind]:
        try:
            return await self._parser.find_products(query)
        except:
            return []
    
    @staticmethod
    def validate_id(product_id: int):
        wb_id_validator(product_id)