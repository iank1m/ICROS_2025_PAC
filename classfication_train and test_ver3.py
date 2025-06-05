import os
import shutil

# split 기준 경로
split_dir = r"C:\JAAD-JAAD_2.0\split_ids\default"
input_img_dirs = [r"C:\parsed_dataset\train_img", r"C:\parsed_dataset\test_img"]
input_txt_dirs = [r"C:\parsed_dataset\train_txt", r"C:\parsed_dataset\test_txt"]

# 새로 정리할 폴더
base_out_dir = r"C:\parsed_dataset_split"
split_names = ['train', 'val', 'test']
output_dirs = {}

for split in split_names:
    output_dirs[f"{split}_img"] = os.path.join(base_out_dir, f"{split}_img")
    output_dirs[f"{split}_txt"] = os.path.join(base_out_dir, f"{split}_txt")
    os.makedirs(output_dirs[f"{split}_img"], exist_ok=True)
    os.makedirs(output_dirs[f"{split}_txt"], exist_ok=True)

# split 파일 로딩
split_video_ids = {}
for split in split_names:
    with open(os.path.join(split_dir, f"{split}.txt"), "r") as f:
        split_video_ids[split] = set(line.strip() for line in f if line.strip())

# 모든 입력 이미지 폴더에서 반복 처리
moved_counts = {'train': 0, 'val': 0, 'test': 0}
unmatched = []

for img_dir, txt_dir in zip(input_img_dirs, input_txt_dirs):
    for fname in os.listdir(img_dir):
        if not fname.endswith(".jpg"):
            continue
        video_id = fname.split("_frame")[0]  # 예: video_0012

        found = False
        for split in split_names:
            if video_id in split_video_ids[split]:
                # 이미지와 라벨 이동
                src_img = os.path.join(img_dir, fname)
                dst_img = os.path.join(output_dirs[f"{split}_img"], fname)
                shutil.copy(src_img, dst_img)

                txt_name = fname.replace(".jpg", ".txt")
                src_txt = os.path.join(txt_dir, txt_name)
                dst_txt = os.path.join(output_dirs[f"{split}_txt"], txt_name)
                if os.path.exists(src_txt):
                    shutil.copy(src_txt, dst_txt)

                moved_counts[split] += 1
                found = True
                break

        if not found:
            unmatched.append(fname)

moved_counts, len(unmatched)
