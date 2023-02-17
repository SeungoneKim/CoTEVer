import React from 'react';

function EachResult({
  question,
  rate,
  date,
}: {
  question: string;
  rate: number | null;
  date: string;
}) {
  return (
    <button className="w-full flex gap-8 justify-between items-center bg-white py-4 px-4 shadow cursor-pointer rounded">
      <div className="font-semibold text-xl">{question}</div>
      <div className=" flex-shrink-0">
        <div className="text-lg font-medium">{rate} / 5</div>
        <div className="text-sm">{date}</div>
      </div>
    </button>
  );
}

function PastResult() {
  return (
    <div className="w-full h-full flex items-center flex-col gap-8">
      <div className="font-bold text-2xl">과거 검색결과</div>
      <div className="flex flex-col w-full h-[50vh] overflow-y-auto gap-4 px-1 py-1 scrollbar-hide">
        {Array(9)
          .fill(0)
          .map((_, i) => (
            <EachResult
              key={i}
              question={`Temp Question ${i + 1}`}
              rate={(i + 1) * 0.1 + 4}
              date={`2022-0${i + 1}-0${i + 1}`}
            />
          ))}
      </div>
    </div>
  );
}

export default PastResult;
