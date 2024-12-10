import os

# 파일 이름 변경 함수

def rename_files_in_folder(folder_path):
    # 폴더 내 파일 목록 가져오기
    files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.txt'))]
    files.sort()  # 파일을 정렬 (일관된 순서 보장)
    
    # 숫자로 파일 이름 변경
    count = 1
    base_name = str(count).zfill(5)  # 첫 번째 이름 설정
    for file in files:
        # 파일 확장자 분리
        file_ext = os.path.splitext(file)[-1]
        
        # 새로운 파일 이름
        new_name = f"{base_name}{file_ext}"
        
        # 파일 경로
        old_file = os.path.join(folder_path, file)
        new_file = os.path.join(folder_path, new_name)
        
        # 파일 이름 변경
        os.rename(old_file, new_file)
        
        # 다음 번호로 진행
        if file.endswith('.txt'):  # txt 파일 이름이 끝났으면 번호 증가
            count += 1
            base_name = str(count).zfill(5)

# 'train' 폴더와 'val' 폴더에서 파일 이름 변경
train_image_folder = "C:/Users/Windows/Desktop/Side_Project/data/house/train/image"
val_image_folder = "C:/Users/Windows/Desktop/Side_Project/data/house/val/image"

rename_files_in_folder(train_image_folder)
rename_files_in_folder(val_image_folder)

print("파일 이름 변경 완료")


# 'train' 폴더와 'val' 폴더에서 파일 이름 변경
train_image_folder = "C:/Users/Windows/Desktop/Side_Project/data/house/train/image"
val_image_folder = "C:/Users/Windows/Desktop/Side_Project/data/house/val/image"

rename_files_in_folder(train_image_folder)
rename_files_in_folder(val_image_folder)

print("파일 이름 변경 완료")