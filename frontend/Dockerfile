FROM node:latest
WORKDIR /app

# Insatll package
COPY package*.json ./
RUN npm install

# Copy source code
COPY . .

# Vite 개발 서버가 모든 인터페이스에서 접근 가능하도록 설정
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]