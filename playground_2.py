from haystack import Pipeline
from haystack.summarizer import TransformersSummarizer
from haystack import Document


docs = [Document("PG&E stated it scheduled the blackouts in response to forecasts for high winds amid dry conditions.\
                 The aim is to reduce the risk of wildfires. Nearly 800 thousand customers were scheduled to be affected by\
                 the shutoffs which were expected to last through at least midday tomorrow.")]


summarizer = TransformersSummarizer(model_name_or_path="google/pegasus-xsum", use_gpu=0)
summary = summarizer.predict(documents=docs, generate_single_summary=True)
print(summary)
# p = Pipeline()
# p.add_node(component=retriever, name="ESRetriever1", inputs=["Query"])
# p.add_node(component=summarizer, name="Summarizer", inputs=["ESRetriever1"])
# res = p.run(query="What did Einstein work on?")