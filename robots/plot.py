# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby

from __future__ import division

import matplotlib
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    plt.style.use('adam_phd')
except:
    pass

import matplotlib
font = {'weight' : 'regular',
    'size'   : 7}

matplotlib.rc('font', **font)

def standard_error(p, n):
    """
    Calculate the stnadard error of a proportion

    # Parameters
    p (float): Proportion
    n (int): Sample size
    """

    num = p * (1. - p)
    return np.sqrt(num / n)


def barplot(data, save_path='plots/2d_axis_plot.png'):
    """Plot the barplot of preferences"""

    # relabel preference data for plot
    data['Preference'] = data['Preference'].replace(to_replace={0: '1st', 1: '2nd', 2: '3rd'})
    total_counts = pd.pivot_table(data, index='Preference', aggfunc=np.sum)
    total_counts = total_counts.rename(columns={'Chosen': 'Chosen unique', 'NotChosen': 'Non-chosen'})

    # calculate proportions
    total_prps = total_counts / total_counts.sum()
    total_prps = total_prps[['Chosen unique', 'Shared', 'Non-chosen']]
    total_prps = total_prps

    # calculate stdes
    stdes = standard_error(total_prps, total_counts)
    ax = total_prps.plot(kind='bar', yerr=stdes, figsize=(2.87402, 2.95276))

    ax.legend(loc='upper center', fontsize=7, ncol=1, bbox_to_anchor=(0.5, 1.25))
    ax.set_xticklabels(total_prps.index, rotation=0)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
    plt.ylabel('Chosen')
    # plt.tight_layout()
    plt.savefig(save_path, dpi=1000, bbox_inches='tight')


def plot_trial_variability(data, save_path='plots/line_plot.png'):
    """Plot the variation in preferences over time"""

    trial_variability = data.rename(columns={'Chosen': 'Chosen unique', 'NotChosen': 'Non-chosen'})
    trial_variability.plot(kind='line')

    plt.tight_layout()
    plt.savefig(save_path)
