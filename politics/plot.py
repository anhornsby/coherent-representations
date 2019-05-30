# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby

import string
import matplotlib

matplotlib.use('Agg')
import matplotlib.pylab as plt

import numpy as np
import pandas as pd
import seaborn.apionly as sns

# set specific colour config
try:
    # plt.style.use('adam_phd')
    flatui = ['#4ecdc4', '#ff6b6b', '#ffe66d', '#dbb1d9', '#312f2f', '#A1A0A0']
    sns.set_palette(flatui, desat=1.0)
except:
    pass

# def calculate_change_vs_median(data, contro_dir_col, topic_col, affiliation_col, slider_col, code):
#     """Calculate the change in slider value compared to the median (i.e. expected)"""
    
#     # calculate median values for each topic 
#     medians = data.loc[data[contro_dir_col] == code, :].groupby([affiliation_col, 
#                                                                       topic_col])[slider_col].median().reset_index()
    
#     # now merge the data on, so that we can compare what people slid vs. the median for that topic and party affiliation
#     # when the candidate turned out to have a left wing view
#     merged_data = pd.merge(data[[affiliation_col, contro_dir_col, topic_col, slider_col]], 
#                            medians, on=[affiliation_col, topic_col], how='inner')
    
#     # now calculate the difference in slider value vs. expected 
#     # (i.e. the median where the candidate turned out to be left-wing)
#     # medians are given the prefix of '_y' because it is the second table to be merged
#     merged_data['Change in agreement'] = merged_data[slider_col + '_x'] - merged_data[slider_col + '_y']
    
#     return merged_data

def reverse_dir(x):
    if x == 'Left-wing':
        return 'Right-wing'
    else:
        return 'Left-wing'

def calculate_change_vs_median(data, contro_dir_col, topic_col, affiliation_col, slider_col, absolute=True):
    """Calculate the change in slider value compared to the median (i.e. expected)"""
    
    # calculate median values for each topic (e.g. just for instances where ps revealed a left-wing opinion)
    medians = data.groupby([affiliation_col, topic_col, contro_dir_col])[slider_col].median().reset_index()
    medians[contro_dir_col] = medians[contro_dir_col].apply(reverse_dir)
    
    # now merge the data on, so that we can compare what people slid vs. the median for that topic and party affiliation
    # when the candidate turned out to have a left wing view
    merged_data = pd.merge(data[[affiliation_col, contro_dir_col, topic_col, slider_col]], 
                           medians, on=[affiliation_col, topic_col, contro_dir_col], how='inner')
    
    # now calculate the difference in slider value vs. expected 
    # (i.e. the median where the candidate turned out to be left-wing)
    # medians are given the prefix of '_y' because it is the second table to be merged
    merged_data['Preference change'] = merged_data[slider_col + '_x'] - merged_data[slider_col + '_y']

    if absolute:
        merged_data['Preference change'] = np.abs(merged_data['Preference change'])
        # merged_data = merged_data.rename(columns={'Preference change': 'Absolute preference change'})
    
    return merged_data

def add_label_to_subplots(g, labels=string.ascii_lowercase):
    """Add a prefix before the title of every facet in a Facetgrid"""

    # set the axes titles
    for i, ax in enumerate(g.axes.flatten()):
        ax.set_title('{0:s}) {1:s}'.format(labels[i], ax.get_title().replace('Topic = ', '')), pad=0)

def plot_kdes_of_changes(data, contro_dir_col, topic_col, affiliation_col, slider_col, row_col=None, save_path=None): #right_code
    """Plot kernel densities visualising the change in agreement vs. expected for each topic"""

    sns.set_context(rc={"font.size":9, "lines.linewidth":2})
    sns.set_style('ticks')

    palette = ['#4ecdc4', '#ff6b6b']

    # palette = sns.color_palette("Set1", n_colors=8, desat=1)[0:2][::-1]

    margin_titles=None
    if row_col:
        margin_titles=True

    g = sns.FacetGrid(data,
                  col=topic_col, 
                  row=row_col,
                  hue=affiliation_col,
                  hue_order=['Left-wing', 'Right-wing'],
                  margin_titles=margin_titles,
                  legend_out=True,
                  palette=palette,
                  )

    # set the height of the plot
    height = 2
    if row_col is not None:
        height = 3

    g.fig.set_size_inches(7.20472, height)

    # draw the densities and a rugplot underneath
    g.map(sns.rugplot, slider_col, height=0.05, linewidth=0.5, alpha=0.5)
    kde = g.map(sns.kdeplot, slider_col, linewidth=2, bw=10, shade=False, alpha=0.85)

    # manual over-ride of the legend... lost too many hours to trying to get this to work
    legend_patches = [matplotlib.lines.Line2D([0], [0], linewidth=2, color=palette[0], label='Left-wing'),
    matplotlib.lines.Line2D([0], [0], linewidth=2, color=palette[1], label='Right-wing')]

    # Plot the legend
    plt.legend(title="Chosen candidate's opinion",
                 ncol=2, 
                 handles=legend_patches, 
                 fontsize=9,
                 bbox_to_anchor=(-0.55,2.85))

    # fix the titles
    [plt.setp(ax.texts, text="") for ax in g.axes.flat] # remove the original texts
    g.set_titles(row_template = '{row_name}')
    g.set_ylabels('Proportion')
    add_label_to_subplots(g)


    if save_path is not None:
        # plt.tight_layout()
        plt.savefig(save_path, format='eps', dpi=1000, bbox_inches='tight')
        plt.clf();
        plt.cla();

def create_comparison_boxplot(data, x_col, slider_col, grouping_col, title, bxplt_axis_order, subfigure_col=None, save_path=None):
    """Create a boxplot comparing the slider differences between two groups"""

    # fig, ax = plt.subplots() 
    # fig.set_size_inches(3.50, 3.50)
    sns.set_context(rc={"font.size":7, "lines.linewidth":0.75})

    col_wrap = None
    if subfigure_col is not None:
        col_wrap = 2

    g = sns.catplot(x=x_col, 
                y=slider_col,
                hue=grouping_col, 
                col=subfigure_col,
                hue_order=['Left-wing', 'Right-wing'],
                # height=4,
                # order=['Democrat', 'Republican'],
                data=data,
                sharex=True,
                # legend=True,
                legend_out=False,
                # col_wrap=col_wrap,  
                saturation=0.8,
                linewidth=0.1,
                legend=False,
                # height=3,
                # aspect=7.204/3,
                # palette="Set3",
                kind="boxen", 
                dodge=True)


    # perform fine tuning for publication figure
    lgd=None
    if subfigure_col is not None:
        lgd = g.axes[0][1].legend(loc=9, bbox_to_anchor=(1.,1.35),
            ncol=2,
            # borderaxespad=-1., 
            title="Selected Candidate's Opinion",
            fontsize=7)
        lgd = (lgd,)

        add_label_to_subplots(g)

        # set the figure size to fit the page
        g.fig.set_size_inches(7.20472,2)

    # remove border lines
    sns.despine(left=False, bottom=False, right=True)
    plt.ylim([-10, 110]);

    if save_path is not None:
        # plt.tight_layout()
        plt.savefig(save_path, format='eps', dpi=1000, bbox_extra_artists=lgd, bbox_inches='tight')
        plt.clf();
        plt.cla();
