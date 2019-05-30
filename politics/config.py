# -*- coding: utf-8 -*-
# !/usr/bin/env python

"""
Configuration driving the analyses
"""

CONFIG = {

    # data
    'input_path': 'raw_data.csv', # the filepath to the input CSV

    # columns
    'vote_contro_dir_col': 'VOTE_CONTRO_DIR',  # the direction of the political belief that the candidate revealed
    'political_slider': 'SLIDER_P_DIR',  # the direction of the slider, where higher = more republican
    'contro_topic_col': 'CONTRO_ID', # column name describing the controversial topic selected from
    'affiliation_col': 'AFFILIATION', # the column describing the self-reported affiliation of participants
    'total_clicks_col': 'TOTAL_CLICKS', # the total number of clicks made by the participant
    'gender_col': 'GENDER', # self reported gender of participant
    'age_col': 'AGE', # self reported age of participant
    'slider_raw_col': 'SLIDER_RAW', # the raw, un-normalised slider value (i.e. higher = further to the right)
    'agreement_col': 'SLIDER_AGREEMENT', # the normalised slider value, where higher values = more agreement with their chosen candidate

    #  plots
    'plot_path': './plots/', # path to save plots

    # codes
    'left_code': 'left', # the value in contro_topic_col denoting left-wing choices
    'right_code': 'right', # the value in contro_topic_col denoting right-wing choices
    'democrat': 'd', # the value in affiliation_col denoting republicans
    'republican': 'r' # the value in affiliation_col denoting democrats
}