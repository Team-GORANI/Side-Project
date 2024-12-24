// App.tsx
// 라우팅 관련 컴포넌트, 페이지 컴포넌트 임포트
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Selection from './pages/Selection';
import Drawing from './pages/Drawing';
import Result from './pages/Result';
import './App.css';

function App() {
  return (
    <div className="app-container">
      {/* BrowserRouter로 라우팅 기능 활성화 */}
      <BrowserRouter>
      {/* Routes로 여러 Route 그룹화 */}
        <Routes>
          {/* 경로에 해당하는 컴포넌트 매핑 */}
          <Route path="/" element={<Home />} />
          <Route path="/select" element={<Selection />} />
          <Route path="/drawing/:type" element={<Drawing />} />
          <Route path="/result" element={<Result />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;