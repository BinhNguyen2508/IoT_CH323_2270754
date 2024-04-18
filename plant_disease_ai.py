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
    class_indices = json.load(f)
    class_names = list(class_indices.values())

# Định nghĩa thông tin về loại bệnh và phương pháp chữa trị
disease_info = {
    class_names[0]: ('Bệnh đạo ôn trên táo', 'Sử dụng thuốc trừ nấm, cắt bỏ lá bệnh và thu dọn vật thải sau mùa vụ'),
    class_names[1]: ('Bệnh thối đen trên táo', 'Sử dụng thuốc trừ nấm, cắt bỏ phần bị bệnh và kiểm soát tưới nước'),
    class_names[2]: ('Bệnh sắt trên táo', 'Sử dụng thuốc trừ nấm đặc trị, cắt bỏ phần bị bệnh và loại bỏ cây chủ nhà khác'),
    class_names[3]: ('Táo khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[4]: ('Việt quất khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[5]: ('Bệnh phấn trắng trên cherry', 'Sử dụng thuốc trừ nấm, tỉa cành và kiểm soát tưới nước'),
    class_names[6]: ('Cherry khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[7]: ('Bệnh đốm lá xám trên ngô', 'Sử dụng giống kháng bệnh, luân canh cây trồng và thuốc trừ nấm'),
    class_names[8]: ('Bệnh sắt trên ngô', 'Sử dụng giống kháng bệnh, luân canh cây trồng và thuốc trừ nấm đặc trị'),
    class_names[9]: ('Bệnh đốm lá phần bắc trên ngô', 'Sử dụng giống kháng bệnh, luân canh cây trồng và thuốc trừ nấm'),
    class_names[10]: ('Ngô khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[11]: ('Bệnh thối đen trên nho', 'Sử dụng thuốc trừ nấm, cắt bỏ phần bị bệnh và kiểm soát tưới nước'),
    class_names[12]: ('Bệnh đen đỗ trên nho', 'Sử dụng thuốc trừ nấm, cắt bỏ phần bị bệnh và kiểm soát tưới nước'),
    class_names[13]: ('Bệnh đốm lá trên nho', 'Sử dụng thuốc trừ nấm, cắt bỏ lá bệnh và kiểm soát tưới nước'),
    class_names[14]: ('Nho khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[15]: ('Bệnh vàng lợt trên cam', 'Sử dụng giống kháng bệnh, cắt bỏ cành bệnh và kiểm soát véc-tơ truyền bệnh'),
    class_names[16]: ('Bệnh đốm vi khuẩn trên đào', 'Sử dụng thuốc đồng và kháng sinh thực vật, cắt bỏ phần bệnh'),
    class_names[17]: ('Đào khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[18]: ('Bệnh đốm vi khuẩn trên ớt chuông', 'Sử dụng thuốc đồng và kháng sinh thực vật, cắt bỏ phần bệnh'),
    class_names[19]: ('Ớt chuông khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[20]: ('Bệnh héo xì muộn trên khoai tây', 'Sử dụng thuốc trừ nấm, luân canh và dọn vệ sinh đồng ruộng'),
    class_names[21]: ('Bệnh héo xì sớm trên khoai tây', 'Sử dụng giống kháng bệnh, thuốc trừ nấm và kiểm soát tưới nước'),
    class_names[22]: ('Khoai tây khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[23]: ('Việt quất khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[24]: ('Đậu tương khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[25]: ('Bệnh phấn trắng trên bí ngô', 'Sử dụng thuốc trừ nấm, tỉa cành và kiểm soát tưới nước'),
    class_names[26]: ('Bệnh cháy lá trên dâu tây', 'Sử dụng thuốc trừ nấm, vệ sinh đồng ruộng và kiểm soát tưới nước'),
    class_names[27]: ('Dâu tây khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh'),
    class_names[28]: ('Bệnh đốm vi khuẩn trên cà chua', 'Sử dụng thuốc đồng và kháng sinh thực vật, cắt bỏ phần bệnh'),
    class_names[29]: ('Bệnh héo xì sớm trên cà chua', 'Sử dụng thuốc trừ nấm, luân canh và don vệ sinh đồng ruộng'),
    class_names[30]: ('Bệnh héo xì muộn trên cà chua', 'Sử dụng thuốc trừ nấm, luân canh và dọn vệ sinh đồng ruộng'),
    class_names[31]: ('Bệnh mốc lá trên cà chua', 'Sử dụng thuốc trừ nấm, tỉa cành và kiểm soát tưới nước'),
    class_names[32]: ('Bệnh đốm lá Septoria trên cà chua', 'Sử dụng thuốc trừ nấm, cắt bỏ lá bệnh và thu dọn vật thải'),
    class_names[33]: ('Bệnh nhện đỏ hai chấm trên cà chua', 'Sử dụng thuốc trừ nhện, kiểm soát tưới nước và môi trường'),
    class_names[34]: ('Bệnh đốm đích trên cà chua', 'Sử dụng thuốc trừ nấm, cắt bỏ lá bệnh và luân canh cây trồng'),
    class_names[35]: ('Bệnh cuộn lá vàng virus trên cà chua', 'Sử dụng giống kháng virus, kiểm soát véc-tơ truyền bệnh và dọn vệ sinh đồng ruộng'),
    class_names[36]: ('Bệnh mô-saic virus trên cà chua', 'Sử dụng giống kháng virus, kiểm soát véc-tơ truyền bệnh và dọn vệ sinh đồng ruộng'),
    class_names[37]: ('Cà chua khỏe mạnh', 'Duy trì chăm sóc và phòng ngừa bệnh')
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
        result = f"Loại bệnh: {disease_name}\n Phương pháp chữa trị: {treatment}"
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