# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby

"""
Plotting functions for the simulations
Adam Hornsby
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import seaborn.apionly as sns

from matplotlib import rcParams

# set specific colour config
try:
    # plt.style.use('adam_phd')
    flatui = ['#4ecdc4', '#ff6b6b', '#ffe66d', '#dbb1d9', '#312f2f', '#A1A0A0']
    sns.set_palette(flatui, desat=1.0)
except:
    pass

def plot_blobs(X, y):
    """
    Plot the clusters on a 2D axis

    # Parameters
    X (numpy.ndarray): A 2-dimensional matrix of options to select from
    y (numpy.ndarray): A 1-dimensional vector of labels (either choice type 0 or 1)
    """

    font = {'size'   : 7}

    matplotlib.rc('font', **font)
    fig = plt.figure(figsize=(3.5, 2))
    ax = fig.add_subplot(111)

    y = y.astype(str)
    np.place(y, y == '0', '#4ecdc4')
    np.place(y, y == '1', '#ff6b6b')

    sns.scatterplot(X[:, 0], X[:, 1], hue=y, s= 40.0)

    return ax

def calculate_attention_weight_ratio(att_hist):
    """Calculate the ratio between the two attention weights over the course of the simulation"""

    att_ratio = att_hist[:, 0] / att_hist[:, 1]  # the ratio of the attention values

    return att_ratio


def annotate_preferences(ax, pref, color):
    """Add preferences to plot"""

    sns.scatterplot(pref[:, 0], pref[:, 1], 
    linewidth=0, hue=color, 
    alpha=0.75, 
    palette=sns.dark_palette("gray", as_cmap=True), 
    linestyle='-',
    s= 2.0) #  s=1.0, l, 

    ax.text(pref[-1, 0], pref[-1, 1], 'X', color='black');

    return ax

def custom_legend(cmap):
    """Use a custom legend for the plots"""

    custom_lines = [Line2D([0], [0], color='w', marker='o', markerfacecolor='#4ecdc4', markersize=8),
                    Line2D([0], [0], color='w', marker='o', markerfacecolor='#ff6b6b', markersize=8),
                    Line2D([0], [0], color='white', marker='X', markerfacecolor='black', markersize=8),
                    Line2D([0], [0], color=cmap(.1), lw=2)]

    return custom_lines

def plot_simulation_history(X, y, pref_hist, att_hist, save_path=None):
    """
    Plot the preference and attention history of the simulation, including the two choice types

    # Parameters
    X (numpy.ndarray): A 2-dimensional matrix of options to select from
    y (numpy.ndarray): A 1-dimensional vector of labels (either choice type 0 or 1)
    pref_hist (numpy.ndarray): History of preferences over course of the simulation
    att_hist (numpy.ndarray): History of attention weights over course of the simulation
    save_path (str): Location to save the plot
    """

    # plot the clusters
    ax = plot_blobs(X, y)

    # calculate the attention weight ratio (attribute 1 / attribute 2)
    cmap = sns.dark_palette("lightgray", as_cmap=True) # plt.get_cmap('gist_yarg')

    # plot attention weight history
    att_ratio = calculate_attention_weight_ratio(att_hist)
    att_ratio = att_ratio - 0.5  #  normalise to center at 0.5 (for mpl colormap purposes)
    # att_colors = [cmap(x) for x in att_ratio]

    # add in preferences to plot
    ax = annotate_preferences(ax, pref_hist, att_ratio)

    ax.set_xlabel('Attribute 1')
    ax.set_ylabel('Attribute 2')

    # create custom legend
    lines = custom_legend(cmap)
    plt.legend(lines,
               ['Choice Type a', 'Choice Type b',
                'Final Preference', 'Preference History'],
               loc='center right',
               fontsize=7,
               numpoints=1)
    plt.tight_layout()
    plt.xlim([0, 1])

    # format for publication
    sns.despine(left=False, bottom=False, right=True)

    # save the plot
    if save_path is not None:
        plt.savefig(save_path, format='eps', dpi=1000, bbox_inches='tight')
