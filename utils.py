"""
Helpers for dealing with vectorized environments.
"""

from collections import OrderedDict
from contextlib import contextmanager
import sys

import gym
import numpy as np


@contextmanager
def stdout_redirected(new_stdout):
    saved_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout.close()
        sys.stdout = saved_stdout

def copy_obs_dict(obs):
    """
    Deep-copy an observation dict.
    """
    return {k: np.copy(v) for k, v in obs.items()}


def dict_to_obs(obs_dict):
    """
    Convert an observation dict into a raw array if the
    original observation space was not a Dict space.
    """
    if set(obs_dict.keys()) == {None}:
        return obs_dict[None]
    return obs_dict


def obs_space_info(obs_space):
    """
    Get dict-structured information about a gym.Space.
    Returns:
      A tuple (keys, shapes, dtypes):
        keys: a list of dict keys.
        shapes: a dict mapping keys to shapes.
        dtypes: a dict mapping keys to dtypes.
    """
    if isinstance(obs_space, gym.spaces.Dict):
        assert isinstance(obs_space.spaces, OrderedDict)
        subspaces = obs_space.spaces
    else:
        subspaces = {None: obs_space}
    keys = []
    shapes = {}
    dtypes = {}
    for key, box in subspaces.items():
        keys.append(key)
        shapes[key] = box.shape
        dtypes[key] = box.dtype
    return keys, shapes, dtypes


def obs_to_dict(obs):
    """
    Convert an observation into a dict.
    """
    if isinstance(obs, dict):
        return obs
    return {None: obs}


def print_dic(dic):
    for key in dic.keys():
        if isinstance(dic[key], dict):
            print(key, ":")
            for items in dic[key]:
                print("    %s : %s" % (items, dic[key][items]))
        else:
            print(key, ':', dic[key])