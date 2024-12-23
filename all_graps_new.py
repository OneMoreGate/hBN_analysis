import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import os
import shutil

# создание и удаление директорий  
def create_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
        os.mkdir(path)
    else:
        os.mkdir(path)

# нахождение всех вложенных директорий
def find_directories(data_folder: str) -> list:
    dir_list = []
    for i in os.listdir(data_folder):
        if os.path.isdir(f'{data_folder}/{i}'):
            dir_list.append(f'{i}')
    return dir_list

# нахождение всех файлов в директориях
def find_files(data_folder: str, dir_list: list) -> dict:
    dir_and_files_dict = {}
    for i in dir_list:
        onlyfiles = [int(f.replace('.data','')) for f in os.listdir(os.path.abspath(data_folder + '\\' +  i)) if os.path.isfile(os.path.join(data_folder +'\\' +   i, f))]
        dir_and_files_dict[i] = onlyfiles
    return dir_and_files_dict

def get_colors_from_cmap(cmap_name: str, array_lenght: int) -> list:
    cmap = plt.get_cmap(cmap_name)
    individual_colors = [cmap(i / array_lenght) for i in range(array_lenght)]
    return individual_colors

# получение данных с указанных фалов и директорий
def get_data_from_dict(data_folder: str, dict_of_data: dict) -> dict:
    start_dir = os.path.abspath(data_folder)
    folders = list(dict_of_data.keys())
    output_data_dict = {}
    for i in folders:
        output_data_dict[i] = {}
        if isinstance(dict_of_data[i], list):
            data_list_from_folder = dict_of_data[i]
        elif isinstance(dict_of_data[i], int):
            data_list_from_folder = [dict_of_data[i]]
        for j in data_list_from_folder:
            single_data_path = start_dir + '\\' + i + '\\' + str(j) + '.data'
            single_df = pd.read_csv(single_data_path, delimiter='   ', skiprows=16, engine='python', header=None, encoding='ISO-8859-1').astype(np.float32)
            single_df.rename(columns = {0: 'voltage', 1: 'current', 2: 'resistance'}, inplace=True)
            output_data_dict[i][j] = single_df
    return output_data_dict

def draw_gradient_line(ax, V, I, colors):
    for i in range(len(V)-1):
        ax.plot([V[i], V[i+1]], np.abs([I[i], I[i+1]]), c = colors[i], linewidth = 2)


def draw_all_graphs(data_folder: str):
    dir_list = find_directories(data_folder)
    dirs_and_files = find_files(data_folder, dir_list)
    global_graph_folder = '_'.join([data_folder, 'graphs'])
    create_dir(global_graph_folder)
    all_data = get_data_from_dict(data_folder, dirs_and_files)
    for i in list((all_data.keys())):
        local_graph_folder = '\\'.join([global_graph_folder, i]) 
        create_dir(local_graph_folder)
        for j in list(all_data[i].keys()):
                fig, ax = plt.subplots(figsize = [10,5])
                I = np.array(all_data[i][j]['current'])
                V = np.array(all_data[i][j]['voltage'])
                print([i, j])
                colors = get_colors_from_cmap('plasma', len(V))
                draw_gradient_line(ax, V, I, colors)
                ax.set_yscale('log')
                ax.grid(which='major', linewidth = 0.6)
                ax.grid(which='minor', linewidth = 0.2)
                sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=0, vmax=len(V)))
                cbar = fig.colorbar(sm)
                cbar.set_ticks([0,len(V)])
                cbar.set_ticklabels(['start','end'])
                cbar.set_label('sequence of measurements', size = 15)
                plt.savefig(local_graph_folder + '\\' + str(j) + '.png', bbox_inches = 'tight', dpi = 300)
                plt.clf()
                plt.close(fig)

draw_all_graphs('hBN_1_2')
draw_all_graphs('hBN_1_3')