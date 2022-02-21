from haystack.file_converter.pdf import PDFToTextConverter
from summarizers import Summarizers
from haystack.preprocessor import PreProcessor

converter = PDFToTextConverter(remove_numeric_tables=True)
text = converter.convert(file_path='data/CDL_Annual_Report_2020.pdf')

preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    clean_header_footer=False,
    split_by="word",
    split_overlap=2,
    split_length=200,
    split_respect_sentence_boundary=True
)

docs_default = preprocessor.process(text)

print(docs_default)

summarizer = Summarizers()
final = {}
for item in docs_default:
    text = item.get('text')
    trimmed = text.replace('\n', ' ')
    summed = summarizer(trimmed)
    print(f'Summed {summed}')



