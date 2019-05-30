#!/usr/bin/env bash

case "$1" in
  simulation)
    # Run the simulation analyses
    # usage: simulation/ output_location
    python ~/simulation/ "$2"
    ;;
  politics)
    # Run the robot experiment analyses
    Rscript ~/politics/anova.R ~/data/politics/politics_data.csv "$2"
    # usage: simulation/ input_csv n output_location
    python ~/politics/ ~/data/politics/politics_data.csv "$2"
    ;;
  robots)
    # Run the robot experiment analyses
    # usage: simulation/ input_csv n output_location
    python ~/robots/ ~/data/robots/robots-first/robots_results.csv n "$2"
    ;;
  robots_rerun)
    # Run the robot experiment analyses
    # usage: simulation/ input_csv n output_location
    python ~/robots/ ~/data/robots/robots-rerun/robots_rerun_results.csv y "$2"
    ;;
  *)
    echo "usage - simulation|robots|robots_rerun|politics output_location"
esac
