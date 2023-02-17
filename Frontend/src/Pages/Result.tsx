import React, { useState } from 'react';
import Graph from '../Components/Graph.jsx';
import MakeRate from '../Components/MakeRate';

function Result() {
  const [answer, setAnswer] = useState('');
  return (
    <div className="grid grid-cols-3 w-full h-[calc(100vh-80px)]  p-4 gap-2 min-h-0">
      <div className="col-start-1 border overflow-y-auto">
        <Graph setAnswer={setAnswer} />
      </div>
      <div
        className="col-start-2 border overflow-y-auto"
        style={{
          overflow: "scroll",
          whiteSpace: 'pre-wrap',
          fontFamily: 'Verdana',
          fontSize: '20px',
        }}
      >
        {answer}
      </div>
      <div className="col-start-3 border p-4 h-full min-h-0 overflow-y-auto">
        <MakeRate />
      </div>
    </div>
  );
}

export default Result;
