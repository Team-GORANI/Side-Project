import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

interface NavbarProps {
  style?: React.CSSProperties;
  link?: string;
}

export const Navbar = ({ style, link = "/" }: NavbarProps) => {
  return (
    // 네비게이션 바 컨테이너
    <nav 
      className="w-full px-8 py-6 sticky top-0 z-50 
                bg-gradient-to-b from-[rgb(250,250,250)] to-transparent
                md:px-6" 
      style={style}
    >
      {/* 내부 컨텐츠 컨테이너 */}
      <div className="ml-0 flex items-center">
        <Link to={link}>
          {/* 로고 컨테이너 - 호버/클릭 애니메이션 적용 */}
          <motion.div
            className="w-[50px] h-[50px] flex items-center justify-center p-2 cursor-pointer
                      md:w-[50px] md:h-[50px]"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            {/* 로고 SVG */}
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 44 44"
              className="w-[44px] h-[44px] md:w-[44px] md:h-[44px]"
            >
              {/* 그라데이션 */}
              <defs>
                <linearGradient 
                  id="logo-gradient" 
                  x1="0.498" 
                  x2="0.502" 
                  y1="0" 
                  y2="1"
                >
                  <stop offset="0" stopColor="rgb(250, 92, 64)" />
                  <stop offset="1" stopColor="rgb(255, 185, 94)" />
                </linearGradient>
              </defs>
              <path 
                d="M 0 22 C 13.984 22 22 13.984 22 0 C 22 13.984 30.016 22 44 22 C 30.016 22 22 30.016 22 44 C 22 30.016 13.984 22 0 22 Z" 
                fill="url(#logo-gradient)"
              />
            </svg>
          </motion.div>
        </Link>
      </div>
    </nav>
  );
};