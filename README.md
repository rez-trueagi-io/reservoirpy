![ReservoirPy banner](static/rpy_banner_bw.png)

[![PyPI version](https://badge.fury.io/py/reservoirpy.svg)](https://badge.fury.io/py/reservoirpy)
[![Documentation Status](https://readthedocs.org/projects/reservoirpy/badge/?version=latest)](https://reservoirpy.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://travis-ci.org/reservoirpy/reservoirpy.svg?branch=master)](https://travis-ci.org/reservoirpy/reservoirpy)


# ReservoirPy (v0.3.0-**beta**) 🌀 🧠
**Simple and flexible code for Reservoir Computing architectures like Echo State Networks (ESN).**


```python
from reservoirpy.nodes import Reservoir, Ridge, Input

data      = Input(input_dim=1)
reservoir = Reservoir(100, lr=0.3, sr=1.1)
readout   = Ridge(1, ridge=1e-6)

esn = data >> reservoir >> readout

forecast = esn.fit(X, y).run(timeseries)
```


ReservoirPy is a simple user-friendly library based on Python scientific modules. It provides a flexible interface to implement efficient Reservoir Computing (RC) architectures with a particular focus on Echo State Networks (ESN). Advanced features of ReservoirPy allow to improve computation time efficiency on a simple laptop compared to basic Python implementation. Some of its features are: offline and online training, parallel implementation, sparse matrix computation, fast spectral initialization, etc. Moreover, graphical tools are included to easily explore hyperparameters with the help of the hyperopt library.

This library works for Python 3.8 and higher.

## Offcial documentation 📖

See [the official ReservoirPy's documentation](https://reservoirpy.readthedocs.io/en/latest/?badge=latest)
to learn more about the main features of ReservoirPy, its API and the installation process.

## Examples and tutorials 🎓

[Go to the tutorial folder](./tutorials/) for tutorials in Jupyter Notebooks.

[Go to the examples folder](./examples/) for examples and papers with codes, also in Jupyter Notebooks.


## Quick try ⚡
#### Chaotic timeseries prediction (MackeyGlass)

Run and analyse these two files to see how to make timeseries prediction with Echo State Networks:
- simple_example_MackeyGlass.py (using the ESN class)

    ```bash
    python simple_example_MackeyGlass.py
    ```

- minimalESN_MackeyGlass.py (without the ESN class)

    ```bash
    python minimalESN_MackeyGlass.py
    ```

## Paper with tutorials
Tutorial on ReservoirPy can be found in this [Paper (Trouvain et al. 2020)](https://hal.inria.fr/hal-02595026).

## Explore Hyper-Parameters with Hyperopt
A quick tutorial on how to explore hyperparameters with ReservoirPy and Hyperopt can be found in this [paper (Trouvain et al. 2020)](https://hal.inria.fr/hal-02595026).

Take a look at our **advices and general method to explore hyperparameters** for reservoirs in our recent paper:
"Which Hype for My New Task? Hints and Random Search for Echo State Networks Hyperparameters", ICANN 2021
[HTML](https://link.springer.com/chapter/10.1007/978-3-030-86383-8_7) [PDF](https://hal.inria.fr/hal-03203318/)

[Turorial and Jupyter Notebook for hyper-parameter exploration](./examples/Optimization%20of%20hyperparameters)

More info on hyperopt: [Official website](http://hyperopt.github.io/hyperopt/)

## Papers and projects using ReservoirPy
- Trouvain & Hinaut (2021) Canary Song Decoder: Transduction and Implicit Segmentation with ESNs and LTSMs. ICANN 2021 [HTML](https://link.springer.com/chapter/10.1007/978-3-030-86383-8_6) [HAL](https://hal.inria.fr/hal-03203374) [PDF](https://hal.inria.fr/hal-03203374/document)
- Pagliarini et al. (2021) Canary Vocal Sensorimotor Model with RNN Decoder and Low-dimensional GAN Generator. ICDL 2021. [HTML](https://ieeexplore.ieee.org/abstract/document/9515607?casa_token=QbpNhxjtfFQAAAAA:3klJ9jDfA0EEbckAdPFeyfIwQf5qEicaKS-U94aIIqf2q5xkX74gWJcm3w9zxYy9SYOC49mQt6vF) 
- Pagliarini et al. (2021) What does the Canary Say? Low-Dimensional GAN Applied to Birdsong. HAL preprint. [HAL](https://hal.inria.fr/hal-03244723/) [PDF](https://hal.inria.fr/hal-03244723/document)
- Which Hype for My New Task? Hints and Random Search for Echo State Networks Hyperparameters. ICANN 2021 [HTML](https://link.springer.com/chapter/10.1007/978-3-030-86383-8_7) [HAL](https://hal.inria.fr/hal-03203318) [PDF](https://hal.inria.fr/hal-03203318)



## Cite
Trouvain, N., Pedrelli, L., Dinh, T. T., Hinaut, X. (2020) Reservoirpy: an efficient and user-friendly library to design echo state networks. In International Conference on Artificial Neural Networks (pp. 494-505). Springer, Cham. [HTML](https://link.springer.com/chapter/10.1007/978-3-030-61616-8_40) [HAL](https://hal.inria.fr/hal-02595026) [PDF](https://hal.inria.fr/hal-02595026/document)
