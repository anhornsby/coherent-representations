# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby
from __future__ import division

import matplotlib
matplotlib.use('Agg')

import sys
import scipy
from scipy import stats
import pandas as pd
import numpy as np
import statsmodels
from scipy.stats import friedmanchisquare, wilcoxon, iqr
import statsmodels.api as st
import logging

from prepare import qa_results, prepare_modelling_data
from plot import barplot, plot_trial_variability

# CONFIG = {
#     # input data
#     'input_filename': '../data/robot_rerun_data_raw.csv', # the path to the data

#     # if rerun_data==True, then we are analysing data from the robot study re-run...
#     # (i.e. breaking down by Democrat and Republican)
#     'rerun_data': True, 

#     # output path
#     'plot_savepath': './plots/', # the path to save the plots
# }


def initialise_logger():
    """Initialise logger to print messages to stdout"""

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def run_ols(df, x_col, y_col):
    """Run multiple OLS' returning the p values each time"""

    mod = statsmodels.regression.linear_model.OLS(df[y_col], st.add_constant(df[x_col].astype(float), prepend=False))
    result = mod.fit()
    logging.info(result.summary())


def calculate_rank_sums(data):
    """Calculate the rank sums of preference for each choice type"""

    # rollup ranks across blocks
    data['Preference'] = data['Preference'].astype(int)

    data[['NotChosen', 'Shared', 'Chosen']] = data[['NotChosen', 'Shared', 'Chosen']].astype(int)
    data['ChoiceType'] = data[['NotChosen', 'Shared', 'Chosen']].idxmax(axis=1)
    rank_sums = pd.pivot_table(data, values='Preference', index='Participant', columns='ChoiceType',
                               aggfunc=np.sum)

    logging.info('Rank Medians: {0:s}'.format(rank_sums.astype(float).median()))
    logging.info('Rank IQRs {0:s}:'.format(rank_sums.astype(float).agg(iqr)))

    return rank_sums


def friedman_chi_square(rank_sums):
    """Calculate the Friedman omnibus test on the summed preferences"""

    # calculate the friedman model
    chi, p = friedmanchisquare(rank_sums['NotChosen'].values,
                               rank_sums['Shared'].values,
                               rank_sums['Chosen'].values)

    logging.info('The results of the Friedman Chi Square test are: Chi = {0:f}, p = {1:f}'.format(chi, p))


def perform_wilcoxon_tests(rank_sums):
    """Perform three wilcoxon tests to calculate significance of each of the pairwise comparisons"""

    # compare chosen unique with shared
    # z methodology here: https://www.sheffield.ac.uk/polopoly_fs/1.714576!/file/stcp-marquier-WilcoxonR.pdf
    for a, b in [['Chosen', 'Shared'], ['Chosen', 'NotChosen'], ['NotChosen', 'Shared']]:
        T, p = wilcoxon(rank_sums[a].values - rank_sums[b].values)

        z = scipy.stats.norm.ppf(p / 2.)
        r = np.abs(z) / np.sqrt(rank_sums[a].shape[0])

        logging.info(
            'The Wilcoxon signed rank test comparing {0:s} with {1:s} returned: Z={2:f}, p={3:f}, r={4:f}'.format(a, b,
                                                                                                                  z, p,
                                                                                                                  r))


def per_trial_variability(data):
    """
    Analyse the per-trial variability in first preferences over time. Check that people do not
    increase their likelihood of responding in any way over the course of the experiment.

    This means calculating an OLS with # first preferences ~ Trial
    for each choice type.
    """

    # sum the preferences for each ChoiceType, broken down by trial
    first_prefs = data[data['Preference'] == 0]
    first_prefs['Preference'] += 1  # make the preferences index at 1 not 0
    trial_variability = pd.pivot_table(first_prefs, values='Preference', index='Trial', columns='ChoiceType',
                                       aggfunc=np.sum)

    for col in ['Chosen', 'Shared', 'NotChosen']:
        run_ols(trial_variability.reset_index(), 'Trial', col)

    # plot preferences over time
    return trial_variability


def run_significance_tests_and_plot(data, line_plot_path, bar_plot_path):
    """
    Format the data for analyses, run significance tests to check whether preferences varied
    by image type and then plot these for the paper.
    """

    # format data in friendly way, such that each trial has a separate row
    modelling_data = prepare_modelling_data(data, trials=10)

    # determine the rank sums of preferences for each choice type
    rank_sums = calculate_rank_sums(modelling_data)

    logging.info('*** SIGNIFICANCE TESTING ***')
    # determine the friedman test results for the overall significance
    friedman_chi_square(rank_sums)

    # calculate the wilcoxon signed rank tests
    perform_wilcoxon_tests(rank_sums)

    # calculate significance tests to measure whether there was any shift in preferences over time
    per_trial = per_trial_variability(modelling_data)
    plot_trial_variability(per_trial, line_plot_path)

    logging.info('*** PLOTTING DATA ***')
    # calculate bar plot
    barplot(modelling_data, save_path=bar_plot_path)


def main(config):
    """Main entrypoint for code"""

    initialise_logger()

    # read in data
    data = pd.read_csv(config['input_filename'])

    logging.info('*** DATA PREPARATION ***')
    # print key statistics for this dataset
    qa_results(data)

    # now perform significance tests
    run_significance_tests_and_plot(data, 
        config['plot_savepath'] + 'line_plot.png', 
        config['plot_savepath'] + '2d_axis_plot.png')

    # if we're analysing the re-run data, then also break down the analyses
    # by political party affiliation
    if config['rerun_data']:
        for party in ['Democrat', 'Republican']:

            party_data = data.loc[data['party'] == party, :].copy(deep=True).reset_index(drop=True)

            logging.info('*** ANALYZING {0:s} PARTICIPANTS (n={1:d}) ***'.format(party, party_data.shape[0]))

            run_significance_tests_and_plot(party_data,
                '{0:s}{1:s}_{2:s}'.format(config['plot_savepath'], party, 'line_plot.png'),
                 '{0:s}{1:s}_{2:s}'.format(config['plot_savepath'], party, '2d_axis_plot.png')
                 )


if __name__ == '__main__':
    main(CONFIG)