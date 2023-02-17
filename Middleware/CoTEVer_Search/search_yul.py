from html.parser import HTMLParser
from xml.dom.expatbuilder import parseString
from googleapiclient.discovery import build #google-api-python-client 
import requests
import json
import re
from readability import Document
import os
import aiohttp
import asyncio
import time


url = 'https://www.google.com/search?q='
header = { 
    'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\
    Safari/537.36'), 
    } 


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res


def html_parser(rough_html):
  parse_re = re.compile('<([^>]+)>|\t|\n|\r|\([^)]*\)|\[[^)]*\]')
  parsed_content = re.sub(parse_re, '', rough_html)
  return parsed_content


async def get(url, session):
    try:
        async with session.get(url=url, timeout=3) as response:
            resp = await response.text()
            print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
            return (url, resp)
    except Exception as e:
        print("Unable to get url {} due to {}.".format(url, e.__class__))
        return (url, None)


async def main_get(urls):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(url, session) for url in urls])
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))
    return ret


async def search(q, google_search_api, google_engine_id):
    sub_questions = q['explanation']
    for i in sub_questions:
        tmptmp_res = {}
        tmptmp_res[str(i)] = []
        search_result = google_search(sub_questions[str(i)]['sub_question'], google_search_api, google_engine_id)
        items = search_result['items']
        url = {}
        
        for item in items:
            url[item['link']] = {}
            url[item['link']]['title'] = item['title']

        ret = await main_get(list(url.keys()))

        for response in ret:
            if response[1] != None:
                doc = Document(response[1]).summary()
                doc = html_parser(doc).strip()
                url[response[0]]['document'] = doc
            else:
                del url[response[0]]

        cnt = 0
        for key in url:
            if cnt == 5:
                break
            evidence_doc = {}
            evidence_doc['url'] = key
            evidence_doc['title'] = url[key]['title']
            evidence_doc['document'] = url[key]['document']
            sub_questions[str(i)]['evidence_document'][str(cnt)] = evidence_doc
            cnt += 1
       
    # json_file = json.dumps(q,ensure_ascii=False, indent=4)
    return q