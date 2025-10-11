import spacy

from app.utils import singleton


@singleton
class DescriptiveKeywordExtractor:

    def __init__(self, language_model: str = 'en_core_web_sm'):
        self.nlp = spacy.load(language_model)
        self.allowed_pos = {'ADJ', 'NOUN', 'PROPN'}

    def extract(self, text: str) -> str:
        doc = self.nlp(text)
        keywords = [token.text for token in doc if token.pos_ in self.allowed_pos]
        return ' '.join(keywords)


keyword_extractor = DescriptiveKeywordExtractor()

__all__ = ['DescriptiveKeywordExtractor', 'keyword_extractor']
