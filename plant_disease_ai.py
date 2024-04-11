from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np
import json
import tkinter as tk
from tkinter import filedialog

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("plant_disease.h5", compile=False)

# Load the class names
with open('class_indices.json', 'r') as f:
    class_names = list(json.load(f).keys())

# Định nghĩa thông tin về loại bệnh và phương pháp chữa trị
disease_info = {
    'Apple___Apple_scab': ('Bệnh đạo ôn trên táo', 'Sử dụng thuốc trừ nấm, cắt bỏ lá bệnh và thu dọn vật thải sau mùa vụ'),
    'Apple___Black_rot': ('Bệnh thối đen trên táo', 'Sử dụng thuốc trừ nấm, cắt bỏ phần bị bệnh và kiểm soát tưới nước'),
    'Apple___Cedar_apple_rust': ('Bệnh sắt trên táo', 'Sử dụng thuốc trừ nấm đặc trị, cắt bỏ phần bị bệnh và loại bỏ cây chủ nhà khác'),
    'Apple___healthy': ('Táo khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Blueberry___healthy': ('Việt quất khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Cherry_(including_sour)___Powdery_mildew': ('Bệnh phấn trắng trên cherry', 'Sử dụng thuốc trừ nấm, tỉa cành và kiểm soát tưới nước'),
    'Cherry_(including_sour)___healthy': ('Cherry khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': ('Bệnh đốm lá xám trên ngô', 'Sử dụng giống kháng bệnh, luân canh cây trồng và thuốc trừ nấm'),
    'Corn_(maize)___Common_rust_': ('Bệnh sắt trên ngô', 'Sử dụng giống kháng bệnh, luân canh cây trồng và thuốc trừ nấm đặc trị'),
    'Corn_(maize)___Northern_Leaf_Blight': ('Bệnh đốm lá phần bắc trên ngô', 'Sử dụng giống kháng bệnh, luân canh cây trồng và thuốc trừ nấm'),
    'Corn_(maize)___healthy': ('Ngô khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Grape___Black_rot': ('Bệnh thối đen trên nho', 'Sử dụng thuốc trừ nấm, cắt bỏ phần bị bệnh và kiểm soát tưới nước'),
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': ('Bệnh đốm lá trên nho', 'Sử dụng thuốc trừ nấm, cắt bỏ lá bệnh và kiểm soát tưới nước'),
    'Grape___healthy': ('Nho khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Orange___Haunglongbing_(Citrus_greening)': ('Bệnh vàng lợt trên cam', 'Sử dụng giống kháng bệnh, cắt bỏ cành bệnh và kiểm soát véc-tơ truyền bệnh'),
    'Peach___Bacterial_spot': ('Bệnh đốm vi khuẩn trên đào', 'Sử dụng thuốc đồng và kháng sinh thực vật, cắt bỏ phần bệnh'),
    'Peach___healthy': ('Đào khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Pepper,_bell___Bacterial_spot': ('Bệnh đốm vi khuẩn trên ớt chuông', 'Sử dụng thuốc đồng và kháng sinh thực vật, cắt bỏ phần bệnh'),
    'Pepper,_bell___healthy': ('Ớt chuông khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Potato___Early_blight': ('Bệnh héo xì muộn trên khoai tây', 'Sử dụng thuốc trừ nấm, luân canh và dọn vệ sinh đồng ruộng'),
    'Potato___Late_blight': ('Bệnh héo xì sớm trên khoai tây', 'Sử dụng giống kháng bệnh, thuốc trừ nấm và kiểm soát tưới nước'),
    'Potato___healthy': ('Khoai tây khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Raspberry___healthy': ('Việt quất khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Soybean___healthy': ('Đậu tương khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Squash___Powdery_mildew': ('Bệnh phấn trắng trên bí ngô', 'Sử dụng thuốc trừ nấm, tỉa cành và kiểm soát tưới nước'),
    'Strawberry___Leaf_scorch': ('Bệnh cháy lá trên dâu tây', 'Sử dụng thuốc trừ nấm, vệ sinh đồng ruộng và kiểm soát tưới nước'),
    'Strawberry___healthy': ('Dâu tây khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    'Tomato___Bacterial_spot': ('Bệnh đốm vi khuẩn trên cà chua', 'Sử dụng thuốc đồng và kháng sinh thực vật, cắt bỏ phần bệnh'),
    'Tomato___Late_blight': ('Bệnh héo xì muộn trên cà chua', 'Sử dụng thuốc trừ nấm, luân canh và dọn vệ sinh đồng ruộng'),
	'Tomato___Leaf_Mold': ('Bệnh mốc lá trên cà chua', 'Sử dụng thuốc trừ nấm, tỉa cành và kiểm soát tưới nước'),
	'Tomato___Septoria_leaf_spot': ('Bệnh đốm lá Septoria trên cà chua', 'Sử dụng thuốc trừ nấm, cắt bỏ lá bệnh và thu dọn vật thải'),
	'Tomato___Spider_mites Two-spotted_spider_mite': ('Bệnh nhện đỏ hai chấm trên cà chua', 'Sử dụng thuốc trừ nhện, kiểm soát tưới nước và môi trường'),
	'Tomato___Target_Spot': ('Bệnh đốm đích trên cà chua', 'Sử dụng thuốc trừ nấm, cắt bỏ lá bệnh và luân canh cây trồng'),
	'Tomato___Tomato_Yellow_Leaf_Curl_Virus': ('Bệnh cuộn lá vàng virus trên cà chua', 'Sử dụng giống kháng virus, kiểm soát véc-tơ truyền bệnh và dọn vệ sinh đồng ruộng'),
	'Tomato___Tomato_mosaic_virus': ('Bệnh mô-saic virus trên cà chua', 'Sử dụng giống kháng virus, kiểm soát véc-tơ truyền bệnh và dọn vệ sinh đồng ruộng'),
	'Tomato___healthy': ('Cà chua khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh')
}

def image_detector():
    # CAMERA can be 0 or 1 based on default camera of your computer
    camera = cv2.VideoCapture(0)

    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class: ", class_name)
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    disease_name, treatment

    # Print disease information
    if class_name in disease_info:
        disease_name, treatment = disease_info[class_name]
        print(f"Loại bệnh: {disease_name}")
        print(f"Phương pháp chữa trị: {treatment}")
    else:
        print("Không có thông tin về loại bệnh này.")
        
    camera.release()
    cv2.destroyAllWindows()
    return disease_name + ": " + treatment

def open_file():
    file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    if file_path:
        return image_detector_demo(file_path)

def image_detector_demo(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Kiểm tra xem ảnh có được tải thành công hay không
    if image is None:
        print(f"Không thể tải ảnh từ đường dẫn: {image_path}")
        return

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class: ", class_name)
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    # Print disease information
    if class_name in disease_info:
        disease_name, treatment = disease_info[class_name]
        print(f"Loại bệnh: {disease_name}")
        print(f"Phương pháp chữa trị: {treatment}")
        result = f"Loại bệnh: {disease_name}\nPhương pháp chữa trị: {treatment}"
    else:
        print("Không có thông tin về loại bệnh này.")
        result = "Không có thông tin về loại bệnh này."

    return result

# # Tạo cửa sổ GUI
# root = tk.Tk()
# root.title("Nhận dạng bệnh cây trồng")

# # Tạo nút "Chọn ảnh"
# open_button = tk.Button(root, text="Chọn ảnh", command=open_file)
# open_button.pack(pady=10)

# # Chạy vòng lặp sự kiện của GUI
# root.mainloop()