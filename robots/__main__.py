# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby

"""
Main entrypoint for Robot Experiment analyses
"""

import argparse

from analyse import main 

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def initialise_cli_args():
    """Initialise command line arguments"""

    parser = argparse.ArgumentParser(description='Recreate results from the Robot Experiment')

    parser.add_argument('input', type=str,
                       help='The location of the input CSV of results data')
    parser.add_argument('rerun', type=str2bool, nargs='?',
                        const=True, default=False,
                       help='Are you analysing data from the rerun (with political analyses)? (y/n)')
    parser.add_argument('output', type=str,
                       help='Location of the directory to output plots')

    args = parser.parse_args()

    return args


def create_config(args):
    """Create a config dictionary from cli args"""

    config = {
        # input data
        'input_filename': args.input,

        # if rerun_data==True, then we are analysing data from the robot study re-run...
        # (i.e. breaking down by Democrat and Republican)
        'rerun_data': args.rerun,

        # output path
        'plot_savepath': args.output, # the path to save the plots
    }

    return config


if __name__ == '__main__':

    # define command line arguments
    args = initialise_cli_args()
    config = create_config(args)

    # run the analyses
    main(config)
