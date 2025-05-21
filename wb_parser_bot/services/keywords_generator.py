from typing import List
import nltk
from abc import ABC, abstractmethod
from rake_nltk import Rake
from nltk.corpus import stopwords

class KeywordsGeneratorBase(ABC):
    @abstractmethod
    def generate(self, query: str, limit: int = 10) -> List[str]:
        raise NotImplementedError()

nltk.download('punkt_tab')
nltk.download("stopwords")

custom_stopwords = stopwords.words("russian") + stopwords.words("english")

class KeywordsGenerator(KeywordsGeneratorBase):
    def generate(self, query: str, limit: int = 10) -> List[str]:
        rake = Rake(stopwords=custom_stopwords, language="multilingual")
        rake.extract_keywords_from_text(query)
        return rake.get_ranked_phrases()[:limit]