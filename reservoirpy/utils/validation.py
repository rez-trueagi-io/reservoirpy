# Author: Nathan Trouvain at 21/06/2021 <nathan.trouvain@inria.fr>
# Licence: MIT License
# Copyright: Xavier Hinaut (2018) <xavier.hinaut@inria.fr>
from typing import Any, Mapping, Sequence, Union

import numpy as np
from scipy.sparse import issparse

from .types import Weights


def is_square(array: Weights) -> bool:
    return array.shape[0] == array.shape[1] and is_2d(array)


def is_2d(array: Weights) -> bool:
    return array.ndim == 2


def is_sequence_set(seq: Any) -> bool:
    return isinstance(seq, list) or \
           (isinstance(seq, np.ndarray) and seq.ndim > 2)


def is_array(obj: Any) -> bool:
    return obj is not None and isinstance(obj, np.ndarray) or issparse(obj)


def is_mapping(obj):
    return isinstance(obj, Mapping) or \
           ((hasattr(obj, "items") and hasattr(obj, "get")) or
            (not (isinstance(obj, list) or isinstance(obj, tuple)) and
             hasattr(obj, "__getitem__") and
             not hasattr(obj, "__array__")))


def is_numerical(obj):
    return (hasattr(obj, "dtype") and np.issubdtype(obj.dtype, np.number)) \
           or isinstance(obj, int) \
           or isinstance(obj, float)


def is_node(obj):
    return hasattr(obj, "state") and callable(obj.state) \
           and hasattr(obj, "call") and hasattr(obj, "run") \
           and hasattr(obj, "_forward")


def add_bias(X):
    if isinstance(X, np.ndarray):
        if X.ndim < 2:
            X = X.reshape(1, -1)
        return np.hstack([np.ones((X.shape[0], 1)), X])
    elif isinstance(X, list):
        new_X = []
        for x in X:
            new_X.append(np.hstack([np.ones((x.shape[0], 1)), x]))
        return new_X


def _check_values(array_or_list: Union[Sequence, np.ndarray], value: Any):
    """ Check if the given array or list contains the given value. """
    if value == np.nan:
        assert np.isnan(array_or_list).any() == False, \
            f"{array_or_list} should not contain NaN values."
    if value is None:
        if type(array_or_list) is list:
            assert np.count_nonzero(array_or_list == None) == 0, \
                f"{array_or_list} should not contain None values."
        elif type(array_or_list) is np.array:
            # None is transformed to np.nan when it is in an array
            assert np.isnan(array_or_list).any() == False, \
                f"{array_or_list} should not contain NaN values."


def check_vector(array, allow_reshape=True, expand_axis=0):
    if not isinstance(array, np.ndarray):
        raise TypeError(
            f"Data type '{type(array)}' not understood. All sequences of data "
            f"should be Numpy arrays, or lists of Numpy arrays.")

    if not (np.issubdtype(array.dtype, np.number)):
        raise TypeError(
            f"Impossible to operate on non-numerical data, in array: {array}")

    if allow_reshape:
        if array.ndim < 2:
            if expand_axis == 0:
                array = array[np.newaxis, :]
            elif expand_axis == 1:
                array = array[:, np.newaxis]

    return array


def check_input_lists(X, dim_in, Y=None, dim_out=None):
    if isinstance(X, np.ndarray):
        X = [X]

    if Y is not None:
        if isinstance(Y, np.ndarray):
            Y = [Y]
        if not (len(X) == len(Y)):
            raise ValueError(f"Inconsistent number of inputs and targets: "
                             f"found {len(X)} input sequences, but {len(Y)} "
                             f"target sequences.")

    for i in range(len(X)):
        x = check_vector(X[i], allow_reshape=False)

        if x.ndim != 2:
            raise ValueError(f"Input {i} has shape {x.shape} but should "
                             f"be 2-dimensional, with first axis representing "
                             f"time and second axis representing features.")

        if x.shape[1] != dim_in:
            raise ValueError(
                f"Input {i} has {x.shape[1]} features but ESN expects "
                f"{dim_in} features as input.")

        if Y is not None:
            y = check_vector(Y[i], allow_reshape=False)
            if y.ndim != 2:
                raise ValueError(f"Target {i} has shape {y.shape} but should "
                                 f"be 2-dimensional, with first axis "
                                 f"representing "
                                 f"time and second axis representing "
                                 f"features.")

            if x.shape[0] != y.shape[0]:
                raise ValueError(f"Inconsistent inputs and targets lengths: "
                                 f"input {i} has length {x.shape[0]} but "
                                 f"corresponding target {i} has length "
                                 f"{y.shape[0]}.")

            if dim_out is not None:
                if y.shape[1] != dim_out:
                    raise ValueError(
                        f"Target {i} has {y.shape[1]} features but ESN "
                        f"expects "
                        f"{dim_out} features as feedback.")

    return X, Y


def check_datatype(array, caller=None, name=None, allow_inf=False,
                   allow_nan=False):
    caller_name = f"{caller.__class__.__name__} :" if caller is not None \
        else ""
    array_name = name if isinstance(name, str) else array.__class__.__name___

    if not isinstance(array, np.ndarray) and not issparse(array):
        array = np.asarray(array)

    if not (np.issubdtype(array.dtype, np.number)):
        raise TypeError(
            f"{caller_name} Impossible to operate on non-numerical data, "
            f"in array '{array_name}' of type {array.dtype}: {array}")

    if not allow_nan:
        msg = f"{caller_name} Impossible to operate on NaN value, " \
              f"in array '{array_name}': {array}."
        if issparse(array):
            if np.any(np.isnan(array.data)):
                raise ValueError(msg)
        else:
            if np.any(np.isnan(array)):
                raise ValueError(msg)

    if not allow_inf:
        msg = f"{caller_name} Impossible to operate on inf value, " \
              f"in array '{array_name}': {array}."
        if issparse(array):
            if np.any(np.isinf(array.data)):
                raise ValueError(msg)
        else:
            if np.any(np.isinf(array)):
                raise ValueError(msg)

    return array


def check_reservoir_matrices(W, Win, Wout=None, Wfb=None, caller=None):
    caller_name = f"{caller.__class__.__name__} :" if caller is not None \
        else ""

    W = check_datatype(W, caller=caller, name="W")
    Win = check_datatype(Win, caller=caller, name="Win")

    in_shape = Win.shape
    res_shape = W.shape

    # W shape is (units, units)
    if res_shape[0] != res_shape[1]:
        raise ValueError(
            f"{caller_name} reservoir matrix W should be square but has "
            f"shape {res_shape}.")
    # Win shape is (units, dim_in [+ bias])
    if in_shape[0] != res_shape[0]:
        raise ValueError(
            f"{caller_name} dimension mismatch between W and Win: "
            f"W is of shape {res_shape} and Win is of shape {in_shape} "
            f"({res_shape[0]} != {in_shape[0]}).")

    # Wout shape is (dim_out, units + bias)
    out_shape = None
    if Wout is not None:
        Wout = check_datatype(Wout, caller=caller, name="Wout")
        out_shape = Wout.shape
        if out_shape[1] != res_shape[0] + 1:
            raise ValueError(
                f"{caller_name} dimension mismatch between W and Wout: "
                f"W is of shape {res_shape} and Wout is of shape {out_shape} "
                f"({res_shape[0]} + bias (1) != {out_shape[1]}).")
    # Wfb shape is (units, dim_out)
    if Wfb is not None:
        Wfb = check_datatype(Wfb, caller=caller, name="Wfb")
        fb_shape = Wfb.shape
        if out_shape is not None:
            if fb_shape[1] != out_shape[0]:
                raise ValueError(
                    f"{caller_name} dimension mismatch between Wfb and Wout: "
                    f"Wfb is of shape {fb_shape} and Wout is of sh"
                    f"ape {out_shape} "
                    f"({fb_shape[1]} != {out_shape[0]}).")
        if fb_shape[0] != res_shape[0]:
            raise ValueError(
                f"{caller_name} dimension mismatch between W and Wfb: "
                f"W is of shape {res_shape} and Wfb is of shape {fb_shape} "
                f"({res_shape[0]} != {fb_shape[0]}).")

    return W, Win, Wout, Wfb
