import pathlib
import pickle
import numpy as np
import sys
from PIL import Image
import matplotlib.pyplot as plt
import os
import os.path
from tqdm.notebook import tqdm
import shutil


#ファイルパス取得
def GetFilePath(path, search_word):
    file_path_list = []
    all_path = pathlib.Path(path)
    files = all_path.glob('**/*'+search_word)
    for file in files:
        file_path_list.append(str(file))
    file_path_list = sorted(file_path_list)
    return file_path_list


#numpyファイルとpklファイルを一致させる
def search_file(numpy_folder_path, pkl_folder_path):
    npy_path_list = GetFilePath(numpy_folder_path, '.npy')
    pkl_path_list = GetFilePath(pkl_folder_path, '.pkl')
    match_file_list = []
    for npy_file in tqdm(npy_path_list,desc='ファイルの検索'):
        for pkl_file in pkl_path_list:
            if npy_file.split('_')[-2].split('.')[0] == pkl_file.split('_')[-1].split('.')[0]:
                match_file_list.append([npy_file, pkl_file])
    return match_file_list
                

#pklからnumpyに変換
def pkl_numpy(file):
    with open(file, 'rb') as file:
        npy_file = pickle.load(file)
    return npy_file


#ファイル保存
def save_file(match_file, save_path, numpy_data):
    save = os.path.join(save_path, 'facebox_npy')
    os.makedirs(save, exist_ok=True)
    save = os.path.join(save, match_file[1].split(os.sep)[-1].split('.pkl')[0])
    np.save(save, numpy_data)


#顔特徴点を元に熱画像を切り抜く
def cut_npy(match_file_list, save_path, point, dif):
    for match_file in tqdm(match_file_list, desc='顔領域npyファイル生成'):
        facepoint_npy = np.load(match_file[0])
        picture_npy = pkl_numpy(match_file[1])
        
        #切り抜く座標
        xmin = int(facepoint_npy[ int(point[0][0]) ][0] + int(dif[0][0]) )
        xmax = int(facepoint_npy[ int(point[0][1]) ][0] + int(dif[0][1]) )
        ymin = int(facepoint_npy[ int(point[1][0]) ][1] + int(dif[1][0]) )
        ymax = int(facepoint_npy[ int(point[1][1]) ][1] + int(dif[1][1]) )

        face_box = picture_npy[ymin:ymax, xmin:xmax]
        save_file(match_file, save_path, face_box)


def main(numpy_folder_path, pkl_folder_path, save_path, point, dif):
    save = os.path.join(save_path, 'facebox_npy')
    if os.path.exists(save):
        shutil.rmtree(save)
    match_file_list = search_file(numpy_folder_path, pkl_folder_path)
    cut_npy(match_file_list, save_path, point, dif)
    return os.path.join(save_path, 'facebox_npy')

