from transformers import pipeline
from transformers import AutoTokenizer, AutoModelWithLMHead
from CoTEVer_AI.utils import *
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch
import json


class SpeedyPipeline():
    def __init__(self):
        # print_now()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # t5tokenizer = AutoTokenizer.from_pretrained("t5-base",truncation=True,torchscript=True)
        # t5model = AutoModelWithLMHead.from_pretrained("t5-base",torchscript=True)
        # self.summarizer = pipeline("summarization",  model="t5-base", device=self.device)
        self.model = SentenceTransformer("sentence-transformers/sentence-t5-base")
        self.tokenizer_kwargs = {'truncation':True}


    # def process(self,input):
    #     sub_questions = []
    #     documents = []
    #     for subproblem in input["explanation"].values(): # input["explanation"]["0"]
    #         sub_questions.append(subproblem["sub_question"]) 
    #         for document in subproblem["evidence_document"].values(): # input["explanation"]["0"]["evidence_document"]
    #             documents.append(document["document"])
    #     # result = self.summarizer(documents, max_length=64, min_length=20, return_text=True,**self.tokenizer_kwargs)
    #     # summaries = [sum["summary_text"] for sum in result]
    #     doc_embeddings = self.model.encode(sub_questions)
    #     # candidate_embeddings = self.model.encode(summaries) 
    #     # summaries = [summaries[i:i+5] for i in range(0, len(summaries), 5)]
        
    #     candidate_embeddings = [candidate_embeddings[i:i + 5] for i in range(0, len(candidate_embeddings), 5)]
    #     assert len(candidate_embeddings) == len(doc_embeddings), print(len(candidate_embeddings),len(doc_embeddings))
    #     idx = 0
    #     for de, ce, summ in zip(doc_embeddings,candidate_embeddings,summaries):
    #         distances = cosine_similarity([de], ce)[0]
    #         distances = [float(s) for s in distances]
    #         top_results = list(zip(distances, summ))
    #         new_out = sorted(top_results, key=lambda x: x[0], reverse=True)
    #         inner_idx = 0
    #         for dist,sum in new_out:
    #             input["explanation"][str(idx)]["evidence_document"][str(inner_idx)]["document"] = sum
    #             input["explanation"][str(idx)]["evidence_document"][str(inner_idx)]["score"] = dist
    #             inner_idx += 1
    #         idx+=1
    #     return input

    def process_wo_summ(self,input):
        sub_questions = []
        documents = []
        for subproblem in input["explanation"].values(): # input["explanation"]["0"]
            sub_questions.append(subproblem["sub_question"]) 
            for document in subproblem["evidence_document"].values(): # input["explanation"]["0"]["evidence_document"]
                documents.append(document["document"])
        doc_embeddings = self.model.encode(sub_questions)
        candidate_embeddings = self.model.encode(documents) 
        
        candidate_embeddings = [candidate_embeddings[i:i + 5] for i in range(0, len(candidate_embeddings), 5)]
        assert len(candidate_embeddings) == len(doc_embeddings), print(len(candidate_embeddings),len(doc_embeddings))
        idx = 0
        for de, ce, doc in zip(doc_embeddings,candidate_embeddings,documents):
            distances = cosine_similarity([de], ce)[0]
            distances = [float(s) for s in distances]
            top_results = list(zip(distances, doc))
            new_out = sorted(top_results, key=lambda x: x[0], reverse=True)
            inner_idx = 0
            for dist,doc in new_out:
                input["explanation"][str(idx)]["evidence_document"][str(inner_idx)]["document"] = doc
                input["explanation"][str(idx)]["evidence_document"][str(inner_idx)]["score"] = dist
                inner_idx += 1
            idx+=1
        return input



    # def process_one(self,input):
    #     sub_questions = []
    #     documents = []
    #     for subproblem in input["explanation"].values(): # input["explanation"]["0"]
    #         sub_questions.append(subproblem["sub_question"]) 
    #         for document in subproblem["evidence_document"].values(): # input["explanation"]["0"]["evidence_document"]
    #             documents.append(self.summarizer([document["document"]], max_length=64, min_length=20, return_text=True,**self.tokenizer_kwargs)[0])
    #     doc_embeddings = self.model.encode(sub_questions)
    #     candidate_embeddings = self.model.encode(documents) 
    #     summaries = [documents[i:i+5] for i in range(0, len(documents), 5)]
    #     candidate_embeddings = [candidate_embeddings[i:i + 5] for i in range(0, len(candidate_embeddings), 5)]
    #     assert len(candidate_embeddings) == len(doc_embeddings), print(len(candidate_embeddings),len(doc_embeddings))
    #     idx = 0
    #     for de, ce, summ in zip(doc_embeddings,candidate_embeddings,summaries):
    #         distances = cosine_similarity([de], ce)[0]
    #         distances = [float(s) for s in distances]
    #         top_results = list(zip(distances, summ))
    #         new_out = sorted(top_results, key=lambda x: x[0], reverse=True)
    #         inner_idx = 0
    #         for dist,sum in new_out:
    #             input["explanation"][str(idx)]["evidence_document"][str(inner_idx)]["document"] = sum["summary_text"]
    #             input["explanation"][str(idx)]["evidence_document"][str(inner_idx)]["score"] = dist
    #             inner_idx += 1
    #         idx+=1
    #     return input
