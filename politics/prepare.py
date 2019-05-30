# -*- coding: utf-8 -*-
# !/usr/bin/env python

import logging

def rename_data(data, config):
    """Rename column names and values in the raw dataset"""

    # rename columns
    vote_col_name = "Selected Candidate's Opinion"
    affil_col_name = "Participant Affiliation"
    topic_col_name = 'Topic'
    slider_p_name = 'Agreement slider'

    data = data.rename(
        columns={'VOTE_CONTRO_DIR': vote_col_name, 
        'AFFILIATION': affil_col_name, 
        'CONTRO_ID': topic_col_name,
        'SLIDER_P_DIR': slider_p_name})

    config['vote_contro_dir_col'] = vote_col_name
    config['affiliation_col'] = affil_col_name
    config['contro_topic_col'] = topic_col_name
    config['political_slider'] = slider_p_name

    # rename the values
    data[vote_col_name] = data[vote_col_name].replace({'left': 'Left-wing', 'right': 'Right-wing'}, axis=0)
    config['left_code'] = 'Left-wing'
    config['right_code'] = 'Right-wing'

    data[config['affiliation_col']] = data[config['affiliation_col']].replace({'d': 'Democrat', 'r': 'Republican'},
                                                                              axis=0)
    config['democrat'] = 'Democrat'
    config['republican'] = 'Republican'

    data[topic_col_name] = data[topic_col_name].replace(
        {'immigration': 'Immigration', 'trade': 'Trade', 'abortion': 'Abortion'}, axis=0)

    return data, config


def profile_participants(data, gender_col, age_col, affiliation_col):
    """Determine the number of people in each group and the mean and SD age"""

    logging.info('There are {0:d} participants in this dataset'.format(data.shape[0]))

    logging.info('The final gender split was: {0:s}'.format(data[gender_col].value_counts(normalize=True)))

    logging.info('The final affiliation split was: {0:s}'.format(data[affiliation_col].value_counts(normalize=True)))

    logging.info('The mean age was: {0:f} (SD = {1:f})'.format(data[age_col].mean(), data[age_col].std()))