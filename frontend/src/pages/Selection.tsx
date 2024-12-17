// src/pages/Selection.tsx

// 라우팅을 위한 네비게이션 훅
import { useNavigate } from 'react-router-dom';

// 선택 옵션 데이터 정의
const options = [
  { id: 'house', label: '집' },
  { id: 'tree', label: '나무' },
  { id: 'person', label: '사람' },
];

export default function Selection() {
  const navigate = useNavigate();

  return (
    // 전체 페이지 컨테이너
    <div className="w-full h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-screen-xl mx-auto px-4">
        {/* 중앙 정렬 */}
        <div className="text-center">
          {/* 선택 페이지 제목 */}
          <h2 className="text-4xl font-bold text-gray-800 mb-12">
            그리고 싶은 대상을 선택하세요
          </h2>
          {/* 선택 버튼 그리드 컨테이너 */}
          <div className="max-w-4xl mx-auto">
            {/* 3열 그리드 레이아웃 */}
            <div className="grid grid-cols-3 gap-8">
              {options.map((option) => (
                <button
                  key={option.id}
                  onClick={() => navigate(`/draw/${option.id}`)}
                  className="h-40 bg-white border-2 border-gray-200 rounded-lg 
                           text-2xl font-medium text-gray-700
                           hover:border-blue-500 hover:bg-blue-50 hover:text-blue-600
                           transition-all duration-200 shadow-sm"
                >
                  {option.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}