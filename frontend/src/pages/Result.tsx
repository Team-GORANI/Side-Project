import React, { useEffect, useRef,useState } from 'react';
import { motion } from 'framer-motion'; // framer-motion 추가
import { useLocation } from 'react-router-dom';
import { Navbar } from '../components/Navbar';

const Result: React.FC = () => {
  const location = useLocation();
  const backgroundRef = useRef<HTMLDivElement>(null);
  const label = location.state?.label || ' '; // 전달된 label 읽기

  // 전달된 이미지 데이터 가져오기
  const [image, setImage] = useState<string | null>(null);

  useEffect(() => {
    // 로컬 스토리지에서 이미지 가져오기
    const drawnImage = localStorage.getItem('drawnImage');
    const uploadedImage = localStorage.getItem('uploadedImage');

    if (drawnImage) {
      setImage(drawnImage);
    } else if (uploadedImage) {
      setImage(uploadedImage);
    }
  }, []);
  // 애니메이션 variants
  const gradientVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  };
  // 애니메이션 variants
  const textVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
  };

  return (
    <div className="w-full h-screen overflow-y-scroll">
      {/* 상단 네비게이션 바 */}
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar link="/" />
      </div>

      {/* 위 섹션 */}
      <motion.section
        className="relative flex justify-center items-center h-screen bg-white"
        initial="hidden"
        animate="visible"
        transition={{ staggerChildren: 0.3 }}
      >
        {/* 배경 그라데이션 
          - 세 개의 레이어로 구성된 동적 그라데이션 */}
      <div className="absolute top-0 left-0 right-0 h-screen overflow-hidden">
        <div className="gradient-container">
          {['white', 'orange-light', 'orange-dark'].map((color) => (
            <motion.div
              key={color}
              className={`gradient-${color}`}
              initial="hidden"
              animate="visible"
              variants={gradientVariants}
              transition={{ duration: 1, delay: 0.3 }}
            />
          ))}
        </div>
      </div>

        {/* 텍스트 섹션 */}
        <div className="absolute top-20 left-20">
          
        <motion.h1
            className="text-6xl font-bold italic"
            style={{
              fontFamily: 'Sansita Swashed, sans-serif',
              color: '#3B3B3B',
            }}
            variants={textVariants}
            initial="hidden"
            animate="visible"
            transition={{ duration: 0.6, delay: 1.2 }}
          >
            HTP Test Result
          </motion.h1>
          <motion.p
            className="mt-8 text-lg"
            style={{
              fontFamily: 'Sansita Swashed, sans-serif',
              color: '#3B3B3B',
            }}
            variants={textVariants}
            initial="hidden"
            animate="visible"
            transition={{ duration: 0.6, delay: 1.4 }}
          >
            {`${label} 그림으로 심리를 분석한 결과입니다.`}
          </motion.p>
        </div>

        {/* 그림 영역 */}
        <motion.div
          className="relative mt-32 flex justify-center"
          variants={textVariants}
          initial="hidden"
          animate="visible"
          transition={{ duration: 0.6, delay: 1.6 }}
        >
          {image ? (
            <img
              src={image} // 전달받은 이미지 렌더링
              alt="Analysis Result"
              className="rounded-lg shadow-lg"
              style={{
                width: '100%',
                height: 'auto',
                display: 'block',
                margin: '0 auto',
              }}
            />
          ) : (
            <p>이미지가 없습니다.</p> // 이미지가 없는 경우 표시
          )}
        </motion.div>
      </motion.section>


      {/* 아래 섹션 */}
      <motion.section
        className="h-[85vh] bg-white flex justify-center items-center mt-[-250px]"
        initial="hidden"
        animate="visible"
        variants={textVariants}
        transition={{ staggerChildren: 0.3, delayChildren: 1.8 }}
      >
        {/* 왼쪽 섹션 */}
        <div className="flex flex-col space-y-30 text-left w-2/5">
          <motion.div variants={textVariants}>
            <p
              style={{
                fontFamily: 'Recoleta Alt, sans-serif',
                color: '#5C6470',
                fontSize: '18px',
              }}
            >
              keyword
            </p>
            <h2
              style={{
                fontFamily: 'Instrument Sans, sans-serif',
                color: '#2E3238',
                fontSize: '28px',
                marginTop: '8px',
              }}
            >
              현실적
            </h2>
          </motion.div>

          <motion.div variants={textVariants}>
            <p
              style={{
                fontFamily: 'Recoleta Alt, sans-serif',
                color: '#5C6470',
                fontSize: '18px',
              }}
            >
              keyword
            </p>
            <h2
              style={{
                fontFamily: 'Instrument Sans, sans-serif',
                color: '#2E3238',
                fontSize: '28px',
                marginTop: '8px',
              }}
            >
              안정성
            </h2>
          </motion.div>

          <motion.div variants={textVariants}>
            <p
              style={{
                fontFamily: 'Recoleta Alt, sans-serif',
                color: '#5C6470',
                fontSize: '18px',
              }}
            >
              keyword
            </p>
            <h2
              style={{
                fontFamily: 'Instrument Sans, sans-serif',
                color: '#2E3238',
                fontSize: '28px',
                marginTop: '8px',
              }}
            >
              심리적 억압
            </h2>
          </motion.div>
        </div>

        {/* 오른쪽 섹션 */}
        <div className="flex flex-col space-y-5 text-left w-2/5">
          <motion.h2
            style={{
              fontFamily: 'Lustria, serif',
              textTransform: 'capitalize',
              fontSize: '28px',
              color: '#2E3238',
            }}
            variants={textVariants}
          >
            HOUSE Drawing Analysis
          </motion.h2>

          {['🔅 성격 특징 🔅', '🌤️ 대인 관계 🌤️', '🧘 현재 심리 상태 🧘', '💪 멘탈 케어 Tips 💪'].map((text, index) => (
            <motion.div
              key={index}
              variants={textVariants}
              style={{
                fontFamily: 'Sansita Swashed, sans-serif',
                fontSize: '24px',
                color: '#3B3B3B',
              }}
            >
              {text}
            </motion.div>
          ))}
        </div>
      </motion.section>
    </div>
  );
};

export default Result;