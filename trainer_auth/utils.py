import os, json, logging, re
from transformers import BertTokenizer, BertForSequenceClassification, TextClassificationPipeline
from hazm import Normalizer
from dotenv import load_dotenv

load_dotenv()

class PersianSwearWordRemover:
    def __init__(self, model_name=None, swear_file=None):
        model_name = model_name or os.getenv('MODEL_NAME', 'HooshvareLab/bert-fa-base-uncased-clf-persiannews')
        swear_file = swear_file or os.getenv('SWEAR_FILE', 'swears.json')

        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForSequenceClassification.from_pretrained(model_name)
        self.pipeline = TextClassificationPipeline(model=self.model, tokenizer=self.tokenizer, return_all_scores=True)

        self.normalizer = Normalizer()
        self.swear_words = set(self.load_swear_words(swear_file))

    @staticmethod
    def load_swear_words(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("swear_words", [])
        except Exception as e:
            logging.error(f"Error loading swear words from {file_path}: {e}")
            return []

    @staticmethod
    def normalize_text(text):
        return re.sub(r'(.)\1{2,}', r'\1', text)

    def tokenize(self, text):
        normalized = self.normalizer.normalize(self.normalize_text(text))
        return re.findall(r'[\u0600-\u06FF]+', normalized)

    def is_swear_word(self, token):
        return token in self.swear_words

    def contains_swear_word(self, text):
        tokens = self.tokenize(text)
        return any(self.is_swear_word(token) for token in tokens)



remover = PersianSwearWordRemover()
