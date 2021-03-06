import json
from pathlib import Path
from tornado.escape import json_decode
import ray
from haystack.document_store.faiss import FAISSDocumentStore
from haystack.document_store import InMemoryDocumentStore
from haystack.document_store import ElasticsearchDocumentStore
from haystack.file_converter.pdf import PDFToTextConverter
from haystack.preprocessor import PreProcessor
from haystack.retriever import DensePassageRetriever
from haystack.retriever.sparse import ElasticsearchRetriever
from tornado.web import RequestHandler
from haystack.pipeline import ExtractiveQAPipeline
from models.model_utils import setup_models_at_startup
from questions.question_picker import QuestionsPicker
from memory_profiler import profile
from haystack.utils import launch_es
from haystack.pipeline import Pipeline
import time
from summarizers import Summarizers

readers = setup_models_at_startup()
try:
    launch_es()
except:
    pass

#pipeline = Pipeline().load_from_yaml(Path('/home/wicio/PycharmProjects/pub_haystack/pipelines/pipeline.yaml'))
#pipeline.load_from_yaml(Path("sample.yaml"))


@profile
def predict(questions, pipe):
    predictions = {}
    for question in questions:
        prediction = pipe.run(query=question)
        print(prediction)
        predictions[question] = {'answer': prediction['answers'][0]['answer'],
                                 'probability': prediction['answers'][0]['probability'],
                                 'context': prediction['answers'][0]['context']}

    return predictions


class QAHealthCheck(RequestHandler):

    def get(self):
        self.write("Hello, world")


class QAService(RequestHandler):
    # def post(self):
    #     data = json_decode(self.request.body)
    #     additional_questions = data.get('additional_questions', [])

    def post(self):
        data = json_decode(self.request.body)
        additional_questions = data.get('additional_questions', [])
        doc_language = data.get('doc_language')
        doc_type = data.get('doc_type')
        start_time = time.time()
        document_store = ElasticsearchDocumentStore()
        converter = PDFToTextConverter(remove_numeric_tables=True)
        text = converter.convert(file_path='data/CDL_Annual_Report_2020.pdf')

        # summarizer = Summarizers('normal')
        #
        # summed_text = summarizer(text)
        # print(summed_text)

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
        print(docs_default)
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
        retriever = ElasticsearchRetriever(document_store=document_store)
        #document_store.update_embeddings(retriever, batch_size=10000)
        questions = QuestionsPicker(doc_type=doc_type,
                                    doc_language=doc_language,
                                    additional_questions=additional_questions).get_related_questions()
        selected_reader = readers.get('en')
        pipeline = ExtractiveQAPipeline(reader=selected_reader, retriever=retriever)
        preds = predict(questions, pipeline)

        end_time = time.time()
        processed_time = end_time-start_time
        response = json.dumps({"doc_type": 'annual_report',
                               "execution_time": f'{processed_time}s',
                               "predictions": preds})

        return self.finish(response)


class QAService_static(RequestHandler):
    pass
