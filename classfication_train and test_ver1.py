#프레임별 + 보행자별 쪼개진 사진들의 10%만 test폴더 만들어서 옮기기 (나머지는 90%는 그대로 -> train)

import os
import shutil
import random

# 원본 경로
img_dir = r"C:\parsed_dataset\img"
txt_dir = r"C:\parsed_dataset\txt"

# 테스트셋 이동 대상 경로
test_img_dir = r"C:\parsed_dataset\test_img"
test_txt_dir = r"C:\parsed_dataset\test_txt"

# 폴더 없으면 만들기
os.makedirs(test_img_dir, exist_ok=True)
os.makedirs(test_txt_dir, exist_ok=True)

# 전체 파일 목록 (확장자 .jpg 기준)
all_imgs = [f for f in os.listdir(img_dir) if f.endswith(".jpg")]
print(f"전체 이미지 개수: {len(all_imgs)}")

# 고정된 무작위 시드
random.seed(42)

# 10%만 선택
test_count = int(len(all_imgs) * 0.1)
test_imgs = random.sample(all_imgs, test_count)

# 이동
for img_name in test_imgs:
    txt_name = img_name.replace(".jpg", ".txt")
    # 원본 경로
    img_path = os.path.join(img_dir, img_name)
    txt_path = os.path.join(txt_dir, txt_name)
    # 대상 경로
    new_img_path = os.path.join(test_img_dir, img_name)
    new_txt_path = os.path.join(test_txt_dir, txt_name)

    if os.path.exists(img_path) and os.path.exists(txt_path):
        shutil.move(img_path, new_img_path)
        shutil.move(txt_path, new_txt_path)
    else:
        print(f"[경고] 매칭 실패: {img_name} 또는 {txt_name} 없음")

print(f"\n✅ 테스트셋 10% ({test_count}개) 이동 완료!")
print(f"→ {test_img_dir}")
print(f"→ {test_txt_dir}")
