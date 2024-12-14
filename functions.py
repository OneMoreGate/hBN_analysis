import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 
import os
import shutil

def draw_list_of_data(ax, data_path, graph_dict):

    start_dir = os.path.dirname(os.path.abspath(__file__)) + '\\' + data_path
    os.chdir(start_dir)
    for i in graph_dict.keys():
        os.chdir(start_dir + '\\' + i + '\\')
        for j in graph_dict[i]:
            graph_data_path = start_dir + '\\' + i + '\\' + str(j) + '.data'
            df = pd.read_csv(graph_data_path, delimiter='   ', skiprows=16, engine='python', header=None, encoding='ISO-8859-1').astype(np.float32)
            ax.plot(df[0], np.abs(df[1]), c='#A9A9A9', linewidth = 1)
        os.chdir(start_dir)

def read_on_off_stat(data_path, graph_dict, check_voltage: float):
    I_on_off = []
    I_on = []
    I_off = []

    start_dir = os.path.dirname(os.path.abspath(__file__)) + '\\' + data_path
    os.chdir(start_dir)
    for i in graph_dict.keys():
        os.chdir(start_dir + '\\' + i + '\\')
        for j in graph_dict[i]:
            graph_data_path = start_dir + '\\' + i + '\\' + str(j) + '.data'
            df = pd.read_csv(graph_data_path, delimiter='   ', skiprows=16, engine='python', header=None, encoding='ISO-8859-1').astype(np.float32)
            a, b = df.loc[df[0] == check_voltage][1]
            I_on.append(a)
            I_off.append(b)
            I_on_off.append(a/b)
        os.chdir(start_dir)

    return {'I_on': np.array(I_on), 'I_off': np.array(I_off), 'I_on_off': np.array(I_on_off)}

def hex_to_RGB(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(1,6,2)]

def draw_color_gradient(c1, c2, axes):
    lines = axes.get_lines()
    n = len(lines)
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1))/255
    c2_rgb = np.array(hex_to_RGB(c2))/255
    mix_pcts = [x/(n-1) for x in range(n)]
    rgb_colors = [((1-mix)*c1_rgb + (mix*c2_rgb)) for mix in mix_pcts]
    colors = ["#" + "".join([format(int(round(val*255)), "02x") for val in item]) for item in rgb_colors]
    for i in range(n):
        lines[i].set_color(colors[i])

def draw_one_color(color, lines):
    n = len(lines)
    for i in range(n):
        lines[i].set_color(color)