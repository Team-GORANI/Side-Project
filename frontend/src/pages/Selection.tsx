import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Navbar } from '../components/Navbar';
import houseImage from '../assets/images/house.png';
import treeImage from '../assets/images/tree.png';
import personImage from '../assets/images/person.png';
import '../styles/pages/selection.css';

// 테스트 타입 정의
type TestOption = {
  id: 'house' | 'tree' | 'person';
  label: string;
  description: string;
  buttonText: string;
  image: string;
}

// 테스트 옵션 데이터
const testOptions: TestOption[] = [
  { 
    id: 'house', 
    label: 'Home', 
    description: '집으로 심리분석하기',
    buttonText: '집 그리기',
    image: houseImage
  },
  { 
    id: 'tree', 
    label: 'Tree', 
    description: '나무로 심리분석하기',
    buttonText: '나무 그리기',
    image: treeImage
  },
  { 
    id: 'person', 
    label: 'Person', 
    description: '사람으로 심리분석하기',
    buttonText: '사람 그리기',
    image: personImage
  },
];

export default function Selection() {
  const navigate = useNavigate();
  
  // 그라데이션 애니메이션 설정
  const gradientVariants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1 }
  };

  // 선택한 옵션의 그리기 페이지로 이동
  const handleOptionSelect = (optionId: string, label: string) => {
  navigate(`/drawing/${optionId}`, { state: { label } }); // `state`로 label 전달
  };


  return (
    <div className="w-full min-h-screen flex flex-col bg-gray-50">
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

      {/* 상단 네비게이션 바 */}
      <div className="fixed top-0 left-0 w-full z-50">
        <Navbar link="/" />
      </div>

      {/* 메인 컨텐츠 */}
      <div className="flex-1 flex justify-center pt-32">
        <div className="w-full max-w-[1200px] px-6 relative z-10">
          {/* 타이틀 섹션 */}
          <motion.div 
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.2 }}
          >
            <h1
              className="text-[70px] text-gray-900 mb-4"
              style={{ fontFamily: 'Sansita Swashed, cursive' }}
            >
              Select Test Type
            </h1>
            <p className="text-xl text-gray-600">
              집-나무-사람 중 그리고 싶은 대상을 선택하세요.
            </p>
          </motion.div>

          {/* 카드 그리드 */}
          <div className="w-full flex gap-6 justify-center">
            {testOptions.map((option, index) => (
              <motion.div
                key={option.id}
                className="group relative w-[350px] h-[450px] bg-white rounded-[20px] overflow-hidden
                         shadow-md cursor-pointer transition-all duration-300"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 1.5 + index * 0.2 }}
              >
                {/* 카드 이미지 */}
                <div className="absolute inset-0">
                  <img 
                    src={option.image} 
                    alt={option.label}
                    className="w-full h-full object-cover"
                  />
                </div>

                {/* 호버 오버레이 */}
                <div className="absolute inset-0 bg-black/60 opacity-0 
                              group-hover:opacity-100 transition-all duration-300
                              backdrop-blur-sm" />
                
                {/* 카드 컨텐츠 */}
                <div className="absolute inset-x-0 bottom-0 p-6 pt-[3px]
                              transform translate-y-[calc(100%-4rem)] 
                              group-hover:translate-y-0
                              transition-transform duration-300 ease-out">
                  <h2 className="text-4xl font-bold text-white mb-4" 
                      style={{ fontFamily: 'Lustria, serif' }}>
                    {option.label}
                  </h2>
                  
                  <p className="text-lg text-white mb-6"
                     style={{ fontFamily: 'Inter, sans-serif' }}>
                    {option.description}
                  </p>

                  {/* 액션 버튼 */}
                  <div className="flex justify-start">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleOptionSelect(option.id, option.label);
                      }}
                      className="flex items-center justify-between 
                                bg-[#0D3272] text-white rounded-[20px]
                                transition-colors duration-200 hover:bg-[#FA8E41]
                                group/btn w-[155px] h-[44px]"  
                    >
                      <span className="pl-6 whitespace-nowrap" 
                            style={{ fontFamily: 'Inter, sans-serif' }}>
                        {option.buttonText}
                      </span>
                      {/* 버튼 아이콘 */}
                      <div className="w-[40px] h-[40px] bg-white rounded-full 
                                    flex items-center justify-center
                                    transition-colors duration-200
                                    group-hover/btn:bg-white
                                    -mr-[1px]">
                        <svg 
                          className="w-4 h-4 text-[#0D3272]
                                   transition-colors duration-200
                                   group-hover/btn:text-[#FA8E41]" 
                          viewBox="0 0 24 24" 
                          fill="none" 
                          stroke="currentColor" 
                          strokeWidth="2"
                        >
                          <path d="M5 12h14M12 5l7 7-7 7"/>
                        </svg>
                      </div>
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}