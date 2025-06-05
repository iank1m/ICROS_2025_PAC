import os
import cv2
import xml.etree.ElementTree as ET
from tqdm import tqdm

# 경로 설정
# 추출할 동영상들
video_dir = "C:/JAAD_clips" 
# 추출할 주석 파일 위치
annotation_dir = "C:/JAAD-JAAD_2.0/annotations"
# 만들 폴더
output_img_dir = "C:/parsed_dataset/img"
output_txt_dir = "C:/parsed_dataset/txt"
# 우선 프레임으로 쪼갠 사진들 저장할 위치
temp_frames_dir = "C:/JAAD_temp_frames"

# 디렉토리 생성
os.makedirs(output_img_dir, exist_ok=True)
os.makedirs(output_txt_dir, exist_ok=True)
os.makedirs(temp_frames_dir, exist_ok=True)

def extract_frames(video_path, output_dir):
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    basename = os.path.basename(video_path).split(".")[0]

    for i in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_dir, f"{basename}_frame{i:04}.jpg")
        cv2.imwrite(frame_filename, frame)
    cap.release()
    print(f"Extracted {frame_count} frames from {video_path}")

def parse_annotations(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    annotations = {}

    for track in root.findall(".//track[@label='pedestrian']"):
        for box in track.findall("box"):
            if box.get("outside") == "1":
                continue
            frame = int(box.get("frame"))
            xtl = float(box.get("xtl"))
            ytl = float(box.get("ytl"))
            xbr = float(box.get("xbr"))
            ybr = float(box.get("ybr"))

            # look attribute
            look_attr = box.findall(".//attribute[@name='look']")
            if look_attr:
                look_value = look_attr[0].text
            else:
                look_value = "not-looking"  # 기본값

            look_binary = 1 if look_value == "not-looking" else 0

            if frame not in annotations:
                annotations[frame] = []

            annotations[frame].append({
                "bbox": (int(xtl), int(ytl), int(xbr), int(ybr)),
                "look": look_binary
            })
    return annotations

# 전체 처리
for filename in tqdm(os.listdir(video_dir)):
    if not filename.endswith(".mp4"):
        continue
    video_id = os.path.splitext(filename)[0]
    video_path = os.path.join(video_dir, filename)
    xml_path = os.path.join(annotation_dir, f"{video_id}.xml")

    if not os.path.exists(xml_path):
        print(f"주석 파일 없음: {xml_path}")
        continue

    # 1. 프레임 추출
    extract_frames(video_path, temp_frames_dir)

    # 2. 주석 파싱
    annotations = parse_annotations(xml_path)

    # 3. 프레임별로 이미지 저장
    for frame_idx, data_list in annotations.items():
        frame_path = os.path.join(temp_frames_dir, f"{video_id}_frame{frame_idx:04}.jpg")
        if not os.path.exists(frame_path):
            continue
        image = cv2.imread(frame_path)

        for i, item in enumerate(data_list):
            x1, y1, x2, y2 = item["bbox"]
            cropped = image[y1:y2, x1:x2]

            img_filename = f"{video_id}_frame{frame_idx:04}_ped{i}.jpg"
            txt_filename = img_filename.replace(".jpg", ".txt")

            cv2.imwrite(os.path.join(output_img_dir, img_filename), cropped)
            with open(os.path.join(output_txt_dir, txt_filename), "w") as f:
                f.write(str(item["look"]))

print("작업 완료!!!!")