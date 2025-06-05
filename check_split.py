import os
import pandas as pd

# split 기준 경로 및 대상 split 목록
split_dir = r"C:\JAAD-JAAD_2.0\split_ids\default"
splits = {
    "train": {
        "txt_file": "train.txt",
        "img_dir": r"C:\parsed_dataset_split\train_img",
        "txt_dir": r"C:\parsed_dataset_split\train_txt"
    },
    "val": {
        "txt_file": "val.txt",
        "img_dir": r"C:\parsed_dataset_split\val_img",
        "txt_dir": r"C:\parsed_dataset_split\val_txt"
    },
    "test": {
        "txt_file": "test.txt",
        "img_dir": r"C:\parsed_dataset_split\test_img",
        "txt_dir": r"C:\parsed_dataset_split\test_txt"
    }
}

summary_data = []
all_missing = {}

for split_name, split_info in splits.items():
    split_path = os.path.join(split_dir, split_info["txt_file"])
    with open(split_path, "r") as f:
        video_ids = set(line.strip() for line in f if line.strip())

    img_counts = {vid: 0 for vid in video_ids}
    txt_counts = {vid: 0 for vid in video_ids}

    for fname in os.listdir(split_info["img_dir"]):
        if not fname.endswith(".jpg"):
            continue
        vid = fname.split("_frame")[0]
        if vid in img_counts:
            img_counts[vid] += 1

    for fname in os.listdir(split_info["txt_dir"]):
        if not fname.endswith(".txt"):
            continue
        vid = fname.split("_frame")[0]
        if vid in txt_counts:
            txt_counts[vid] += 1

    # 누락된 video ID 수집
    missing = [vid for vid in video_ids if img_counts[vid] == 0 and txt_counts[vid] == 0]
    all_missing[split_name] = missing

    for vid in sorted(video_ids):
        summary_data.append({
            "split": split_name,
            "video_id": vid,
            "img_count": img_counts[vid],
            "txt_count": txt_counts[vid]
        })

df_summary = pd.DataFrame(summary_data)
print(df_summary)

print(all_missing)
