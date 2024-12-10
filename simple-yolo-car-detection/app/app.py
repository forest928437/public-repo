import os
import shutil

from flask import Flask, request, redirect, render_template, url_for, flash

import src.check_car_num as ccn

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションの秘密鍵を設定

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/delete_static', methods=['POST'])
def delete_static():
    folder = 'static'
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        flash('staticフォルダの内容が削除されました。')  # ポップアップメッセージを追加
        return redirect(url_for('index'))
    else:
        return 'staticフォルダが存在しません。', 404

@app.route('/upload_image', methods=['POST'])
def upload_image():
    image_file = request.files['image_file']
    if image_file:
        # 一時ファイルとして保存
        filepath = 'static/' + image_file.filename
        image_file.save(filepath)

        # 車の検知を実行
        car_num, result_path, result_df = ccn.detect_cars_and_save(filepath)

        # データフレームをHTMLに変換
        result_df_html = result_df.to_html()

        # 結果をテンプレートに渡して表示
        print(result_path)
        return render_template('result.html', car_num=car_num, image_path=result_path, result_df_html=result_df_html)
    else:
        return 'ファイルがアップロードされていません。'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)