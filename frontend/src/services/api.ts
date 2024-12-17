// src/services/api.ts

/**
 * 이미지 분석 함수
 * @param imageFile - 분석할 이미지 파일 또는 데이터 URL
 * @param type - 분석 유형 (집, 나무, 사람)
 * @returns 분석 결과 객체
 */
export const analyzeImage = async (
    imageFile: File | string,
    type: 'house' | 'tree' | 'person'
  ) => {
    try {
      // 임시 데이터 반환 (API 연동 전 테스트)
      return {
        originalImage: typeof imageFile === 'string' ? imageFile : URL.createObjectURL(imageFile),
        analysis: `이것은 ${type}에 대한 임시 분석 결과입니다. 당신의 그림에서는 [...] 특징이 보입니다.`,
        type: type
      };
  
      // API 구현 시 사용
      /*
      const formData = new FormData();
      if (typeof imageFile === 'string') {
        // 데이터 URL을 Blob으로 변환하여 FormData에 추가
        const blob = await fetch(imageFile).then(res => res.blob());
        formData.append('image', blob, 'drawing.png');
      } else {
       // File 객체를 직접 FormData에 추가
        formData.append('image', imageFile);
      }
      formData.append('type', type);

      // API 엔드포인트로 요청 전송
      const response = await api.post('/analyze', formData);
      return response.data;
      */
    } catch (error) {
      console.error('Image analysis failed:', error);
      throw error;
    }
  };
  