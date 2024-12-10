import cv2
import torch

def detect_cars_direction(image_path):
    # YOLOv5のnanoモデルをロード
    model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)

    # 画像をモデルに入力し、検知結果を取得
    results = model(image_path)

    # 検知結果から車（'car'クラス）のみをフィルタリング
    results = results.pandas().xyxy[0]  # 検知結果をpandas DataFrameで取得
    car_results = results[results['name'] == 'car']  # 'car'クラスの結果のみを抽出

    # 元の画像を読み込み
    image_cv = cv2.imread(image_path)
    height, width = image_cv.shape[:2]

    # 検知された車の中心座標を格納するリスト
    car_centers = []

    # 検知された車のバウンディングボックスを描画
    for index, row in car_results.iterrows():
        xmin = int(row['xmin'])
        ymin = int(row['ymin'])
        xmax = int(row['xmax'])
        ymax = int(row['ymax'])
        cv2.rectangle(image_cv, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        # 中心座標を計算
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        car_centers.append((center_x, center_y))

    # 保存先のパス
    save_path = 'static/detected_cars.jpg'

    # 画像の中心線を計算（画像の幅の半分）
    center_line_x = width / 2

    # 車が直線の右側または左側にあるかを判別するためのリスト
    cars_left = []
    cars_right = []

    # 各車の中心座標をチェックし、直線の左側または右側にあるかを判定
    for center in car_centers:
        if center[0] < center_line_x:
            cars_left.append(center)
        else:
            cars_right.append(center)

    # 結果を表示（オプション）
    print(f"左側にある車の数: {len(cars_left)}")
    print(f"右側にある車の数: {len(cars_right)}")

    # 斜めの線を引くための始点と終点を設定
    start_point = (int(center_line_x), 0)  # 左上の角
    end_point = (int(center_line_x), height - 1)  # 右下の角

    # 線の色を青で設定（B, G, R）
    line_color = (255, 0, 0)

    # 線の太さ
    line_thickness = 2

    # 画像に斜めの線を描画
    cv2.line(image_cv, start_point, end_point, line_color, line_thickness)

    # 画像の横幅を900にリサイズ
    new_width = 900
    aspect_ratio = new_width / width
    new_height = int(height * aspect_ratio)
    image_cv = cv2.resize(image_cv, (new_width, new_height))

    # 画像を保存
    cv2.imwrite(save_path, image_cv)

    # 検出された車の数と保存された画像のパスを返す
    return len(car_results), save_path, len(cars_left), len(cars_left)

if __name__ == '__main__':
    detect_cars_direction(fr'C:\Users\KM\Documents\Python Scripts\docker-pss\other\app\data\output\61.jpg')