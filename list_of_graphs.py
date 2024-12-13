import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker
import pandas as pd 
import numpy as np 
import os

def list_of_graphs(data_path, graph_dict, name):
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize = [10,5])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    ax.set_yscale('log')
    ax.set_xlim([-3,3])
    ax.set_ylim([10**(-10), 10**(-2)])
    ax.set_xlabel('Напряжение, В')
    ax.set_ylabel('Ток, А')

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
            ax.plot(df[0], np.abs(df[1]), c='#A9A9A9', linewidth = 1)
            a, b = df.loc[df[0] == 1][1]
            I_on.append(a)
            I_off.append(b)
            I_on_off.append(a/b)

        os.chdir(start_dir)

    I_on_mean = np.abs(np.mean(I_on))
    I_off_mean = np.abs(np.mean(I_off))
    I_on_off_mean = np.abs(np.mean(I_on_off))
    info_on_title = ''.join([r'$I_{on}^{mean} =$', f'{I_on_mean:.2e} A, ', r'$I_{off}^{mean} =$', f'{I_off_mean:.2e} A, ', r'mean $\frac{I_{on}}{I_{off}} =$', f'{I_on_off_mean:.2e}, '])

    ax.set_title(name+ ': ' + info_on_title)
    
    save_path = os.path.dirname(os.path.abspath(__file__)) + '\\' + name + '.png'
    plt.savefig(save_path, dpi = 300, bbox_inches = 'tight')