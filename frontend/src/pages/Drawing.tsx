import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ReactSketchCanvas, ReactSketchCanvasRef } from 'react-sketch-canvas';
import { useNavigate, useParams } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import { analyzeImage } from '../services/api';
import '../styles/pages/drawing.css';

const ERASER_SIZE = 20; // 지우개 크기
const PEN_SIZE = 4; // 펜 크기

// 그리기 타입 정의 (house/tree/person)
type DrawingType = 'house' | 'tree' | 'person';

// 애니메이션 variants
const containerVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

const contentVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

export default function Drawing() {
  // URL 파라미터에서 그리기 타입 추출 (house/tree/person)
  const { type } = useParams<{ type: string }>();
  const navigate = useNavigate();

  // 상태 관리
  const [mode, setMode] = useState<'draw' | 'upload'>('draw');   // 그리기/업로드 모드
  const [tool, setTool] = useState<'pen' | 'eraser'>('pen');     // 펜/지우개 도구
  const [isLoading, setIsLoading] = useState(false);             // 로딩 상태
  const [error, setError] = useState<string | null>(null);       // 에러 메시지
  const [isDragging, setIsDragging] = useState(false);           // 드래그 상태
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);   // 업로드된 파일
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);     // 미리보기 URL
  const [cursorPosition, setCursorPosition] = useState({ x: 0, y: 0 });  // 커서 위치

  // 캔버스 참조
  const canvasRef = useRef<ReactSketchCanvasRef>(null);

  // Blob URL 메모리 정리 (cleanup)
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  // type 유효성 검사
  const validateType = (param: string | undefined): DrawingType => {
    if (!param || !['house', 'tree', 'person'].includes(param)) {
      return 'house';
    }
    return param as DrawingType;
  };
  const validatedType = validateType(type);

  // 페이지 타이틀 설정
  const getTitle = () => {
    switch (validatedType) {
      case 'house': return 'Draw Your House!';
      case 'tree': return 'Draw Your Tree!';
      case 'person': return 'Draw Your Person!';
      default: return 'Draw Your House!';
    }
  };
  
  // 한글 라벨 설정
  const getLabel = () => {
    switch (validatedType) {
      case 'house': return '집';
      case 'tree': return '나무';
      case 'person': return '사람';
      default: return '알 수 없음';
    }
  };
  const label = getLabel(); // label 추출
  

  // 지우개 커서 위치 업데이트
  useEffect(() => {
    const updatePosition = (e: MouseEvent) => {
      if (tool === 'eraser') {
        const canvas = document.querySelector('.drawing-area');
        if (canvas) {
          const rect = canvas.getBoundingClientRect();
          // 캔버스 영역 내에서만 커서 표시
          if (
            e.clientX >= rect.left &&
            e.clientX <= rect.right &&
            e.clientY >= rect.top &&
            e.clientY <= rect.bottom
          ) {
            setCursorPosition({ x: e.clientX, y: e.clientY });
          }
        }
      }
    };

    window.addEventListener('mousemove', updatePosition);
    return () => window.removeEventListener('mousemove', updatePosition);
  }, [tool]);

  // 파일 처리 함수
  const handleFileChange = (file: File) => {
    setUploadedFile(file);
    const previewURL = URL.createObjectURL(file); // Blob URL 생성 (미리보기)
    setPreviewUrl(previewURL);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  // 파일 드롭 처리
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file?.type.startsWith('image/')) {
      handleFileChange(file);
    }
  };
  
  // 제출 핸들러
  const handleSubmit = async () => {
    try {
      setIsLoading(true);
      setError(null);

      let imageBase64 = '';
      if (mode === 'draw') {
        // 캔버스 이미지를 Base64 형식으로 가져오기
        imageBase64 = await canvasRef.current?.exportImage('png') ?? '';
      } else if (uploadedFile) {
        // 업로드된 파일을 Base64로 변환
        const reader = new FileReader();
        reader.readAsDataURL(uploadedFile);
            await new Promise((resolve) => {
                reader.onloadend = () => {
                    if (typeof reader.result === 'string') {
                        imageBase64 = reader.result;
                        resolve(null);
                    }
                };
            });
        }
        if (!imageBase64) {
            throw new Error(mode === 'draw' ? '그림을 그려주세요' : '파일을 선택해주세요');
        }

        // API 호출하여 분석 결과 받기
        const result = await analyzeImage(imageBase64, validatedType);
        console.log('Analysis result:', result);

        // 결과 페이지로 이동
        navigate('/result', { 
            state: { 
                label,
                image: imageBase64,
                analysis: result.analysis || '분석 결과를 불러올 수 없습니다.'
            } 
        });

    } catch (err) {
        console.error('Submit error:', err);
        setError(err instanceof Error ? err.message : '오류가 발생했습니다');
    } finally {
        setIsLoading(false);
    }
  };

  return (
    <div className="w-full min-h-screen flex flex-col bg-white">
      {/* 네비게이션 바 */}
      <Navbar style={{ width: '100%', position: 'sticky', top: 0, zIndex: 50 }} link="/" />

      <div className="flex-1 flex justify-center items-start pt-4">
        {/* 메인 컨테이너 */}
        <motion.div 
          className="drawing-page-container"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          {/* 배경 애니메이션 */}
          <motion.div 
            className="conic-animation-1"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          />
          <motion.div 
            className="conic-animation-2"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          />

          {/* 컨텐츠 영역 */}
          <motion.div
            variants={contentVariants}
            initial="hidden"
            animate="visible"
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            {/* 타이틀 */}
            <motion.h1 
              className="text-[64px] font-bold mb-8 text-white text-center"
              style={{ textShadow: '2px 2px 4px rgba(0, 0, 0, 0.2)', fontFamily: 'Lustria, serif' }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.7 }} 
            >
              {getTitle()}
            </motion.h1>

            {/* 모드 선택 버튼 (그리기/업로드) */}
            <motion.div className="flex justify-center gap-4 mb-8">
              {['draw', 'upload'].map((m) => (
                <button
                  key={m}
                  onClick={() => setMode(m as 'draw' | 'upload')}
                  className={`px-6 py-2 rounded-lg transition-all duration-200 
                    ${mode === m ? 'bg-white text-[#DE523A]' : 'bg-white/20 text-white hover:bg-white/30'}`}
                >
                  {m === 'draw' ? '✏️ 그리기' : '📁 업로드'}
                </button>
              ))}
            </motion.div>

            {/* 그리기/업로드 영역 */}
            <div className="relative w-full max-w-[900px] h-[500px] mx-auto overflow-hidden">
              {mode === 'draw' ? (
                <div className="drawing-container relative w-full h-full">
                  {/* ToolBar 컴포넌트 */}
                  <motion.div 
                    className="tools-container"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4 }}
                  >
                    <button 
                      onClick={() => setTool('pen')}
                      className={`tool-button ${tool === 'pen' ? 'active' : ''}`}
                    >
                      🖌️
                    </button>
                    <button 
                      onClick={() => setTool('eraser')}
                      className={`tool-button ${tool === 'eraser' ? 'active' : ''}`}
                    >
                      🧽
                    </button>
                  </motion.div>
                  
                  {/* 지우개 커서 */}
                  {tool === 'eraser' && (
                    <div
                      style={{
                        position: 'fixed',
                        left: cursorPosition.x - ERASER_SIZE,
                        top: cursorPosition.y - ERASER_SIZE,
                        width: ERASER_SIZE * 2,
                        height: ERASER_SIZE * 2,
                        border: '2px solid black',
                        borderRadius: '50%',
                        pointerEvents: 'none',
                        zIndex: 1000,
                        backgroundColor: 'rgba(255, 255, 255, 0.2)'
                      }}
                    />
                  )}

                  {/* 캔버스 */}
                  <div className="drawing-area w-full h-full">
                    <ReactSketchCanvas
                      ref={canvasRef}
                      width="100%"
                      height="100%"
                      strokeWidth={tool === 'pen' ? PEN_SIZE : ERASER_SIZE * 2}
                      strokeColor={tool === 'pen' ? 'black' : 'white'}
                      className={`bg-white rounded-[30px] ${tool === 'pen' ? 'pen-cursor' : ''}`}
                    />
                  </div>
                </div>
              ) : (
                // 업로드 모드
                <div 
                  className={`upload-area w-full h-full ${isDragging ? 'dragging' : ''}`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  {previewUrl ? (
                    <div className="relative w-full h-full">
                      <div className="w-full h-full bg-white rounded-[30px] overflow-hidden">
                        <img 
                          src={previewUrl} 
                          alt="업로드된 이미지" 
                          className="w-full h-full object-contain"
                        />
                      </div>
                      {/* 이미지 삭제 버튼 */}
                      <button
                        onClick={() => {
                          setUploadedFile(null);
                          setPreviewUrl(null);
                        }}
                        className="absolute -top-1 -right-1 w-8 h-8 bg-white rounded-full 
                                  flex items-center justify-center shadow-md hover:bg-gray-100 
                                  transition-all duration-200 border border-gray-200 z-[1000]"
                      >
                        ❌
                      </button>
                    </div>
                  ) : (
                    // 파일 업로드 영역
                    <label className="cursor-pointer text-center">
                      <input
                        type="file"
                        accept="image/*"
                        onChange={(e) => {
                          const file = e.target.files?.[0];
                          if (file) handleFileChange(file);
                        }}
                        className="hidden"
                      />
                      <div className="text-4xl mb-2">📁</div>
                      <p className="text-gray-600 mb-2">
                        클릭하여 이미지를 업로드하거나<br />
                        이미지를 여기로 드래그하세요
                      </p>
                      <p className="text-sm text-gray-400">
                        지원 형식: JPG, PNG
                      </p>
                    </label>
                  )}
                </div>
              )}
            </div>

            {error && (
              <div className="text-white text-center mt-4">{error}</div>
            )}

            {/* 제출 버튼 */}
            <motion.div className="text-center mt-8">
              <button
                onClick={handleSubmit}
                disabled={isLoading}
                className="submit-button"
              >
                {isLoading ? '분석 중...' : '분석결과 보러가기'}
              </button>
            </motion.div>
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}