import sys
import time
import random
import argparse
import collections
import numpy as np
import json

import torch
import torch.utils
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.datasets as dset
import torch.backends.cudnn as cudnn

from utils import *
from train import *
from operation import *
from mutation import *

parser = argparse.ArgumentParser("cora")
parser.add_argument('--seed', type=int, default=2, help='random seed')
parser.add_argument('--gpu', type=int, default=1, help='gpu device id')
parser.add_argument('--hiddim', type=int, default=128, help='hidden dims')
parser.add_argument('--fdrop', type=float, default=0.5, help='drop for cora feature')
parser.add_argument('--drop', type=float, default=0.8, help='drop for cora layers')
parser.add_argument('--learning_rate', type=float, default=0.04, help='init cora learning rate')
parser.add_argument('--weight_decay', type=float, default=2e-4, help='weight decay')
parser.add_argument('--epochs', type=int, default=200, help='num of training epochs')
parser.add_argument('--evals', type=int, default=10, help='num of evals')
parser.add_argument('--startLength', type=int, default=4, help='num of startArch')
args = parser.parse_args()

adj, features, labels, idx_train, idx_val, idx_test = load_data(path="drive/MyDrive/GNN-NAS-Group10/data", dataset='cora')
adj = aug_normalized_adjacency(adj)
adj = sparse_mx_to_torch_sparse_tensor(adj).float().cuda()
features = features.cuda()
labels = labels.cuda()
data = adj, features, labels

idx_train = idx_train.cuda()
idx_val = idx_val.cuda()
idx_test = idx_test.cuda()
index = idx_train, idx_val, idx_test

class Model(object):
  """A class representing a model."""
  def __init__(self):
    self.arch = None
    self.val_acc = None
    self.test_acc = None
    self.num_parameters = None
    self.latency = None
    
  def __str__(self):
    """Prints a readable version of this bitstring."""
    return self.arch

def main(cycles, population_size, sample_size):
    if not torch.cuda.is_available():
        print('no gpu device available')
        sys.exit(1)
    
    """Algorithm for regularized evolution (i.e. aging evolution)."""
    population = collections.deque()
    history = []  # Not used by the algorithm, only used to report results.
    bench = {} # Stores model with performance metrics
    
    # Initialize the population with random models.
    while len(population) < population_size:
        model = Model()
        model.arch = random_architecture(args.startLength)
        model.val_acc, model.test_acc, model.num_parameters, model.latency = train_and_eval(args, model.arch, data, index)
        population.append(model)
        history.append(model)
        bench[str(model.arch)] =  {"val_acc": model.val_acc, "test_acc": model.test_acc, 
                            "num_parameters": model.num_parameters, "latency": model.latency}
        print(model.arch)
        print(model.val_acc, model.test_acc)
        print(model.num_parameters)
        print(model.latency)
    
    # Carry out evolution in cycles. Each cycle produces a model and removes another.
    while len(history) < cycles:
        # Sample randomly chosen models from the current population.
        sample = []
        while len(sample) < sample_size:
            candidate = random.choice(list(population))
            sample.append(candidate)
        
        # The parent is the best model in the sample.
        parent = max(sample, key=lambda i: i.val_acc)
        
        # Create the child model and store it.
        child = Model()
        child.arch = mutate_arch(parent.arch, np.random.randint(0, 3))
        child.val_acc, child.test_acc, child.num_parameters, child.latency = train_and_eval(args, child.arch, data, index)
        population.append(child)
        history.append(child)
        bench[str(child.arch)] =  {"val_acc": child.val_acc, "test_acc": child.test_acc, 
                            "num_parameters": child.num_parameters, "latency":child.latency}
        print(child.arch)
        print(child.val_acc, child.test_acc)
        print(child.num_parameters)
        print(child.latency)
        
        # Remove the oldest model.
        population.popleft()
    
    return history, bench

# store the search history
h, bench = main(10, 5, 3) #(500, 20, 3)
f = open("drive/MyDrive/GNN-NAS-Group10/data/cora_bench.txt", "w")
f.write(json.dumps(bench))
f.close()
