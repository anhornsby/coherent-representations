# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby

"""
Main entrypoint for coherency maximization simulation

Demonstrates how strong subjective preferences could be learned using the intrinsic desire to 
maximize coherency between one's past and present preferences
"""

import argparse
from simulate import CONFIG, main 


def initialise_cli_args():
    """Initialise command line arguments"""

    parser = argparse.ArgumentParser(description='Recreate results from the coherency maximization simulation')

    parser.add_argument('output', type=str,
                       help='Location of the directory to output plots')

    args = parser.parse_args()

    return args


def create_config(args, config):
    """Create a config dictionary from cli args"""

    config.update({
        # output path
        'save_path': args.output, # the path to save the plots
    })

    return config


if __name__ == '__main__':

    # define command line arguments
    args = initialise_cli_args()
    config = create_config(args, CONFIG)

    # run the analyses
    main(config)
