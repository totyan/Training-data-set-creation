import csv
import os
import glob
import shutil
import pandas as pd
import itertools
from itertools import groupby
from tqdm.notebook import tqdm
import sys
import pathlib
import openpyxl



#nedoリストの作成
def make_nedo(elapsed_time_path,nedo_file_path,movie_start_time,error_time):
    #顔表情と実験開始時間の差分（顔表情　ー　実験開始）
    elapse_start = elapsed_time_path.split('_')[-1][8:14]
    hour = int(movie_start_time.split(':')[0]) - int(elapse_start[:2])
    minute = int(movie_start_time.split(':')[1]) - int(elapse_start[2:4])
    second = int(movie_start_time.split(':')[2]) - int(elapse_start[4:])
    time_diferent = -1*(hour*60*60 + minute*60 + second)-error_time

    #NEDO評価csvの読み込み
    with open(nedo_file_path) as f:
        reader = csv.reader(f)
        list_nedo = [row for row in reader]
    list_nedo = list_nedo[1:]

    #1秒ずつのリストに変換
    new_nedo = []
    for nedo in range(len(list_nedo)):
        if list_nedo[nedo][1] == '0':
            pass
        else:
            hour = int(list_nedo[nedo][0].split(':')[0]) 
            minute = int(list_nedo[nedo][0].split(':')[1])
            second = int(list_nedo[nedo][0].split(':')[2])
            time = hour*60*60 +minute*60 + second
            for t in range(1,21):
                times = (time - 20) + t
                new_nedo.append([times-time_diferent,list_nedo[nedo][1]])
                #print(times-time_diferent_a,list_nedo[nedo][1])
    return new_nedo
    

#pklファイルの振り分け
def sep_file(new_nedo,elapsed_time_path , thermo_start_time, save_path, error_time, sort_destination_folder_path, npy_folder_path):
    if os.path.exists(sort_destination_folder_path+os.sep+'dataset'):
        shutil.rmtree(sort_destination_folder_path+os.sep+'dataset')
    
    sort_destination_folder_path = os.path.join(sort_destination_folder_path, 'dataset')

    #眠気レベル別のフォルダの作成
    #T1
    T1_level_1_path = sort_destination_folder_path + '/cnn_train_data/T1/1'
    T1_level_2_path = sort_destination_folder_path + '/cnn_train_data/T1/2'
    T1_level_3_path = sort_destination_folder_path + '/cnn_train_data/T1/3'
    T1_level_4_path = sort_destination_folder_path + '/cnn_train_data/T1/4'
    T1_level_5_path = sort_destination_folder_path + '/cnn_train_data/T1/5'
    T1_level_6_path = sort_destination_folder_path + '/cnn_train_data/T1/6'
    T1_path_list = [T1_level_1_path, T1_level_2_path, T1_level_3_path, T1_level_4_path, T1_level_5_path, T1_level_6_path]
    os.makedirs(T1_level_1_path)
    os.makedirs(T1_level_2_path)
    os.makedirs(T1_level_3_path)
    os.makedirs(T1_level_4_path)
    os.makedirs(T1_level_5_path)
    os.makedirs(T1_level_6_path)
    #T2
    T2_level_1_path = sort_destination_folder_path + '/cnn_train_data/T2/1'
    T2_level_2_path = sort_destination_folder_path + '/cnn_train_data/T2/2'
    T2_level_3_path = sort_destination_folder_path + '/cnn_train_data/T2/3'
    T2_level_4_path = sort_destination_folder_path + '/cnn_train_data/T2/4'
    T2_level_5_path = sort_destination_folder_path + '/cnn_train_data/T2/5'
    T2_level_6_path = sort_destination_folder_path + '/cnn_train_data/T2/6'
    T2_path_list = [T2_level_1_path, T2_level_2_path, T2_level_3_path, T2_level_4_path, T2_level_5_path, T2_level_6_path]
    os.makedirs(T2_level_1_path)
    os.makedirs(T2_level_2_path)
    os.makedirs(T2_level_3_path)
    os.makedirs(T2_level_4_path)
    os.makedirs(T2_level_5_path)
    os.makedirs(T2_level_6_path)
    #T3
    T3_level_1_path = sort_destination_folder_path + '/cnn_train_data/T3/1'
    T3_level_2_path = sort_destination_folder_path + '/cnn_train_data/T3/2'
    T3_level_3_path = sort_destination_folder_path + '/cnn_train_data/T3/3'
    T3_level_4_path = sort_destination_folder_path + '/cnn_train_data/T3/4'
    T3_level_5_path = sort_destination_folder_path + '/cnn_train_data/T3/5'
    T3_level_6_path = sort_destination_folder_path + '/cnn_train_data/T3/6'
    T3_path_list = [T3_level_1_path, T3_level_2_path, T3_level_3_path, T3_level_4_path, T3_level_5_path, T3_level_6_path]
    os.makedirs(T3_level_1_path)
    os.makedirs(T3_level_2_path)
    os.makedirs(T3_level_3_path)
    os.makedirs(T3_level_4_path)
    os.makedirs(T3_level_5_path)
    os.makedirs(T3_level_6_path)

    #サーモと実験開始時間の差分　(サーモ　ー　実験開始)
    elapse_start = elapsed_time_path.split('_')[-1][8:14]
    hour = int(thermo_start_time.split(':')[0]) - int(elapse_start[:2])
    minute = int(thermo_start_time.split(':')[1]) - int(elapse_start[2:4])
    second = int(thermo_start_time.split(':')[2]) - int(elapse_start[4:])
    time_diferent = -1*(hour*60*60 + minute*60 + second)-error_time

    #elapsed_timeから経過時間を取得
    elapsed_time = pd.read_csv(elapsed_time_path, index_col=0)
    T1_suppression = round(elapsed_time.loc['T1_suppression'])
    T2_suppression = round(elapsed_time.loc['T2_suppression'])
    T3_suppression = round(elapsed_time.loc['T3_suppression'])
    T1_sleep = round(elapsed_time.loc['T1_sleep'])
    T2_sleep = round(elapsed_time.loc['T2_sleep'])
    T3_sleep = round(elapsed_time.loc['T3_sleep'])
    T1_sup_start = int(T1_suppression['start_time']) + time_diferent
    T1_sup_end = int(T1_suppression['end_time']) + time_diferent
    T2_sup_start = int(T2_suppression['start_time']) + time_diferent
    T2_sup_end = int(T2_suppression['end_time']) + time_diferent
    T3_sup_start = int(T3_suppression['start_time']) + time_diferent
    T3_sup_end = int(T3_suppression['end_time']) + time_diferent
    T1_sleep_start = int(T1_sleep['start_time']) + time_diferent
    T1_sleep_end = int(T1_sleep['end_time']) + time_diferent
    T2_sleep_start = int(T2_sleep['start_time']) + time_diferent
    T2_sleep_end = int(T2_sleep['end_time']) + time_diferent
    T3_sleep_start = int(T3_sleep['start_time']) + time_diferent
    T3_sleep_end = int(T3_sleep['end_time']) + time_diferent

    #振り分け（眠気誘発区間）
    for nedo in tqdm(new_nedo,desc='npyファイル振り分け'):

        def sep_nedo(start,end,save_path):
            if start <= nedo[0]+time_diferent <= end:
                try:
                    if nedo[1] == '1':
                        shutil.copy2(npy_folder_path + '/' + search_word, save_path[0] + '/' + search_word)
                    elif nedo[1] == '2':
                        shutil.copy2(npy_folder_path + '/' + search_word, save_path[1] + '/' + search_word)
                    elif nedo[1] == '3':
                        shutil.copy2(npy_folder_path + '/' + search_word, save_path[2] + '/' + search_word)
                    elif nedo[1] == '4':
                        shutil.copy2(npy_folder_path + '/' + search_word, save_path[3] + '/' + search_word)
                    elif nedo[1] == '5':
                        shutil.copy2(npy_folder_path + '/' + search_word, save_path[4] + '/' + search_word)
                except:
                    print('facebox_npyになかったファイル：'+str(search_word))

        count = 10 - len(str(int(nedo[0])+time_diferent) + '.npy')
        search_word = 'frame_' +'0'*count + str(int(nedo[0])+time_diferent) + '.npy'

        #T1_sleep
        sep_nedo(T1_sleep_start,T1_sleep_end,T1_path_list)
        #T2_sleep
        sep_nedo(T2_sleep_start,T2_sleep_end,T2_path_list)
        #T3_sleep
        sep_nedo(T3_sleep_start,T3_sleep_end,T3_path_list)

    def sep_sup(start,end,save_path):
        for i in range(start, end+1):
            try:
                count = 10 - len(str(i) + '.npy')
                word = 'frame_' + '0'*count + str(i) + '.npy'
                shutil.copy2(npy_folder_path + '/' + word, save_path + '/' + word)
            except:
                print(word)

    #T1_sup
    sep_sup(T1_sup_start, T1_sup_end, T1_level_6_path)
    #T2_sup
    sep_sup(T2_sup_start, T2_sup_end, T2_level_6_path)
    #T3_sup
    sep_sup(T3_sup_start, T3_sup_end, T3_level_6_path)

    return sort_destination_folder_path


#データセットのデータ数のカウント（輪講資料用）
def count(path):

    #フォルダパス取得
    def GetFilePath(path):
        file_path_list = []
        all_path = pathlib.Path(path)
        files = all_path.glob('**/*.npy')
        for file in files:
            f = str(file).rsplit(os.sep,1)[0]
            file_path_list.append(str(f))
        file_path_list = sorted(set(file_path_list))
        file_path_list = [list(g) for _, g in groupby(file_path_list, lambda x: x.rsplit(os.sep,1)[0])]
        return file_path_list

    def data_count(path, or_path):
        data_list = ['Level']
        for p in path:
            data_list.append(p[0].split(os.sep)[-2])
        data_list = [data_list]
        data_list.append([1,0,0,0])
        data_list.append([2,0,0,0])
        data_list.append([3,0,0,0])
        data_list.append([4,0,0,0])
        data_list.append([5,0,0,0])
        data_list.append([6,0,0,0])
        i = 1
        for p in path:
            for u in p:
                f_count = len(os.listdir(u))
                level = int(u.rsplit(os.sep,1)[-1])
                data_list[level][i] = f_count
            i += 1
        return data_list

    def make_excel(data_info, path):
        book = openpyxl.Workbook()
        ex_path = os.path.join(path, 'dataset_info.xlsx')
        sheet = book.active
        sheet.title = 'cnn_train_data'
        row = 1
        column = 1
        for data in data_info:
            for d in data:
                sheet.cell(row=row, column=column).value = d
                column += 1
            row += 1
            column = 1
        book.save(ex_path)

    all_data = os.path.join(path, 'cnn_train_data')
    all_path = GetFilePath(all_data)
    data_list = data_count(all_path, path)
    make_excel(data_list, path)


def main(seq_start,video_start,elapsed_time_path,nedo_file_path,sort_destination_folder_path,npy_folder_path,error_time,save_path):
    new_nedo = make_nedo(elapsed_time_path, nedo_file_path,video_start, error_time)
    data_path = sep_file(new_nedo, elapsed_time_path, seq_start, save_path, error_time, sort_destination_folder_path, npy_folder_path)
    count(data_path)