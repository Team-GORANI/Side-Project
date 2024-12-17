// src/pages/Drawing.tsx

import { useState, useRef } from 'react';
import { ReactSketchCanvas, ReactSketchCanvasRef } from 'react-sketch-canvas';
import { useNavigate, useParams } from 'react-router-dom';
import { analyzeImage } from '../services/api';
  
export default function Drawing() {
  // 상태 관리
  const [mode, setMode] = useState<'draw' | 'upload'>('draw');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // 캔버스 참조, 라우팅 훅
  const canvasRef = useRef<ReactSketchCanvasRef>(null);
  const navigate = useNavigate();
  const { type } = useParams<{ type: 'house' | 'tree' | 'person' }>();

  // 실행 취소 핸들러(sketch-canvas)
  const handleUndo = () => {
    canvasRef.current?.undo();
  };

  // 전체 지우기 핸들러(sketch-canvas)
  const handleClear = () => {
    canvasRef.current?.clearCanvas();
  };

  // 제출 핸들러
  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      setError(null);

      let imageData: File | string;
      
      // 모드에 따른 이미지 데이터 처리
      if (mode === 'draw') {
        const canvas = await canvasRef.current?.exportImage('png');
        if (!canvas) throw new Error('캔버스 데이터를 가져올 수 없습니다.');
        imageData = canvas;
      } else {
        const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
        const file = fileInput.files?.[0];
        if (!file) throw new Error('파일을 선택해주세요.');
        imageData = file;
      }

      if (!type) throw new Error('유형이 선택되지 않았습니다.');

      // API 호출 및 결과 페이지로 이동
      const result = await analyzeImage(imageData, type);
      navigate('/result', { state: { result } });
    } catch (err) {
      setError(err instanceof Error ? err.message : '분석 중 오류가 발생했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  // UI 렌더링
  return (
    <div className="w-full h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-3xl mx-auto px-4"> {}
        <div className="text-center">
          {/* 제목 */}
          <h2 className="text-2xl font-bold text-gray-800 mb-4"> {}
            {type === 'house' ? '집' : type === 'tree' ? '나무' : '사람'}을 그려보세요
          </h2>

          {/* 모드 선택 버튼 */}
          <div className="flex justify-center gap-4 mb-4"> {}
            <button 
              onClick={() => setMode('draw')}
              className={`w-32 h-10 rounded-lg font-medium transition-colors duration-200 
                ${mode === 'draw' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-200 hover:bg-gray-300'}`}
            > {}
              직접 그리기
            </button>
            <button 
              onClick={() => setMode('upload')}
              className={`w-32 h-10 rounded-lg font-medium transition-colors duration-200
                ${mode === 'upload' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-200 hover:bg-gray-300'}`}
            > {}
              이미지 업로드
            </button>
          </div>

          {/* 그리기/업로드 영역 */}
          <div className="flex justify-center mb-4"> {}
            {mode === 'draw' ? (
              <div className="w-full max-w-xl"> {}
                <div className="w-[450px] h-[450px] mx-auto"> {}
                  <ReactSketchCanvas
                    ref={canvasRef}
                    width="100%"
                    height="100%"
                    strokeWidth={4}
                    strokeColor="black"
                    backgroundImage=""
                    exportWithBackgroundImage={true}
                    className="border-2 border-gray-300 rounded-lg"
                  />
                </div>
                <div className="flex justify-center gap-3 mt-4">
                  <button
                    onClick={handleUndo}
                    className="w-32 h-10 bg-gray-200 rounded-lg font-medium
                             hover:bg-gray-300 transition-colors duration-200"
                  > {}
                    ↩ 되돌리기
                  </button>
                  <button
                    onClick={handleClear}
                    className="w-34 h-10 bg-red-100 text-red-600 rounded-lg font-medium
                             hover:bg-red-200 transition-colors duration-200"
                  > {}
                    🗑 모두 지우기
                  </button>
                </div>
              </div>
            ) : (
              <div className="w-full max-w-xl text-center"> {}
                <div className="w-[450px] h-[450px] mx-auto border-2 border-gray-300 
                              rounded-lg flex items-center justify-center">
                  {}
                  <input
                    type="file"
                    accept="image/*"
                    className="w-full max-w-md"
                  />
                </div>
              </div>
            )}
          </div>

          {/* 에러 메시지 */}
          {error && (
            <div className="text-red-500 text-center mb-3"> {}
              {error}
            </div>
          )}

          {/* 제출 버튼 */}
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className={`w-32 h-10 bg-blue-500 text-white text-lg font-medium rounded-lg
                     transition-colors duration-200 
                     ${isLoading 
                       ? 'opacity-50 cursor-not-allowed' 
                       : 'hover:bg-blue-600'}`}
          > {}
            {isLoading ? '분석 중...' : '제출하기'} {}
          </button>
        </div>
      </div>
    </div>
);
}