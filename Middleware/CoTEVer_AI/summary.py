from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from utils import *



class Summarizer():
    def __init__(self):
        print_now()
        self.tokenizer_kwargs = {'truncation':True}
        self.summarizer = pipeline("summarization",  model="t5-base", tokenizer="t5-base")

        # self.summarizer = pipeline("summarization",  model="google/pegasus-large", tokenizer="google/pegasus-large")


    def summarize(self, input_dict):
        for question in input_dict.keys():
            articles = input_dict[question]
            summaries = self.summary_pipeline(articles,summarizer=self.summarizer,tokenizer_kwargs=self.tokenizer_kwargs)
            new_output = list(zip(summaries,articles))

            input_dict[question] = new_output
        return input_dict

    def summarize_oneshot(self, input_dict):
        articles = []
        n=len(input_dict.keys())
        for question in input_dict.keys():
            articles.append(input_dict[question])
        summaries_whole = self.summary_pipeline(articles,summarizer=self.summarizer,tokenizer_kwargs=self.tokenizer_kwargs)
        summaries_whole = [summaries_whole[i:i + n] for i in range(0, len(summaries_whole), n)]
        for i,question in enumerate(input_dict.keys()):
            new_output = list(zip(summaries_whole[i],input_dict[question]))
            input_dict[question] = new_output
        return input_dict


    def summary_pipeline(self,articles, summarizer,tokenizer_kwargs):
        summ = summarizer(articles, max_length=128, min_length=20, return_text=True,**tokenizer_kwargs)
        out = [sum["summary_text"] for sum in summ]
        return out
        