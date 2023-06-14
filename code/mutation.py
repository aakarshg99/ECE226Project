import copy
import random
import numpy as np

def random_architecture(startLength):
    """Returns a random architecture (bit-string) represented as an int."""
    return list(np.random.randint(0, 2, startLength))

def mutate_arch(parent_arch, mutate_type):
    """Computes the architecture for a child of the given parent architecture."""
    length = len(parent_arch)
    child_arch = parent_arch.copy()
    if mutate_type == 2:
        position = random.randint(0, length-1)
        child_arch[position] ^= 1
    elif mutate_type == 1:
        position = random.randint(0, length)
        child_arch.insert(position, 1)
    elif mutate_type == 0:
        position = random.randint(0, length)
        element = 0
        # element = random.choice([0,2]) # 0 for MLP, 2 for ANN
        child_arch.insert(position, element)
    else:
        print('mutate type error')
    
    return child_arch