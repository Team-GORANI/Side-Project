import React, { useEffect, useRef } from 'react';
import { Navbar } from '../components/Navbar';
import noiseImage from '../assets/images/noise.png';


const Home: React.FC = () => {
  const circleRef = useRef<HTMLDivElement>(null);
  const innerCircleRef = useRef<HTMLDivElement>(null);
  const textRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // 'layer in view' 트리거 효과 (IntersectionObserver 사용)
  useEffect(() => {
    const textElement = textRef.current;
    const buttonElement = buttonRef.current;

    if (textElement && buttonElement) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            textElement.classList.add('in-view'); // 애니메이션 트리거
            buttonElement.classList.add('in-view'); // 버튼 애니메이션 트리거
          }
        });
      }, { threshold: 0.5 }); // 50% 보였을 때 트리거

      observer.observe(textElement);

      return () => {
        if (textElement) {
          observer.unobserve(textElement);
        }
      };
    }
  }, []);

  return (
    <div className="relative w-full h-screen bg-white overflow-visible">
      {/* 원형 배경 */}
      <div
        ref={circleRef}
        className="absolute rounded-full overflow-hidden"
        style={{
          width: '1400px', // 너비
          height: '1000px', // 높이
          top: '-400px', // 위치
          left: '50%', // 좌우 중앙 정렬
          transform: 'translateX(-50%) perspective(1200px) scale(0.8)', // 중앙 정렬, perspective, scale
          background: 'conic-gradient(from 0deg at 50% 50%, #ff8000, #ffc300)', // conic gradient
          filter: 'blur(100px)', // Blur 효과 추가
          transition: 'transform 0.8s ease', // 부드러운 트랜지션 효과
          opacity: 1, // 불투명도
        }}
      >
        {/* 배경 이미지 추가 */}
        <div
          style={{
            backgroundImage: noiseImage, // public 폴더에 저장된 이미지 경로 사용
            backgroundRepeat: 'repeat', // 타일 방식으로 반복
            backgroundSize: '100%', // 크기를 100%로 맞추기
            opacity: 0.1, // 반투명 처리
            backgroundBlendMode: 'color-dodge', // 블렌딩 모드 설정
            width: '100%',
            height: '100%',
            position: 'absolute',
            top: '0',
            left: '0',
          }}
        />
      </div>

      {/* 전체 화면 밝기 조정 (배경 밝게 설정) */}
      <div
        className="absolute top-0 left-0 w-full h-full"
        style={{
          backgroundColor: 'rgba(255, 255, 255, 0.2)', // 밝은 흰색 배경
          opacity: 1, // opacity 1로 설정
          overflow: 'visible', // overflow visible 설정
        }}
      ></div>

      {/* 새로운 원형 배경 */}
      <div
        ref={innerCircleRef}
        className="absolute opacity-0 transition-opacity duration-1000 ease-in-out"
        style={{
          top: '-524px', // 고정된 위치
          left: '50%', // 좌우 중앙 정렬
          transform: 'translateX(-50%)', // 좌우 정확히 가운데 정렬
          width: '736px', // 고정 크기
          height: '736px', // 고정 크기
          backgroundColor: '#FFFFFF', // 흰색 배경
          opacity: 1, // 시작 시 opacity 0으로 설정
          borderRadius: '50%', // 원형 모양
          zIndex: 1,
          
        }}
      />
      {/* 상단 네비게이션 바 */}
            <div className="fixed top-0 left-0 w-full z-50">
              <Navbar link="/" />
            </div>

      
      {/* Heading Text - 'HTP Test' */}
      <div
        ref={textRef}
        className="absolute w-full text-center"
        style={{
          top: '50%', // 텍스트가 중앙에 오도록
          left: '50%',
          transform: 'translate(-50%, -50%)', // 중앙 정렬
          fontFamily: 'Sansita Swashed, sans-serif', // 폰트 설정
          fontWeight: 'regular', // 폰트 두께
          fontStyle: 'italic', // 이탤릭체 적용
          color: '#3B3B3B', // 텍스트 색상
          fontSize: '64px', // 텍스트 크기 설정
          lineHeight: '1.2',
          width: '1216px', // 너비 설정
          whiteSpace: 'pre-wrap',
          wordWrap: 'break-word',
          opacity: 1, // 바로 보이도록 설정 (애니메이션 없음)
          transition: 'none', // 애니메이션 없애기
        }}
      >
        HTP Test
      </div>

      {/* 추가 텍스트 - "집-나무-사람 그림으로 심리를 분석해보세요!" */}
      <div
        ref={textRef}
        className="absolute w-full text-center opacity-0 translate-y-10 transition-all duration-1000 ease-out"
        style={{
          top: 'calc(50% + 100px)', // 텍스트 위치는 HTP Test 아래로
          left: '50%',
          transform: 'translate(-50%, -50%)', // 중앙 정렬
          fontFamily: 'Satashi, sans-serif', // 폰트 설정
          color: '#3B3B3B',
          fontSize: '24px', // 텍스트 크기 설정
          opacity: 1, // 시작 시 opacity 0으로 설정
        }}
      >
        집-나무-사람 그림으로 심리를 분석해보세요!
      </div>

      {/* 버튼 */}
      <button
        ref={buttonRef}
        onClick={() => window.location.href = '/select'} // 페이지 이동
        className="absolute mt-8 py-3 px-12 text-white rounded-full text-xl shadow-lg hover:bg-blue-600 transition-colors duration-200"
        style={{
          backgroundColor: '#0D3272', // 버튼 색상 변경
          top: 'calc(50% + 180px)', // 버튼은 텍스트 아래에 위치
          left: '50%',
          transform: 'translateX(-50%)', // 좌우 중앙 정렬
          opacity: 1, // 바로 보이도록 설정
          zIndex: 2, // 버튼이 다른 요소들 위에 오도록 설정
        }}
      >
        심리 분석 하러 가기
      </button>
    </div>
  );
};

export default Home;