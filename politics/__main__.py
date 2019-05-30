# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby

"""
Main entrypoint for politics experiment analyses
"""

import argparse

from analyse import main 
from config import CONFIG

def initialise_cli_args():
    """Initialise command line arguments"""

    parser = argparse.ArgumentParser(description='Recreate results from the politics experiment')

    parser.add_argument('input', type=str,
                       help='The location of the input CSV of results data')
    parser.add_argument('output', type=str,
                       help='Location of the directory to output plots')

    args = parser.parse_args()

    return args


def create_config(args, config):
    """Create a config dictionary from cli args"""

    config.update({
        # input data location
        'input_path': args.input, 

        # output path
        'plot_path': args.output, # the path to save the plots
    })

    return config


if __name__ == '__main__':

    # define command line arguments
    args = initialise_cli_args()
    config = create_config(args, CONFIG)

    # run the analyses
    main(config)
