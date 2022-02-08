from questions.questions import questions_trust_deeds, questions_annual_reports
from exceptions.exceptions import LanguageNotSupportedException, DocumentNotSupportedException


class QuestionsPicker:
    """
    Based on the input (language and document type) decides what questions are loaded into the prediction.
    """
    def __init__(self, doc_type: str, doc_language: str, additional_questions: list = None):
        self.doc_type = doc_type
        self.doc_language = doc_language
        self.additional_questions = additional_questions

    def __get_questions_by_language(self, languages: dict) -> list:
        if self.doc_language in languages:
            return languages.get(self.doc_language)
        else:
            raise LanguageNotSupportedException(f'language {self.doc_language} is not supported')

    def get_related_questions(self):
        """
        Searches for the related question based on document and language
        :return:
        """
        if self.doc_type == 'trust_deed':
            doc_based_questions = questions_trust_deeds
        elif self.doc_type == 'annual_report':
            doc_based_questions = questions_annual_reports
        else:
            raise DocumentNotSupportedException(f'Document {self.doc_type} not supported')

        questions = self.__get_questions_by_language(doc_based_questions)
        if self.additional_questions is not None:
            [questions.append(item) for item in self.additional_questions]

        return questions
