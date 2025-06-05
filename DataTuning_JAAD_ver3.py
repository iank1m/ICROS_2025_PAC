import os
import shutil
from tqdm import tqdm  # 진행 상황 표시용

# 경로 설정
split_txt_path = r"C:\JAAD_default\test.txt"
all_frames_dir = r"C:\JAAD_temp_frames"
output_dir = r"C:\JAAD_selected_test_frames"
os.makedirs(output_dir, exist_ok=True)

# video ID 목록 로드
with open(split_txt_path, "r") as f:
    selected_videos = set(line.strip() for line in f if line.strip())

# 전체 프레임 파일 목록
all_files = [f for f in os.listdir(all_frames_dir) if f.endswith(".jpg")]

# tqdm으로 진행 표시
copied_files = []
for fname in tqdm(all_files, desc="복사 중", unit="파일"):
    video_id = fname.split("_frame")[0]
    if video_id in selected_videos:
        src = os.path.join(all_frames_dir, fname)
        dst = os.path.join(output_dir, fname)
        shutil.copy(src, dst)
        copied_files.append(fname)

print(f"\n✅ 총 {len(copied_files)}개의 이미지가 복사되었습니다.")
