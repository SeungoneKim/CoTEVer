export interface querySubNodeI {
  subQuestion: string;
  subQuestionKeyword: string;
  subAnswer: string;
  top5List: { first: string; second: string }[];
}
export interface queryI {
  query: string;
  finalAnswer: string;
  finalExplanation: string;
  stepCount: number;
  nodeList: querySubNodeI[];
}

export interface rawQueryI {
  question: string;
  output: { final_answer: string };
  explanation: {
    [x: string]: {
      sub_question: string;
      sub_answer: string;
      evidence_document: {
        [x: string]: {
          url: string;
          title: string;
          document: string;
          score: number;
        };
      };
    };
  };
}

export interface resultI {
  query: string;
  finalAnswer: string;
  finalExplanation: string;
  stepCount: number;
  nodeList: (querySubNodeI & {
    subAnswerRating: number;
    subAnswerAlt: string;
  })[];
  finalAnswerRating: number | string;
  finalAnswerAlt: string | number;
  finalExplanationRating: number | string;
  finalExplanationAlt: string | number;
}
