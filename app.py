from haystack.preprocessor import PreProcessor
from haystack.file_converter.pdf import PDFToTextConverter
from questions.question_picker import QuestionsPicker
converter = PDFToTextConverter(remove_numeric_tables=False)
text = converter.convert(file_path='data/trust_deed_01.pdf')


#extract_doc_type

questions = QuestionsPicker(doc_type='trust_deed', doc_language='en')\
    .get_related_questions()
print(questions)

# preprocessor = PreProcessor(
#     clean_empty_lines=True,
#     clean_whitespace=True,
#     clean_header_footer=False,
#     split_by="word",
#     split_overlap=3,
#     split_length=100,
#     split_respect_sentence_boundary=True
# )
#
# docs_default = preprocessor.process(text)
# for element in docs_default:
#     for key, value in element.items():
#         print(key)
#         print(value)
#print(len(docs_default))