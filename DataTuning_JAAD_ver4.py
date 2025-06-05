import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

# 실제 존재하는 test 프레임 이미지 경로
test_frame_dir = r"C:\JAAD_selected_test_frames"
annotation_dir = r"C:\JAAD-JAAD_2.0\annotations"
output_txt_dir = r"C:\JAAD_selected_test_txt"
os.makedirs(output_txt_dir, exist_ok=True)

# test 프레임 이미지 목록 가져오기
test_frames = [f for f in os.listdir(test_frame_dir) if f.endswith(".jpg")]

created_txt = []
skipped_frames = []

# 각 프레임에 대해 bbox + looking 라벨 저장
for fname in tqdm(test_frames, desc="라벨 txt 생성 중", unit="frame"):
    video_id, frame_str = fname.split("_frame")
    frame_num = int(frame_str.replace(".jpg", ""))
    xml_path = os.path.join(annotation_dir, f"{video_id}.xml")
    if not os.path.exists(xml_path):
        skipped_frames.append(fname)
        continue

    tree = ET.parse(xml_path)
    root = tree.getroot()

    labels = []

    for track in root.findall(".//track[@label='pedestrian']"):
        for box in track.findall("box"):
            if int(box.get("frame")) != frame_num:
                continue
            if box.get("outside") == "1":
                continue

            xtl = int(float(box.get("xtl")))
            ytl = int(float(box.get("ytl")))
            xbr = int(float(box.get("xbr")))
            ybr = int(float(box.get("ybr")))

            look_attr = box.findall(".//attribute[@name='look']")
            look_value = look_attr[0].text if look_attr else "not-looking"
            look_binary = 1 if look_value == "not-looking" else 0

            labels.append(f"{xbr} {xtl} {ybr} {ytl} {look_binary}")

    # 저장
    if labels:
        txt_filename = fname.replace(".jpg", ".txt")
        with open(os.path.join(output_txt_dir, txt_filename), "w") as f:
            f.write(" ".join(labels))
        created_txt.append(txt_filename)
    else:
        skipped_frames.append(fname)

# 최종 요약 출력
print(f"\n✅ 총 {len(created_txt)}개의 .txt 라벨 파일 생성 완료!")
print(f"⚠️ 보행자 정보가 없어 건너뛴 프레임 수: {len(skipped_frames)}")
