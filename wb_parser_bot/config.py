from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class BotSettings(BaseModel):
    token: str
    developer_url: str = "https://t.me/anton_code"

class ParserSettings(BaseModel):
    url_get: HttpUrl
    url_find: HttpUrl

    @property
    def url_get_str(self) -> str:
        return self.parse_httpurl_to_str(self.url_get)

    @property
    def url_find_str(self) -> str:
        return self.parse_httpurl_to_str(self.url_find)

    def parse_httpurl_to_str(self, url: HttpUrl) -> str:
        url_str = str(url)
        if url_str[-1] == '/':
            url_str = url_str[:-1]
        return url_str

class Settings(BaseSettings):
    bot: BotSettings
    parser: ParserSettings
    
    model_config = SettingsConfigDict(env_file=("example.env", ".env"), env_nested_delimiter="__")

settings = Settings()