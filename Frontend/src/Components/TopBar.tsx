import React from 'react';
import {
  createSearchParams,
  useNavigate,
  useSearchParams,
} from 'react-router-dom';
import PastResult from './PastResult';
import usePopup from './usePopup';

function TopBar() {
  const { component, openPopup } = usePopup();
  const [searchParams] = useSearchParams();
  const question = searchParams.get('question');
  const navigate = useNavigate();
  console.log(question);
  return (
    <form
      className="w-full h-20 flex justify-between items-center px-8 gap-8 flex-shrink-0"
      onSubmit={(e) => {
        e.preventDefault();
        const q = (e.target as any)[0].value as string;
        if (!q || typeof q !== 'string') return;
        const qq = q.trim();
        if (qq.length === 0) return;
        const asdf = createSearchParams({ question: qq });
        navigate({
          pathname: '',
          search: asdf.toString(),
        });
      }}
    >
      {/* {component} */}
      <h1 className="font-bold text-2xl">CoTEver</h1>
      <input
        type="text"
        className="w-full border-2 border-blue-300 rounded-full outline-none focus:border-blue-800 text-center px-8 py-2"
        defaultValue={question || ''}
        placeholder="Please ask any questions you may have!"
      />
      {/* <button
        className=" shrink-0 cursor-pointer"
        onClick={() => openPopup(<PastResult />)}
      >
        과거 검색결과
      </button> */}
    </form>
  );
}

export default TopBar;
