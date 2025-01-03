import React from 'react';
import { motion } from 'framer-motion';
import { useLocation } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import '../styles/pages/selection.css';

interface LocationState {
  label: string;
  image: string;
  analysis: string;
}

const Result: React.FC = () => {
  const location = useLocation();
  const { label, image, analysis } = location.state as LocationState || {
    label: '',
    image: '',
    analysis: ''
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 }
  };

  return (
    <div className="w-full min-h-screen">
      {/* 네비게이션 바 */}
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar link="/" />
      </div>

      {/* 배경 애니메이션 */}
      <div className="absolute top-0 left-0 right-0 h-screen overflow-hidden">
        <div className="gradient-container">
          {['white', 'orange-light', 'orange-dark'].map((color) => (
            <motion.div
              key={color}
              className={`gradient-${color}`}
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.85 }}
              transition={{ duration: 1, delay: 0.3 }}
            />
          ))}
        </div>
      </div>

      {/* 메인 컨텐츠 */}
      <motion.div
        className="pt-24 px-20 flex flex-col items-center relative z-10"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        transition={{ duration: 0.5 }}
      >
        {/* 중앙 정렬된 제목 섹션 */}
        <div className="w-full text-center mb-10">
          <motion.h1
            className="text-6xl font-bold italic mb-4"
            style={{ fontFamily: 'Sansita Swashed, sans-serif' }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            HTP Test Result
          </motion.h1>
          <motion.p
            className="text-lg"
            style={{ fontFamily: 'Inter, sans-serif' }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            {`${label} 그림으로 심리를 분석한 결과입니다.`}
          </motion.p>
        </div>

        {/* 상단 - 이미지 섹션 */}
        <div className="w-full max-w-4xl mb-10">
          {image && (
            <motion.div
              className="rounded-lg overflow-hidden shadow-lg"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <img
                src={image}
                alt="Analysis Result"
                className="w-full h-auto"
                style={{ maxHeight: '500px', objectFit: 'contain' }}
              />
            </motion.div>
          )}
        </div>

        {/* 하단 - 분석 결과 섹션 */}
        <div className="w-full max-w-4xl">
          <motion.div
            className="rounded-lg p-8 mb-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <h2 
              className="text-2xl font-bold mb-6"
              style={{ fontFamily: 'Lustria, serif' }}
            >
              {`${label.toUpperCase()} Drawing Analysis`}
            </h2>
            <div 
              className="whitespace-pre-line text-gray-700"
              style={{ 
                fontFamily: 'Inter, sans-serif',
                fontSize: '16px',
                lineHeight: '1.8'
              }}
            >
              {analysis}
            </div>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};

export default Result;