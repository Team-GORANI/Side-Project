import React, { useEffect, useRef, useState } from 'react';
import { motion, useMotionValue, useSpring } from 'framer-motion';
import { Navbar } from '../components/Navbar';
import noiseImage from '../assets/images/noise.png';

// 자석 효과 설정
const SPRING_CONFIG = { damping: 100, stiffness: 400 };
const MAX_DISTANCE = 0.5;

// 자석 효과 버튼 컴포넌트
const MagneticButton: React.FC<{ onClick: () => void }> = ({ onClick }) => {
  const [isHovered, setIsHovered] = useState(false);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const buttonRef = useRef<HTMLDivElement>(null);
  const springX = useSpring(x, SPRING_CONFIG);
  const springY = useSpring(y, SPRING_CONFIG);

  useEffect(() => {
    const calculateDistance = (e: MouseEvent) => {
      if (buttonRef.current) {
        const rect = buttonRef.current.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const distanceX = e.clientX - centerX;
        const distanceY = e.clientY - centerY;

        if (isHovered) {
          x.set(distanceX * MAX_DISTANCE);
          y.set(distanceY * MAX_DISTANCE);
        } else {
          x.set(0);
          y.set(0);
        }
      }
    };

    document.addEventListener("mousemove", calculateDistance);
    return () => document.removeEventListener("mousemove", calculateDistance);
  }, [isHovered, x, y]);

  return (
    <motion.div
      ref={buttonRef}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        x: springX,
        y: springY,
      }}
    >
      <button
        onClick={onClick}
        className="py-3.5 px-9 text-white rounded-full text-xl shadow-lg transition-colors duration-200"
        style={{
          backgroundColor: '#0D3272',
          opacity: 1,
          zIndex: 2,
        }}
      >
        심리 분석 하러 가기
      </button>
    </motion.div>
  );
};

const Home: React.FC = () => {
  const circleRef = useRef<HTMLDivElement>(null);
  const innerCircleRef = useRef<HTMLDivElement>(null);

  return (
    <div className="relative w-full h-screen bg-white overflow-visible">
      {/* 원형 배경 */}
      <motion.div
        ref={circleRef}
        className="absolute rounded-full overflow-hidden"
        initial={{ opacity: 0, scale: 1 }}
        animate={{ 
          opacity: 1, 
          scale: 0.8,
          rotateZ: 360 // 360도 회전 애니메이션
        }}
        transition={{
          // 불투명도 애니메이션
          opacity: { 
            duration: 2, 
            ease: [0.29, 0, 1, 0.69],
            delay: 0 
          },
          scale: { 
            // 크기 애니메이션
            duration: 2, 
            ease: [0.29, 0, 1, 0.69],
            delay: 0 
          },
          // 회전 애니메이션
          rotateZ: {
            duration: 6,
            ease: [0, 0, 1, 1],
            repeat: Infinity,
            repeatType: "loop"
          }
        }}
        whileInView={{
          opacity: 1,
          scale: 1,
          transition: {
            duration: 2.1,
            ease: [0.98, 0.27, 0.56, 1],
            delay: 0.1
          }
        }}
        viewport={{ once: true }}
        style={{
          width: '1300px', // 너비
          height: '1000px', // 높이
          top: '-770px', // 위치
          left: 0,
          right: 0,
          margin: '0 auto',  
          background: 'conic-gradient(from 0deg at 50% 50%, #ff8000, #ffc300)', // conic gradient
          filter: 'blur(100px)', // Blur 효과 추가
          transition: 'transform 0.8s ease', // 부드러운 트랜지션 효과
          opacity: 1, // 불투명도
        }}
      >
        <motion.div
          animate={{ 
            rotateZ: 360,
            scale: [0.8, 1, 0.8]
          }}
          transition={{
            duration: 6,
            ease: "linear",
            repeat: Infinity,
            repeatType: "mirror"
          }}
          style={{
            backgroundImage: `url(${noiseImage})`, // public 폴더에 저장된 이미지 경로 사용
            backgroundRepeat: 'repeat', // 타일 방식으로 반복
            backgroundSize: '100%', // 크기를 100%로 맞추기
            opacity: 0.1, // 반투명 처리
            mixBlendMode: 'overlay',
            width: '100%',
            height: '100%',
            position: 'absolute',
            top: '0',
            left: '0',
            transformOrigin: 'center center',
          }}
        />
      </motion.div>

      {/* 전체 화면 밝기 조정 (배경 밝게 설정) */}
      <div
        className="absolute top-0 left-0 w-full h-full"
        style={{
          backgroundColor: 'rgba(255, 255, 255, 0.2)', // 밝은 흰색 배경
          opacity: 1, // opacity 1로 설정
          overflow: 'visible', // overflow visible 설정
        }}
      />

      {/* 흰색 원형 배경 애니메이션 */}
      <motion.div
        ref={innerCircleRef}
        initial={{ y: -200, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1, ease: "easeOut" }} // 1초동안 부드러운 트랜지션 
        className="absolute"
        style={{
          top: '-524px', // 고정된 위치
          left: 0,
          right: 0,
          margin: '0 auto',
          width: '736px', // 고정 크기
          height: '736px', // 고정 크기
          backgroundColor: '#FFFFFF', // 흰색 배경
          borderRadius: '50%', // 원형 모양
          zIndex: 1,
        }}
      />

      {/* 상단 네비게이션 바 */}
      <div className="fixed top-0 left-0 w-full z-50">
          <Navbar link="/" />
      </div>

      {/* Heading Text - 'HTP Test' */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2, duration: 0.8 }} // 1.2초 지연 후 0.8초 동안 페이드인 
        className="absolute w-full text-center"
        style={{
          top: '50%', // 텍스트가 중앙에 오도록
          left: '50%',
          transform: 'translate(-50%, -50%)', // 중앙 정렬
          fontFamily: 'Sansita Swashed, sans-serif', // 폰트 설정
          fontWeight: '300', // 폰트 두께
          fontStyle: 'italic', // 이탤릭체 적용
          color: '#3B3B3B', // 텍스트 색상
          fontSize: '96px', // 텍스트 크기 설정
          lineHeight: '1.2',
          width: '1216px', // 너비 설정
          whiteSpace: 'pre-wrap',
          wordWrap: 'break-word',
          zIndex: 2,
        }}
      >
        HTP Test
      </motion.div>

      {/* 부가 설명 텍스트 - "집-나무-사람 그림으로 심리를 분석해보세요!" */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.8, duration: 0.8 }} // 1.8초 지연 후 0.8초 동안 페이드인 
        className="absolute w-full text-center"
        style={{
          top: 'calc(50% + 100px)', // 텍스트 위치는 HTP Test 아래로
          left: '50%',
          transform: 'translate(-50%, -50%)', // 중앙 정렬
          fontFamily: 'Satashi, sans-serif', // 폰트 설정
          color: '#3B3B3B',
          fontSize: '24px', // 텍스트 크기 설정
          zIndex: 2,
        }}
      >
        집-나무-사람 그림으로 심리를 분석해보세요!
      </motion.div>

      {/* 버튼 */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2.6, duration: 0.8 }} // 2.6초 지연 후 0.8초 동안 페이드인 
        className="absolute"
        style={{
          top: 'calc(50% + 180px)',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 2,
        }}
      >
      <MagneticButton onClick={() => window.location.href = '/select'} /> 
      </motion.div>
    </div>
  );
};

export default Home;