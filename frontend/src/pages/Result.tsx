// src/pages/Result.tsx

// 라우팅을 위한 네비게이션 훅
import { useLocation, useNavigate } from 'react-router-dom';

export default function Result() {
  const { state } = useLocation();
  const navigate = useNavigate();
  
  // state가 없는 경우 예외처리
  if (!state?.result) {
    return (
      // 에러 메시지
      <div className="p-8 text-center">
        <p className="text-red-500">분석 결과를 찾을 수 없습니다.</p>
        {/* 처음으로 돌아가기 버튼 */}
        <button 
          onClick={() => navigate('/')}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
        >
          처음으로 돌아가기
        </button>
      </div>
    );
  }

  const { result } = state;

  return (
    // 결과 페이지 컨테이너
    <div className="p-8 max-w-4xl mx-auto">
      {/* 페이지 타이틀 */}
      <h1 className="text-2xl font-bold mb-8 text-center">분석 결과</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* 원본 이미지 섹션 */}
        <div className="border rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-4">업로드한 이미지</h2>
          <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
            <img 
              src={result.originalImage} 
              alt="Original" 
              className="w-full h-full object-contain"
            />
          </div>
        </div>
        
        {/* 분석 결과 섹션 */}
        <div className="border rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-4">심리 분석 결과</h2>
          <div className="prose">
            <p className="text-gray-700 whitespace-pre-line">
              {result.analysis}
            </p>
          </div>
        </div>
      </div>

      {/* 다시 시작하기 버튼 */}
      <div className="mt-8 text-center">
        <button 
          onClick={() => navigate('/')}
          className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          다시 시작하기
        </button>
      </div>
    </div>
  );
}