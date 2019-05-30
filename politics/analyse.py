# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby

"""
Analyse data from the politics experiment
"""

from __future__ import division

import sys
import logging
import pandas as pd
import numpy as np
from datetime import datetime

from scipy.stats import chi2_contingency, mannwhitneyu, iqr, wilcoxon
import statsmodels.formula.api as smf
from statsmodels.graphics.factorplots import interaction_plot

# from config import CONFIG
from prepare import rename_data, profile_participants
from plot import create_comparison_boxplot, plot_kdes_of_changes


def initialise_logger():
    """Initialise logger to print messages to stdout"""

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)


def calculate_median_and_range(data, target_col, grouping_col='VOTE_CONTRO_DIR'):
    """
    Compare the average political beliefs of people that unknowingly chose
    a right wing candidate compared to those than unknowingly chose a left
    wing candidate.

    As we're looking at ranks, we'll report the medians and IQR
    """

    # calculate the mean average
    mean_diff = data.groupby(grouping_col)[target_col].median()
    iqr_diff = data.groupby(grouping_col)[target_col].agg(iqr)

    return mean_diff, iqr_diff


def common_language_effect_size(lessers, greaters):
    """Common-Language Effect Size
    Probability that a random draw from `greater` is in fact greater
    than a random draw from `lesser`.

    Taken from https://github.com/ajschumacher/cles/blob/master/cles.py
    (Thanks!)

    Args:
      lesser, greater: Iterables of comparables.
    """
    if len(lessers) == 0 and len(greaters) == 0:
        raise ValueError('At least one argument must be non-empty')
    # These values are a bit arbitrary, but make some sense.
    # (It might be appropriate to warn for these cases.)
    if len(lessers) == 0:
        return 1
    if len(greaters) == 0:
        return 0
    numerator = 0
    lessers, greaters = sorted(lessers), sorted(greaters)
    lesser_index = 0
    for greater in greaters:
        while lesser_index < len(lessers) and lessers[lesser_index] < greater:
            lesser_index += 1
        numerator += lesser_index  # the count less than the greater
    denominator = len(lessers) * len(greaters)

    return float(numerator) / denominator


def two_samples_test(sample_means_one, sample_means_two):
    """Perform a two-sample non-parametric test"""

    t, p = mannwhitneyu(sample_means_one.values, sample_means_two.values)

    return t, p


def compare_pairwise_sliders(data, grouping_title, political_slider_col, grouping_col,
                             left_code='left', right_code='right'):
    """
    Perform pairwise comparisons of slider values between people that unknowingly
    chose a left-wing candidate (left_code) compared to a rightwing candidate (right_code).

    # Parameters
    data (pandas.DataFrame) - A DataFrame of the results in question
    grouping_title (str) - A title describing the comparison
    political_slider_col (str) - The column name of the slider value
    grouping_col (str) - The column to be grouped in the comparison (e.g., the political affiliation)
    plot_path (str) - The location to save the plot

    left_code (str) - The code inside the column that denotes the candidate revealing a left-wing opinion
    right_code (str) - The code inside the column that denotes the candidate revealing a right-wing opinion
    """

    # compare political preference of ps that chose left wing vs. right wing candidates
    total_mean, total_stde = calculate_median_and_range(data,
                                                        political_slider_col,
                                                        grouping_col=grouping_col)

    # perform a significance test of those two samples
    t, p = two_samples_test(data[data[grouping_col] == left_code][political_slider_col],
                            data[data[grouping_col] == right_code][political_slider_col])

    # calculate non-parametric effect size
    es = common_language_effect_size(data[data[grouping_col] == left_code][political_slider_col],
                            data[data[grouping_col] == right_code][political_slider_col])

    logging.info('A Mann Whitney U comparison for {0:s} showed that the slid political preferences of candidates \
that chose left and right candidates were different: U={1:f} p={2:f}, effect size={3:f} {4:s}: Median={5:f}, IQR={6:f}, {7:s}: Median={8:f} IQR={9:f}'.format(
        grouping_title,
        t,
        p,
        es,
        left_code,
        total_mean.to_dict()[left_code],
        total_stde.to_dict()[left_code],
        right_code,
        total_mean.to_dict()[right_code],
        total_stde.to_dict()[right_code]
        ))

    return total_mean, total_stde, p


def count_and_chi_square(index, columns):
    """Perform a crosstab of index and columns and then calculate a chi-square contingency"""

    # generate counts
    counts = pd.crosstab(index, columns)

    # perform chisquare test
    chi2, p, dof, _ = chi2_contingency(counts)

    return chi2, p, dof


def compare_overall_and_pairwise(data, slider_col, grouping_col, topic_col, code_one, code_two):
    """
    Compare the slider values overall and then make each pairwise comparison within a topic
    """

    mean, stde, _ = compare_pairwise_sliders(data,
                                             'Overall',
                                             slider_col,
                                             grouping_col,
                                             code_one,
                                             code_two)

    # now loop over each controversial topic
    for topic in data[topic_col].unique():
        # subset out participants responding to certain topics (e.g. to trade)
        topic_data = data[data[topic_col] == topic]

        # perform the comparisons
        # e.g. did participants vary their level of agreement after a newly-revealed opinion on free trade?
        compare_pairwise_sliders(topic_data,
                                 topic,
                                 slider_col,
                                 grouping_col,
                                 code_one,
                                 code_two)


def post_hoc_analyses(data, affiliation_col, contro_col, slider_raw_col):
    """Perform post-hoc analyses"""

    # produce a 2 x 2 chi-square between Vote and Affiliation
    chi2, p, dof = count_and_chi_square(data[affiliation_col], data[contro_col])
    logging.info(
        'The chi-square test comparing affiliation with vote yielded: X^2={0:f}, p={1:f}, dof={2:d}'.format(chi2, p,
                                                                                                            dof))

    # check whether there was any position effect (e.g. people tend to click on the right side of the slider)
    t, p = wilcoxon(data[slider_raw_col] - 50.)
    logging.info("""The Wilcoxon signed-rank test evaluating whether there was a bias in peoples slider responses yielded:' +
    'Z={0:f}, p={1:f}, median={2:f}, IQR={3:f}""".format(t, p, data[slider_raw_col].median(), iqr(data[slider_raw_col])))

def compare_democrats_and_republicans(data, config):
    """Evaluate the effects of the candidate's revelation for democrats and republicans separately"""

    # calculate the per-topic changes for democrats and republicans
    for affil in data[config['affiliation_col']].unique():
        logging.info('** Analysing {0:s} participants **'.format(affil))

        affil_data = data[data[config['affiliation_col']] == affil]

        # perform the stats test
        # compare the agreement values of people who affiliate as democrat/republican
        compare_overall_and_pairwise(affil_data,
                                     config['political_slider'],
                                     config['vote_contro_dir_col'],
                                     config['contro_topic_col'],
                                     config['left_code'],
                                     config['right_code'])

        # plot the differences in a boxplot
        create_comparison_boxplot(affil_data,
                                  config['contro_topic_col'],
                                  config['political_slider'],
                                  config['vote_contro_dir_col'],
                                  '',
                                  ['Abortion', 'Immigration', 'Trade'],
                                  save_path=config['plot_path'] + '{0}_interaction_plot.eps'.format(affil))


def main(config):
    """Main entrypoint for code"""

    initialise_logger()

    # import data
    data = pd.read_csv(config['input_path'])

    # rename values
    logging.info('** Pre-processing **')
    data, config = rename_data(data, config)

    # profile participants
    logging.info('** Profiling ** ')
    profile_participants(data, config['gender_col'], config['age_col'], config['affiliation_col'])

    # perform overall comparison
    logging.info('** Main Analyses **')

    # calculate main effect of political party
    compare_pairwise_sliders(data,
                             'Overall Political Party',
                             config['political_slider'],
                             config['affiliation_col'],
                             'Democrat',
                             'Republican')

    # calculate main effect of candidate's political stance
    compare_overall_and_pairwise(data,
                                 config['political_slider'],
                                 config['vote_contro_dir_col'],
                                 config['contro_topic_col'],
                                 config['left_code'],
                                 config['right_code'])

    # plot these main effects in a boxplot
    create_comparison_boxplot(data,
                              config['affiliation_col'],
                              config['political_slider'],
                              config['vote_contro_dir_col'],
                              '',
                              None,
                              save_path=config['plot_path'] + 'interaction_plot.eps')

    # concatenate all values with separate topics
    all_data = data.copy(deep=True)
    all_data[config['contro_topic_col']] = 'All'
    all_data = pd.concat([all_data, data], axis=0)

    create_comparison_boxplot(all_data,
                          config['affiliation_col'],
                          config['political_slider'],
                          config['vote_contro_dir_col'],
                          '',
                          None,
                          subfigure_col=config['contro_topic_col'],
                          save_path=config['plot_path'] + 'interaction_topic_plot.eps')

    # plot kdes
    plot_kdes_of_changes(all_data, 
      config['vote_contro_dir_col'], 
      config['contro_topic_col'], 
      config['vote_contro_dir_col'], 
      config['political_slider'], 
      row_col=config['affiliation_col'], 
      save_path=config['plot_path'] + 'response_kdes.eps')

    # perform per-topic comparisons within democrats and republicans separately
    compare_democrats_and_republicans(data, config)

    # perform all post-hoc analysis
    logging.info('** Post-hoc Analyses **')
    post_hoc_analyses(data,
                      config['affiliation_col'],
                      config['vote_contro_dir_col'],
                      config['slider_raw_col'])
