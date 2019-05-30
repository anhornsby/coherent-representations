# -*- coding: utf-8 -*-
#!/usr/bin/env python
# Adam Hornsby

"""
Data preprocessing and cleaning functions
"""

import numpy as np
import pandas as pd
import ast

import logging

def qa_results(data):
    """Gather key statistics on the dataset"""

    # check how many rows are in dataset
    logging.info('There are {0:f} rows in this dataset'.format(data.shape[0]))

    # print mean age
    logging.info('The mean age of our participants is {0:f} sd={1:f}'.format(data['age'].mean(),
                                                                      data['age'].std()))

    # check how many were female
    gender_counts = data['gender'].value_counts()
    logging.info('The gender split was: {0:s}'.format(gender_counts))


def prepare_modelling_data(data, trials=10):
    """
    Prepare the raw data for statistical analyses

    # Parameters
    :param data: Pandas DataFrame containing raw data, as it is shown in the original CSV
    :param trials: Integer describing the number of trials that were run (in this case, =10)
    :return:
    """

    final_data = []

    # loop over all rows in the data
    for repeat in range(data.shape[0]):

        # subset each row out
        back_config = data.ix[repeat, 'back_config']
        back_config = ast.literal_eval(back_config)

        choices = data.ix[repeat, 'choices']

        skip = False
        try:
            choices = choices.replace(',null', '')
            choices = ast.literal_eval(choices)
        except ValueError:
            skip = True
            print('Skipping row {0:d} because {1:s}'.format(repeat, choices))

        if not skip:

            for trial in range(trials):

                # determine whether choice was chosen before or not
                choice = choices[trial][2]  # list of final choices
                backs = back_config[trial]

                first_choice = choices[trial][0]
                chosen_unique = backs['robot' + str(first_choice) + '_back'][0]

                # create final dataset
                for i, c in enumerate(choice):
                    row_data = []
                    row_data += [c]  # the choice
                    row_data += [trial]  # the trial
                    if backs['both'][0] == c:
                        row_data += [0, 1, 0]  # shared
                    elif chosen_unique == c:
                        row_data += [0, 0, 1]  # unique
                    else:
                        row_data += [1, 0, 0]  # unchosen
                    row_data += [repeat]
                    row_data += [i]  # the preference

                    final_data.append(row_data)

    final_data = np.vstack(final_data)
    final_data = pd.DataFrame(final_data,
                              columns=['Robot Design', 'Trial', 'NotChosen', 'Shared'
                                  , 'Chosen', 'Participant', 'Preference'])

    return final_data