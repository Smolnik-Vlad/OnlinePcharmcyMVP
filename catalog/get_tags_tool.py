from keybert import KeyBERT
import spacy


# Загрузка моделей


class KeyWords:
    nlp = spacy.load("en_core_web_sm")
    kw_model = KeyBERT()

    # Функция для извлечения ключевых слов
    def extract_keywords(self, text):
        # Удаляем стоп-слова, приводим к леммам
        doc = self.nlp(text.lower())
        clean_text = " ".join([token.lemma_ for token in doc if not token.is_stop])

        # Извлекаем ключевые слова
        keywords = self.kw_model.extract_keywords(clean_text, keyphrase_ngram_range=(1, 2), stop_words='english')
        print(keywords)
        return [kw[0] for kw in keywords]

# Пример использования
# user_query = "I have a Sore throat, headache, diarrhea."
# keywords = extract_keywords(user_query)
# print("Matched Tags:", keywords)
key_words_extractor = KeyWords()