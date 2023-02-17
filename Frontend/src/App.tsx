import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import TopBar from './Components/TopBar';
import Result from './Pages/Result';

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <div className="w-full h-screen grid">
        <TopBar />
        <Result />
      </div>
    ),
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
