import glob
import cv2
import os
import datetime
import pathlib
from tqdm.notebook import tqdm
from matplotlib import pyplot as plt
import numpy as np
import csv
import glob
import shutil
import pandas as pd
import itertools


#ファイルパス取得
def GetFilePath(path):
    file_path_list = []
    all_path = pathlib.Path(path)
    files = all_path.glob('**/*facepoint.png')
    for file in files:
        file_path_list.append(str(file))
    file_path_list = sorted(file_path_list)
    return file_path_list


#サーモと実験開始時間の差分　(サーモ　ー　実験開始)
def time_diference(elapsed_time_path,thermo_start_time):
    elapse_start = elapsed_time_path.split('_')[-1][8:14]
    hour = int(thermo_start_time.split(':')[0]) - int(elapse_start[:2])
    minute = int(thermo_start_time.split(':')[1]) - int(elapse_start[2:4])
    second = int(thermo_start_time.split(':')[2]) - int(elapse_start[4:])
    time_diferent = -1*(hour*60*60 + minute*60 + second)
    return time_diferent


def file_sort(elapsed_time_path, time_diferent, file_path_list):

    #elapsed_timeから経過時間を取得
    elapsed_time = pd.read_csv(elapsed_time_path, index_col=0)
    T1_suppression = round(elapsed_time.loc['T1_suppression'])
    T2_suppression = round(elapsed_time.loc['T2_suppression'])
    T3_suppression = round(elapsed_time.loc['T3_suppression'])
    T1_suppression_start = int(T1_suppression['start_time']) + time_diferent
    T1_suppression_end = int(T1_suppression['end_time']) + time_diferent
    T2_suppression_start = int(T2_suppression['start_time']) + time_diferent
    T2_suppression_end = int(T2_suppression['end_time']) + time_diferent
    T3_suppression_start = int(T3_suppression['start_time']) + time_diferent
    T3_suppression_end = int(T3_suppression['end_time']) + time_diferent
    T1_sleep = round(elapsed_time.loc['T1_sleep'])
    T2_sleep = round(elapsed_time.loc['T2_sleep'])
    T3_sleep = round(elapsed_time.loc['T3_sleep'])
    T1_sleep_start = int(T1_sleep['start_time']) + time_diferent
    T1_sleep_end = int(T1_sleep['end_time']) + time_diferent
    T2_sleep_start = int(T2_sleep['start_time']) + time_diferent
    T2_sleep_end = int(T2_sleep['end_time']) + time_diferent
    T3_sleep_start = int(T3_sleep['start_time']) + time_diferent
    T3_sleep_end = int(T3_sleep['end_time']) + time_diferent

    evaluation_file = []
    for file_path in file_path_list:
        time = int(file_path.split('_')[-2])

        if T1_suppression_start <= time <= T1_suppression_end:
            evaluation_file.append([file_path, 'T1_suppression'])

        elif T2_suppression_start <= time <= T2_suppression_end:
            evaluation_file.append([file_path, 'T2_suppression'])
        
        elif T3_suppression_start <= time <= T3_suppression_end:
            evaluation_file.append([file_path, 'T3_suppression'])
            
        elif T1_sleep_start <= time <= T1_sleep_end:
            evaluation_file.append([file_path, 'T1_sleep'])
            
        elif T2_sleep_start <= time <= T2_sleep_end:
            evaluation_file.append([file_path, 'T2_sleep'])

        elif T3_sleep_start <= time <= T3_sleep_end:
            evaluation_file.append([file_path, 'T3_sleep'])

    return evaluation_file



def maina(file_path, thermo_start_time, elapsed_time_path):
    file_path_list = GetFilePath(file_path)
    time_diferent = time_diference(elapsed_time_path,thermo_start_time)
    evaluation_file = file_sort(elapsed_time_path, time_diferent, file_path_list)
    return evaluation_file




def image_to_video(npy_path, save_path):

    def add_title(file,img):
        sentence1 = file[1]
        sentence2 = os.path.basename(file[0])
        cv2.putText(img, sentence1, (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, sentence2, (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1, cv2.LINE_AA)
        return img

    img_array = []
    for filename in tqdm(npy_path, desc='画像の読み込み'):
        img = cv2.imread(filename[0])
        img = add_title(filename, img)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)
    
    image_file_name = '解析データ/check_facepoint.mp4'
    save_path = os.path.join(save_path, image_file_name)
    if os.path.exists(save_path):
        os.remove(save_path)
    out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'MP4V'), 5.0, size)

    for i in tqdm(range(len(img_array)), desc='動画の書き出し'):
        out.write(img_array[i])
    out.release()


def main(png_path,thermo_start_time, elapsed_time_path,save_path):
    png_path = maina(png_path,thermo_start_time, elapsed_time_path)
    image_to_video(png_path, save_path)