import os
import shutil
import random

# 경로 설정
video_dir = r"C:\JAAD_clips"
train_dir = r"C:\JAAD_train_clips"
test_dir = r"C:\JAAD_test_clips"

# 폴더 생성
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# 동영상 리스트 불러오기
video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]
print(f"전체 동영상 수: {len(video_files)}")

# 222개는 train, 나머지는 124개는 test용으로 먼저 분리
# 랜덤추출을 위해 셔플해놓고 그냥 파싱
random.seed(42)
random.shuffle(video_files)
train_videos = video_files[:222]
test_videos = video_files[222:]

# 이동 (move하고싶지만 혹시나 혹시나 모르니 일단 카피피)
for f in train_videos:
    shutil.copy(os.path.join(video_dir, f), os.path.join(train_dir, f))

for f in test_videos:
    shutil.copy(os.path.join(video_dir, f), os.path.join(test_dir, f))

print(f"\n✅ 완료: train={len(train_videos)}개, test={len(test_videos)}개")
