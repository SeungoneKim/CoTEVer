from html.parser import HTMLParser
from xml.dom.expatbuilder import parseString
from googleapiclient.discovery import build #google-api-python-client 
import json
import re
from readability import Document
import asyncio
import aiohttp
import sys
url = 'https://www.google.com/search?q='
google_search_api = ""
google_engine_id = ""
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
async def get_text(sess,url):
    async with sess.get(url, ssl=False) as res:
        text = await res.text()
    text = Document(text)
    text = text.summary()
    text = html_parser(text)
    text = text.strip()
    return text
async def main_fun(item):
    async with aiohttp.ClientSession() as sess:
        content = await asyncio.gather(*[asyncio.ensure_future(get_text(sess,k['link'])) for k in item])
        return content
async def main_async(sub_questions):
    await asyncio.gather(*[sub_qst_query(sub_questions,i) for i in sub_questions])
async def sub_qst_query(sub_questions,i):
    tmptmp_res = {}
    tmptmp_res[str(i)] = []
    search_result = google_search(sub_questions[str(i)]['sub_question'], google_search_api, google_engine_id)
    items = search_result['items']
    tmp_items = []
    tmp_cnt=0
    for k in items:
        if tmp_cnt==5:
            break
        if k['link'][-3:] =='pdf':
            continue
        else:
            tmp_items.append(k)
            tmp_cnt+=1
    items = tmp_items
    
    content = await main_fun(items)
    
    for k in range(0,5):
        tmptmptmp_res = {}
        tmptmptmp_res['url'] = items[k]['link']
        tmptmptmp_res['title'] = items[k]['title']
        tmptmptmp_res['content'] = content[k]
        sub_questions[str(i)]['evidence_document'][str(k)]= tmptmptmp_res

def search(q)->json:
    sub_questions = q['explanation']
    res={}
    res['questions'] = []
    py_ver = int(f"{sys.version_info.major}{sys.version_info.minor}")
    if py_ver > 37 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyc_query=[sub_qst_query(sub_questions,i) for i in sub_questions]
    asyncio.run(asyncio.wait(asyc_query))
    json_file = json.dumps(q,ensure_ascii=False, indent=4)
    return json_file
