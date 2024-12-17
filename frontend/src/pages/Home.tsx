// src/pages/Home.tsx

// 라우팅을 위한 네비게이션 훅
import { useNavigate } from 'react-router-dom';

export default function Home() {
  // 네비게이션 훅
  const navigate = useNavigate();

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-screen-xl mx-auto px-4">
        {/* 중앙 정렬 */}
        <div className="text-center space-y-8">
          {/* 메인 타이틀 */}
          <h1 className="text-6xl font-bold text-gray-800">
            HTP 심리검사
          </h1>
          <div className="max-w-2xl mx-auto">
             {/* 시작 버튼 */}
            <button
              onClick={() => navigate('/select')}
              className="w-64 h-16 bg-blue-500 text-white text-xl font-semibold 
                       rounded-lg shadow-lg hover:bg-blue-600 
                       transition-colors duration-200"
            >
              심리분석 시작하기
            </button>
            {/* 서비스 설명 */}
            <p className="mt-6 text-xl text-gray-600">
              집, 나무, 사람을 그려서 자신의 심리 상태를 분석해보세요.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}