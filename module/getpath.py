import glob
import os
import pathlib

#ファイルパス取得
def GetFilePath(path,name):
    file_path_list = []
    all_path = pathlib.Path(path)
    files = all_path.glob('**/*'+name+'*')
    for file in files:
        file_path_list.append(str(file))
    file_path_list = sorted(file_path_list)
    return file_path_list


def get_time(path):
    f = os.path.basename(path).split('.')[0].split('_')[1]
    time = f[:2]+':'+f[2:4]+':'+f[4:]
    return time


def get_errortime(path):
    with open(path) as f:
        error_time = f.read()
    if '-' in error_time:
        error_time = error_time.replace('-','')
        error_time = -1 * int(error_time)
    else:
        error_time = int(error_time)
    return error_time


class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'


def main(path):
    print('\n')
    try:
        elapsed_file = GetFilePath(path,'elapsed')[0]
        print('elapsed_file  ： '+os.path.basename(elapsed_file))
    except:
        elapsed_file = 'elapsed_file  ：見つかりませんでした'
        print(pycolor.RED+elapsed_file+pycolor.END)
    try:
        Thermal_file = GetFilePath(path,'Thermal')[0]
        print('Thermal_file  ： '+os.path.basename(Thermal_file))
    except:
        Thermal_file = 'Thermal_file  ：見つかりませんでした'
        print(pycolor.RED+Thermal_file+pycolor.END)
    try:
        seq_file = GetFilePath(path,'.seq')[0]
        seq_time = get_time(seq_file)
        print('seq_time      ： '+seq_time)
    except:
        seq_time = 'seq_file      ： 見つかりませんでした'
        print(pycolor.RED+seq_time+pycolor.END)
    try:
        facebox_file = GetFilePath(path,'facebox_npy')[0]
        print('facebox_file  ： '+os.path.basename(facebox_file))
    except:
        facebox_file = 'facebox_file  ： 見つかりませんでした'
        print(pycolor.RED+facebox_file+pycolor.END)
    try:
        video_file = GetFilePath(path,'CA*.mp4')[0]
        video_time = get_time(video_file)
        print('video_time    ： '+video_time)
    except:
        video_time = 'video_path    ： 見つかりませんでした'
        print(pycolor.RED+video_time+pycolor.END)
    try:
        facepoint_file = GetFilePath(path,'facepoint_npy')[0]
        print('facepoint_file： '+os.path.basename(facepoint_file))
    except:
        facepoint_file = 'facepoint_file： 見つかりませんでした'
        print(pycolor.RED+facepoint_file+pycolor.END)
    try:
        pkl_file = GetFilePath(path,'convert_pkl')[0]
        print('pkl_file      ： '+os.path.basename(pkl_file))
    except:
        pkl_file = 'pkl_file      ： 見つかりませんでした'
        print(pycolor.RED+pkl_file+pycolor.END)
    try:
        nedo_file = GetFilePath(path, 'NEDO*.csv')[0]
        print('nedo_file     ： '+os.path.basename(nedo_file))
    except:
        nedo_file = 'nedo_file     ： 見つかりませんでした'
        print(pycolor.RED+nedo_file+pycolor.END)
    try:
        errortime_file = GetFilePath(path, 'error_time.txt')[0]
        error_time = get_errortime(errortime_file)
        print('error_time    ： '+str(error_time))
    except:
        error_time = 'error_time    ： 見つかりませんでした'
        print(pycolor.RED+error_time+pycolor.END)
    return elapsed_file, Thermal_file, seq_time, facebox_file, video_time, facepoint_file, pkl_file, nedo_file, error_time