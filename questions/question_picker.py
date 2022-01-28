import questions
from exceptions.exceptions import LanguageNotSupportedException, DocumentNotSupportedException


class QuestionsPicker:
    """
    Based on the input (language and document type) decides what questions are loaded into the prediction.
    """
    def __init__(self, doc_type: str, doc_language: str):
        self.doc_type = doc_type
        self.doc_language = doc_language

    def __get_language(self, languages: dict) -> list:
        if self.doc_language in languages:
            return languages.get(self.doc_language)
        else:
            raise LanguageNotSupportedException(f'language {self.doc_language} is not supported')

    def get_related_questions(self):
        if self.doc_type == 'trust_deed':
            doc_based_questions = questions.questions_trust_deeds
        elif self.doc_type == 'annual_report':
            doc_based_questions = questions.questions_annual_reports
        else:
            raise DocumentNotSupportedException(f'Document {self.doc_type} not supported')

        return self.__get_language(doc_based_questions)
