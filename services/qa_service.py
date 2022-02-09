import json

from haystack.document_store.faiss import FAISSDocumentStore
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.preprocessor import PreProcessor
from haystack.retriever import DensePassageRetriever
from tornado.web import RequestHandler

from models.model_utils import setup_models_at_startup
from questions.question_picker import QuestionsPicker
import time

readers = setup_models_at_startup()


def predict(questions, pipe):
    predictions = {}
    for question in questions:
        prediction = pipe.run(query=question)
        predictions[question] = {'answer': prediction['answers'][0]['answer'],
                                 'probability': prediction['answers'][0]['probability'],
                                 'context': prediction['answers'][0]['context']}

    return predictions


class QAHealthCheck(RequestHandler):

    def get(self):
        self.write("Hello, world")


class QAService(RequestHandler):

    def get(self):
        start_time = time.time()
        document_store = FAISSDocumentStore(faiss_index_factory_str='Flat')
        converter = PDFToTextConverter(remove_numeric_tables=False)
        text = converter.convert(file_path='data/2021-half-year-report-en.pdf')

        preprocessor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=False,
            split_by="word",
            split_overlap=3,
            split_length=100,
            split_respect_sentence_boundary=True
        )

        docs_default = preprocessor.process(text)

        # with open('data/nestle_report_en.txt', 'r') as file:
        #     text = file.readlines()
        #
        # text_str = '\n'.join([str(elem) for elem in text])
        # stripped_text = text_str.strip('\n')
        # print(stripped_text)

        dicts = docs_default
        # dicts = [{'text': stripped_text,
        #           'meta': {'name': 'thai_air_th.txt'}}]
        document_store.write_documents(dicts)
        retriever = DensePassageRetriever(document_store=document_store)
        document_store.update_embeddings(retriever)

        from haystack.pipeline import ExtractiveQAPipeline

        questions = QuestionsPicker(doc_type='annual_report', doc_language='en').get_related_questions()
        print(questions)
        selected_reader = readers.get('en')

        pipe = ExtractiveQAPipeline(selected_reader, retriever)

        preds = predict(questions, pipe)

        end_time = time.time()
        processed_time = end_time-start_time
        response = json.dumps({"doc_type": 'annual_report',
                               "execution_time": f'{processed_time}s',
                               "predictions": preds})

        return self.finish(response)
