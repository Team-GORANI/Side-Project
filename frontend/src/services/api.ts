import axios from 'axios';

// axios 인스턴스 생성
const api = axios.create({
    baseURL: 'http://localhost:8000', // FastAPI 서버 주소
    headers: {
        'Content-Type': 'application/json',
    },
});

// 이미지 분석 함수
export const analyzeImage = async (
    imageFile: File | string,
    type: 'house' | 'tree' | 'person' // 분석 타입
) => {
    try {
        const formData = new FormData();
        
        if (typeof imageFile === 'string') {
            try {
                // Base64 이미지를 Blob으로 변환
                const base64Data = imageFile.split(',')[1];
                const byteCharacters = atob(base64Data);
                const byteArray = new Uint8Array(byteCharacters.length);
                
                // 바이트 배열로 변환
                for (let i = 0; i < byteCharacters.length; i++) {
                    byteArray[i] = byteCharacters.charCodeAt(i);
                }
                
                // Blob 생성 및 FormData에 추가
                const blob = new Blob([byteArray], { type: 'image/png' });
                formData.append('image', blob, 'drawing.png');
            } catch (error) {
                console.error('Error converting base64 to blob:', error);
                throw new Error('이미지 변환에 실패했습니다.');
            }
        } else {
            formData.append('image', imageFile);
        }
        
        formData.append('type', type);

        // API 요청 전송
        const response = await api.post('/api/detect', formData, {
          headers: {
              'Content-Type': 'multipart/form-data',  
          },
      });

      console.log('API Response:', response.data);

        if (response.data.status === 'error') {
            throw new Error(response.data.message || '이미지 분석에 실패했습니다.');
        }

        // 분석 결과 텍스트 처리
        let analysisText = response.data.analysis;
        if (Array.isArray(analysisText)) {
            analysisText = analysisText.join('\n');
        } else if (!analysisText) {
            analysisText = '분석 결과를 불러올 수 없습니다.';
        }

        // 성공 응답 반환
        return {
            status: 'success',
            originalImage: typeof imageFile === 'string' ? imageFile : URL.createObjectURL(imageFile),
            analysis: analysisText,
            boxes: response.data.boxes || []
        };

    } catch (error) {
        console.error('Image analysis failed:', error);
        throw error instanceof Error ? error : new Error('알 수 없는 오류가 발생했습니다.');
    }
};