import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker
import pandas as pd 
import numpy as np 
import os
import shutil

def get_colors_from_cmap(cmap_name: str, array_lenght: int) -> list:
    cmap = plt.get_cmap(cmap_name)
    individual_colors = [cmap(i / array_lenght) for i in range(array_lenght)]
    return individual_colors

def graph_DC_IV(data_path: str, save_path: str, name: str):
    df = pd.read_csv(data_path, delimiter='   ', skiprows=16, engine='python', header=None, encoding='ISO-8859-1').astype(np.float32)
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize = [10,5])
    colors = get_colors_from_cmap('plasma', len(df[0]))
    get_gradient_line(ax, V=df[0], I=df[1], colors = colors)
    ax.set_yscale('log')
    #ax.set_xlim([-5,5])
    #ax.set_ylim([10**(-8), 10**(-2)])
    #ax.set_title(f'{i} measurment with {lines[10].split()[1]} positive complines')
    ax.grid(which='major', linewidth = 0.6)
    ax.grid(which='minor', linewidth = 0.2)
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    #ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=0, vmax=len(df[0])))
    cbar = fig.colorbar(sm)
    cbar.set_ticks([0,len(df[0])])
    cbar.set_ticklabels(['start','end'])
    cbar.set_label('sequence of measurements', size = 15)
    plt.savefig(save_path + f'\\{name}.png', dpi = 300, bbox_inches = 'tight')
    plt.clf()
    plt.close(fig)

def create_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
        os.mkdir(path)
    else:
        os.mkdir(path)

def get_gradient_line(ax, V, I, colors):
    for i in range(len(V)-1):
        ax.plot([V[i], V[i+1]], np.abs([I[i], I[i+1]]), c = colors[i], linewidth = 2)

def all_graphs(data_path: str) :
    # чтение всех вложенных директорий и разделение на файлы и папки
    dir_list = []
    file_list = []
    for i in os.listdir(data_path):
        if os.path.isdir(f'{data_path}/{i}'):
            dir_list.append(f'{i}')
        else:
            file_list.append(f'{i}')

    # составляем список header файлов по имющимся папкам
    header_list = []
    for i in dir_list:
        if f'{i}.header' in file_list:
            header_list.append(f'{i}.header')

    # считываем данные об измерениях из header файлов
    splite_line = '______________________________________________________'
    all_contacts_info = {}
    for i in header_list:
        with open(f'{data_path}\{i}') as f:
            header_lines = []
            for k in f.readlines()[:-2]:
                header_lines.append(k.replace('\n', ''))
            # информация о всех отдельных измерениях на одном контакте
            single_contact_info = {}
            for j in range(len(header_lines)):
                if header_lines[j] == splite_line:
                    number, *m_type = header_lines[j + 3].split()
                    file_path = header_lines[j + 8].split()[-1]
                    single_contact_info[int(number)] = {'type': ' '.join(m_type), 'file_path': file_path}
                else:
                    continue
        all_contacts_info[i.replace('.header', '')] =  single_contact_info

    # рисуем графики для всех файлов во всех папках
    # создаем общую папку для графиков
    glodal_graph_path = '_'.join([data_path, 'graphs'])
    create_dir(glodal_graph_path)

    # создаем папки с графиками для каждого контакта и рисуем графики
    for i in range(len(dir_list)):
        single_contact_path = '\\'.join([data_path, dir_list[i]])
        local_graph_path = '\\'.join([glodal_graph_path, dir_list[i]])
        create_dir(local_graph_path)
        for j in os.listdir(single_contact_path):
            data_number = int(j.split('.')[0])
            local_data_path = f'{data_path}' + all_contacts_info[dir_list[i]][data_number]['file_path']
            match all_contacts_info[dir_list[i]][data_number]['type']:
                case 'DC IV':
                    graph_DC_IV(local_data_path, local_graph_path, str(data_number))


all_graphs('hBN_1_3')

