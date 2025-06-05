import os
import cv2
import xml.etree.ElementTree as ET
from tqdm import tqdm

# 경로 설정
train_video_dir = r"C:\JAAD_train_clips"
test_video_dir = r"C:\JAAD_test_clips"
annotation_dir = r"C:\JAAD-JAAD_2.0\annotations"

# 결과 저장 디렉토리
train_img_dir = r"C:\parsed_dataset\train_img"
train_txt_dir = r"C:\parsed_dataset\train_txt"
test_img_dir = r"C:\parsed_dataset\test_img"
test_txt_dir = r"C:\parsed_dataset\test_txt"
temp_frame_dir = r"C:\JAAD_temp_frames"

# 디렉토리 생성
os.makedirs(train_img_dir, exist_ok=True)
os.makedirs(train_txt_dir, exist_ok=True)
os.makedirs(test_img_dir, exist_ok=True)
os.makedirs(test_txt_dir, exist_ok=True)
os.makedirs(temp_frame_dir, exist_ok=True)

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
    return frame_count

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
                look_value = "not-looking"

            look_binary = 1 if look_value == "not-looking" else 0

            if frame not in annotations:
                annotations[frame] = []

            annotations[frame].append({
                "bbox": (int(xtl), int(ytl), int(xbr), int(ybr)),
                "look": look_binary
            })
    return annotations

def process_split(video_dir, img_dir, txt_dir):
    for filename in tqdm(os.listdir(video_dir)):
        if not filename.endswith(".mp4"):
            continue

        video_id = os.path.splitext(filename)[0]
        video_path = os.path.join(video_dir, filename)
        xml_path = os.path.join(annotation_dir, f"{video_id}.xml")

        if not os.path.exists(xml_path):
            print(f"[경고] 주석 파일 없음: {xml_path}")
            continue

        # 프레임 추출
        extract_frames(video_path, temp_frame_dir)

        # 주석 로딩
        annotations = parse_annotations(xml_path)

        # 보행자 이미지 저장
        for frame_idx, data_list in annotations.items():
            frame_path = os.path.join(temp_frame_dir, f"{video_id}_frame{frame_idx:04}.jpg")
            if not os.path.exists(frame_path):
                continue
            image = cv2.imread(frame_path)
            if image is None:
                continue

            for i, item in enumerate(data_list):
                x1, y1, x2, y2 = item["bbox"]
                cropped = image[y1:y2, x1:x2]
                img_filename = f"{video_id}_frame{frame_idx:04}_ped{i}.jpg"
                txt_filename = img_filename.replace(".jpg", ".txt")

                cv2.imwrite(os.path.join(img_dir, img_filename), cropped)
                with open(os.path.join(txt_dir, txt_filename), "w") as f:
                    f.write(str(item["look"]))

# train과 test 각각 처리
print("▶ Train 영상 처리 중...")
process_split(train_video_dir, train_img_dir, train_txt_dir)
print("✅ Train 데이터 생성 완료!")

print("▶ Test 영상 처리 중...")
process_split(test_video_dir, test_img_dir, test_txt_dir)
print("✅ Test 데이터 생성 완료!")

print("\n🎉 모든 작업 완료! 프레임 및 보행자 crop + 라벨 저장 완료되었습니다.")
