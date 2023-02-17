import { useState } from 'react';
import { cls } from '../utils/cls';

const closeSvg = (
  <svg
    width="26"
    height="26"
    viewBox="0 0 26 26"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      d="M0.945312 1.75781L24.263 25.0755"
      stroke="#8C8C8C"
      strokeWidth="2.22074"
    />
    <path
      d="M0.945312 25.0742L24.263 1.75655"
      stroke="#8C8C8C"
      strokeWidth="2.22074"
    />
  </svg>
);

export const usePopup = (type = 'default' as 'big' | 'default') => {
  const [Target, setTarget] = useState<JSX.Element | null>(null);
  const openPopup = (target: JSX.Element) => setTarget(target);
  const closePopup = (callback?: () => void) => {
    if (callback) callback();
    setTarget(null);
  };
  const isOpen = Target ? true : false;
  const component = (
    <div
      className={cls(
        'fixed w-screen h-screen bg-black bg-opacity-80 left-0 top-0 z-30 flex justify-center items-center',
        Target ? '' : 'hidden',
      )}
      onClick={() => setTarget(null)}
    >
      <div
        className={cls(
          'max-w-[80%] w-[800px]  px-12 pb-12 pt-20 bg-[#F2F2F2] flex flex-col rounded-xl relative',
        )}
        onClick={(e) => e.stopPropagation()}
      >
        <button className="absolute top-7 left-7" onClick={() => closePopup()}>
          {closeSvg}
        </button>
        {Target}
      </div>
    </div>
  );
  return {
    component,
    openPopup,
    closePopup,
    isOpen,
  };
};

export default usePopup;
