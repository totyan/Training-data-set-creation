import glob
import cv2
import os
import datetime
import pathlib
from tqdm.notebook import tqdm
from matplotlib import pyplot as plt
import numpy as np
import requests


def image_to_video(npy_path, save_path):

    #ファイルパス取得
    def GetFilePath(path,name):
        file_path_list = []
        all_path = pathlib.Path(path)
        files = all_path.glob('**/*'+name)
        for file in files:
            file_path_list.append(str(file))
        file_path_list = sorted(file_path_list)
        return file_path_list

    #ファイルパス取得
    def sort(path):
        file_path_list = []
        path_list = []
        for file in path:
            file_path_list.append(os.path.basename(file))
        file_path_list = sorted(file_path_list)
        for f in file_path_list:
            ans = [x for x in path if f in x]
            path_list.append(ans[0])
        return path_list

    def add_title(file,img):
        sentence1 = file.rsplit(os.sep)[0]
        sentence2 = os.path.basename(file)
        cv2.putText(img, sentence1, (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, sentence2, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
        return img

    img_array = []
    files = GetFilePath(npy_path,'.npy')
    files = sort(files)

    for filename in tqdm(files,desc='npyファイルの読み込み'):
        #画像データ1枚を出力するコード
        plt.figure(dpi=160) 
        plt.axis("off")
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.imshow(np.load(filename))
        plt.savefig('a.png')
        plt.close()
        img = cv2.imread('a.png')
        img = add_title(filename, img)
        img_array.append(img)
    height, width, layer = img.shape
    size = (width, height)
    os.remove('a.png')
    
    
    image_file_name = save_path+'/check_dataset.mp4'
    save_path = os.path.join(save_path, image_file_name)
    if os.path.exists(save_path):
        os.remove(save_path)
    out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'MP4V'), 5.0, size)

    for i in tqdm(range(len(img_array)),desc='動画の書き出し'):
        out.write(img_array[i])
    out.release()


def line_send(message):
    url = "https://notify-api.line.me/api/notify"
    access_token = 'access_token'
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {'message': message}
    requests.post(url, headers=headers, params=payload,)


def main(npy_path, save_path):
    image_to_video(npy_path, save_path)
    line_send('\nデータセット確認動画の出力完了')