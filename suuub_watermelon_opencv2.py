import cv2
import numpy as np
import os


def detect_and_save_faces(input_image_path, output_image_path, min_face_size=50):
    image = cv2.imread(input_image_path)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )

    for i, (x, y, w, h) in enumerate(faces):
        if w > min_face_size and h > min_face_size:
            mask = np.zeros_like(image, dtype=np.uint8)
            cv2.circle(
                mask,
                (x + w // 2, y + h // 2),
                min(w, h) // 2,
                (255, 255, 255),
                thickness=cv2.FILLED,
            )

            face_region = image[y : y + h, x : x + w]
            result_image = np.zeros_like(face_region, dtype=np.uint8)

            cv2.bitwise_and(face_region, mask[y : y + h, x : x + w], dst=result_image)

            result_image_bgra = cv2.cvtColor(result_image, cv2.COLOR_BGR2BGRA)
            result_image_bgra[mask[y : y + h, x : x + w, 0] == 0, 3] = 0

            cv2.imwrite(f"{output_image_path}_{i+1}.png", result_image_bgra)


# 폴더 내의 모든 이미지 파일을 처리하는 함수
def process_images_in_folder(folder_path, output_folder, min_face_size=60):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename.replace(".", "_result."))
            detect_and_save_faces(image_path, output_path, min_face_size)


if __name__ == "__main__":
    input_folder_path = "/Users/ohuseel/Desktop/imgame/input"
    output_folder_path = "/Users/ohuseel/Desktop/imgame/output"

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # 얼굴 크기가 최소 100 이상인 경우에만 저장함
    process_images_in_folder(input_folder_path, output_folder_path, min_face_size=100)
