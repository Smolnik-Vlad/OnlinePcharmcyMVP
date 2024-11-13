from transformers import pipeline
import language_tool_python


class CheckCommentsOnCorrect:
    toxicity_checker = pipeline("text-classification", model="unitary/toxic-bert")
    tool = language_tool_python.LanguageTool("en-US")  # или "ru-RU" для русского языка

    def check_toxicity(self, comment_text):
        result = self.toxicity_checker(comment_text)[0]
        if result['label'] == 'toxic' and result['score'] > 0.7:
            return True  # токсичный текст
        return False

    def check_spelling(self, message: str):
        matches = self.tool.check(message)
        return len(matches) == 0

    def check_comment(self, comment_text):
        return not self.check_toxicity(comment_text) and self.check_spelling(comment_text)


check_comment_tool = CheckCommentsOnCorrect()

# bad_comments = [
#     'F*ck everything',
#     "Hey, I'm Vlad",
#     'sdfasf',
#     'shit'
# ]
# for com in bad_comments:
#     print(a.check_toxicity(com))
#     print(a.check_spelling(com))
#     print('--------------------')
