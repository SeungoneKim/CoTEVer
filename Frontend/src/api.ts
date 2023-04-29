import _axios from 'axios';
import { queryI, rawQueryI, resultI } from './types';
import d from './db/newdb.json';

const isLocalhost = window.location.hostname === 'localhost';
const PROXY = isLocalhost ? 'http://172.30.1.79:8000' : 'http://0.0.0.0:8000/';

export const axios = _axios.create({
  baseURL: PROXY,
  validateStatus: (status) => status < 500,
});

export const getQuery = async (query: string) => {
  const { data } = await axios.post<rawQueryI>('/api/query', {
    question: query,
  });
  // const data = d as any as rawQueryI;
  // console.log(data);
  // return null
  if (!data) return null;
  const nodeList = Object.keys(data.explanation)
    .map((t) => ({
      subQuestion: data.explanation[t].sub_question,
      subQuestionKeyword: data.explanation[t].sub_question,
      subAnswer: data.explanation[t].sub_answer,
      top5List: Object.keys(data.explanation[t].evidence_document)
        .map((tt) => {
          const target = data.explanation[t].evidence_document[tt];
          return {
            first: target.url,
            second: target.document,
            i: tt,
          };
        })
        .sort((a, b) => {
          const aa = parseInt(a.i);
          const bb = parseInt(b.i);
          return aa - bb;
        })
        .map(({ first, second }) => ({ first, second })),
      i: parseInt(t),
    }))
    .sort((a, b) => a.i - b.i)
    .map(({ subQuestion, subQuestionKeyword, subAnswer, top5List }) => ({
      subQuestion,
      subQuestionKeyword,
      subAnswer,
      top5List,
    }));
  const result: queryI = {
    query: data.question,
    finalAnswer: data.output.final_answer,
    finalExplanation: '',
    stepCount: nodeList.length,
    nodeList,
  };
  console.log(result);
  return result;
};

export const postResult = async (result: resultI) => {
  const { data } = await axios.post('/result', result);
  return data;
};
