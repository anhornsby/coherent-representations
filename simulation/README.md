# Coherency Maximization Simulation

This area contains all code necessary to re-create the simulation described in Hornsby and Love, 2019.

### File structure

This repository contains 3 python files:

1. `simulate.py` - Contains code necessary for performing the simulation, as described in the original paper.
2. `model.py` - Contains code necessary for simulating the `CoherencyMaximizationAgent`, as described in the paper
3. `plot.py` - Contains code necessary for re-creating the plot, as shown in the paper.

### Running the simulation

The code requires the following dependencies:

```
numpy>=1.13.3
sklearn>=0.19.1
matplotlib>=2.2.2
```

To run the simulation, please run the following command using Python 2.7:

```bash
python ./
```

Note that the main parameters of the simulation can be modified using the `CONFIG` object within `simulate.py`.

### Questions

Please [get in touch](mailto:adamnhornsby@gmail.com)