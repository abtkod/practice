import numpy as np
import torch
from functools import reduce

"""
**Reminder**: The general methodology to build a Neural Network is to:
    1. Define the neural network structure ( # of input units,  # of hidden units, etc). 
    2. Initialize the model's parameters
    3. Loop:
        - Implement forward propagation
        - Compute loss
        - Implement backward propagation to get the gradients
        - Update parameters (gradient descent)
"""

class DeepNetwork(object):
    
    # activation functions with derivatives
    def SIGMOID(z, derivative=False):        
        if not derivative:
            r = 1/(1 + torch.exp(-z))
        else:
            r = torch.exp(-z)/(1+torch.exp(-z))**2
        r[r == 0.0] = np.nextafter(0, 1)
        r[r == 1.0] = np.nextafter(1, -1)
        return r
#     SIGMOID = lambda z, derivative=False: 1/(1 + torch.exp(-z)) if not derivative else torch.exp(-z)/(1+torch.exp(-z))**2
    TANH = lambda z, derivative=False: torch.tanh(z) if not derivative else 1 - torch.tanh(z)**2
    RELU = lambda z, derivative=False: z * (z>0).float() if not derivative else torch.ones_like(z) * (z>0).float()
                                        
    
    # it may even works with multiple unit output layer
    loss = lambda yhat, y, derivative=False: (-1) * (y * torch.log(yhat) + (1-y) * torch.log(1-yhat)) if not derivative else\
                                            (-1)*y/yhat + (1-y)/(1-yhat)
            
    cost = lambda yhat, y, regularization_value: 1/y.shape[1] * torch.sum(DeepNetwork.loss(yhat, y), dim=1) + regularization_value
    
    # regularization
    class Regularization:
        def __init__(self, kind):
            self.kind = kind
                
        def weight_decay(self, **kwargs):
            assert set(['alpha', 'lambd', 'm']).issubset(set(kwargs.keys())), 'invalid parameters'             
            if self.kind == 'L2':
                return (1 - kwargs['alpha'] * kwargs['lambd'] / kwargs['m'])
                
        def cost_adjustment(self, **kw):
            assert set(['lambd', 'm', 'W']).issubset(kw.keys()), 'invalid parameters'            
            if self.kind == 'L2':
                return kw['lambd']/kw['m']/2 * reduce((lambda x,y: x+y), map(lambda W: torch.norm(W, ord='fro')**2, kw['W']))        

    def __init__(self, units_per_layer, activation_functions, regularization_type='L2'):
        assert len(units_per_layer) == len(activation_functions), 'layer mismatch'
        self._regularizer = self.Regularization(regularization_type)
        self.units_per_layer = list(units_per_layer)
        self.activation_functions = list(activation_functions)
        self._W = None
        self._b = None
    
    @property
    def W(self):
        return self._W[1:].numpy()
    
    @property
    def b(self):
        return self._b[1:].numpy()
        
    def train(self, X, Y, alpha, max_iterations, lambd=None, dropout:list=None, 
              terminate_on_cost_change=0.0000001, print_cost_every=100)->np.array:                
        X = torch.from_numpy(X).float()
        Y = torch.from_numpy(Y).float()
        if torch.cuda.is_available():
            X, Y = X.cuda(), Y.cuda()
        L = len(self.units_per_layer) # input is not counted in the number of layers
        
        assert X.shape[1] == Y.shape[1], 'invalid input'
        assert 0<=alpha and (lambd is None or 0<=lambd), 'invalid hyperparameters'
        if dropout is None: # dropout = 1 - keep-prob
            dropout = [False for i in range(L+1)] # L+1: input layer usually has no dropout (keep-prob == 1.0)
        assert len(dropout) == L+1 and reduce((lambda x,y: x and y), map(lambda x: 0.0 <= x < 1.0, dropout)), 'invalid dropout list'
                
        torch.manual_seed(1)
        m = X.shape[1] # number of examples
        n = [X.shape[0]] + self.units_per_layer # n[0] is the size of the input layer
        G = [None] + self.activation_functions # different functions across layers        
        
        A = [X] + [torch.zeros((n[l], m)) for l in range(1, L+1)] # for layer l we have n[l] activations per example
        W = [None] + [torch.randn(n[l], n[l-1])/np.sqrt(n[l-1]) for l in range(1, L+1)] # for each layer w.T= W[l]: (n[l], n[l-1])
        b = [None] + [torch.zeros((n[l], 1)) for l in range(1, L+1)] # each unit has only one b but n[l-1] ws

        Z = [None] + [torch.zeros((n[l], m)) for l in range(1, L+1)]
        dZ = [None] + [torch.zeros((n[l], m)) for l in range(1, L+1)]
        dW = [None] + [torch.zeros((n[l], n[l-1])) for l in range(1, L+1)]
        db = [None] + [torch.zeros((n[l], 1)) for l in range(1, L+1)]
        
        if torch.cuda.is_available():
            for i in range(1, len(W)):
                A[i], W[i], b[i], Z[i], dZ[i], dW[i], db[i] = \
                A[i].cuda(), W[i].cuda(), b[i].cuda(), Z[i].cuda(), dZ[i].cuda(), dW[i].cuda(), db[i].cuda()
        
        cost = float("inf")
        for i in range(max_iterations):
            
            if dropout[0]:
                D = torch.rand(X.shape[0], X.shape[1]) > dropout[0]
                if torch.cuda.is_available():
                    D = D.cuda()
                A[0] = torch.multiply(A[0], D) / (1-dropout[0])
            else:
                A[0] = X
                
            # forward propagation from layer 1 to layer L
            for l in range(1, L+1):                
                Z[l] = torch.mm(W[l], A[l-1]) + b[l]                
                A[l] = G[l](Z[l]) # applying activation function for layer l on Z[l]                                
                
                if dropout[l]:
                    D = torch.rand(A[l].shape[0], A[l].shape[1]) > dropout[l]
                    if torch.cuda.is_available():
                        D = D.cuda()
                    A[l] = A[l] * D / (1-dropout[l])
                        
            # backward propagation from layer L to layer 1    
            for l in range(L, 0, -1): # from L <= l <= 1         
                if l == L:              
                    # dZ[L] = DeepNetwork.loss(A[L], Y, derivative=True) * G[L](Z[L], derivative=True)
                    dZ[L] = A[L] - Y
                else:                   
                    dZ[l] = torch.mm(W[l+1].transpose(0,1), dZ[l+1]) * G[l](Z[l], derivative=True) # dA[l]= torch.mm(W[l+1].T, dZ[l+1])
                dW[l] = 1/m * torch.mm(dZ[l], A[l-1].transpose(0,1))
                db[l] = 1/m * torch.sum(dZ[l], dim=1, keepdim=True)

                wdec = 1.0 if lambd is None else self._regularizer.weight_decay(**{'alpha':alpha, 'lambd':lambd, 'm':m})
                W[l] = wdec * W[l] - alpha * dW[l] # (1 - alpha*lambd/m) is the weight decay coming from L2 regularization
                b[l] = b[l] - alpha * db[l]

            reg_val = 0.0 if lambd is None else self._regularizer.cost_adjustment(**{'lambd':lambd, 'm':m, 'W':W[1:]})
            new_cost = DeepNetwork.cost(A[L], Y, regularization_value=reg_val)
            new_cost = new_cost[0]
            if 0 < cost - new_cost < terminate_on_cost_change:
                cost = new_cost
                break
            cost = new_cost
            if i % print_cost_every == 0:
                print('iteration: {}, cost: {}'.format(i, cost))
            
        print('iteration: {}, cost: {}'.format(i, cost))
        self._W = W
        self._b = b

    def classify(self, X) -> np.array:
        X = torch.from_numpy(X).float()
        if torch.cuda.is_available():
            X = X.cuda()
        assert X.shape[0] == self._W[1].shape[1], 'invalid input'
        from copy import copy
        A = X
        G = [None] + self.activation_functions        
        for l in range(1, len(self._W)):
            w = self._W[l]
            b = self._b[l]
            Z = torch.mm(w, A) + b
            A = G[l](Z)
        
        if torch.cuda.is_available():
            A = A.cpu()
        return A.numpy()
        