import cv2
import torch

def detect_cars_and_save(image_path):
    # YOLOv5のnanoモデルをロード
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

    # 画像をモデルに入力し、検知結果を取得
    results = model(image_path)

    # 検知結果から車（'car'クラス）のみをフィルタリング
    results = results.pandas().xyxy[0]  # 検知結果をpandas DataFrameで取得
    car_results = results[results['name'] == 'car']  # 'car'クラスの結果のみを抽出

    # 元の画像を読み込み
    image_cv = cv2.imread(image_path)


    # 検知された車のバウンディングボックスを描画
    for index, row in car_results.iterrows():
        xmin = int(row['xmin'])
        ymin = int(row['ymin'])
        xmax = int(row['xmax'])
        ymax = int(row['ymax'])
        cv2.rectangle(image_cv, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)


    # 結果を保存
    save_path = 'static/detected_cars.jpg'

    # 画像の横幅を900にリサイズ
    height, width = image_cv.shape[:2]
    new_width = 900
    aspect_ratio = new_width / width
    new_height = int(height * aspect_ratio)
    image_cv = cv2.resize(image_cv, (new_width, new_height))

    cv2.imwrite(save_path, image_cv)

    # 検出された車の数と保存された画像のパスを返す
    return len(car_results), save_path, results