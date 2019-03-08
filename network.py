import numpy as np

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
    SIGMOID = lambda z, derivative=False: 1/(1 + np.exp(-z)) if not derivative else np.exp(-z)/(1+np.exp(-z))**2
    TANH = lambda z, derivative=False: np.tanh(z) if not derivative else 1 - np.tanh(z)**2
    RELU = lambda z, derivative=False: np.where(z<=0, 0, z) if not derivative else np.where(z<=0, 0, 1)    
    
    # it may even works with multiple unit output layer
    loss = lambda yhat, y, derivative=False: (-1) * (y * np.log(yhat) + (1-y) * np.log(1-yhat)) if not derivative else\
                                            (-1)*y/yhat + (1-y)/(1-yhat)
    cost = lambda yhat, y: 1/y.shape[1] * np.sum(DeepNetwork.loss(yhat, y), axis=1)


    def __init__(self, units_per_layer, activation_functions):
        assert len(units_per_layer) == len(activation_functions), 'layer mismatch'
        self.units_per_layer = list(units_per_layer)
        self.activation_functions = list(activation_functions)
        self._W = None
        self._b = None
    
    @property
    def W(self):
        return self._W[1:]
    
    @property
    def b(self):
        return self._b[1:]
        
    def train(self, X, Y, alpha, max_iterations, terminate_on_cost_change=0.00000001, print_cost_every=100)->np.array:
        assert X.shape[1] == Y.shape[1], 'invalid input'
        
        np.random.seed(1)
        m = X.shape[1] # number of examples
        n = [X.shape[0]] + self.units_per_layer # n[0] is the size of the input layer
        G = [None] + self.activation_functions # different functions across layers
        L = len(n)-1 # actual number of layers are len(n)-1
        
        A = [X] + [np.zeros((n[l], m)) for l in range(1, L+1)] # for layer l we have n[l] activations per example
        W = [None] + [np.random.randn(n[l], n[l-1])/np.sqrt(n[l-1]) for l in range(1, L+1)] # for each layer w.T= W[l]: (n[l], n[l-1])
        b = [None] + [np.zeros((n[l], 1)) for l in range(1, L+1)] # each unit has only one b but n[l-1] ws

        Z = [None] + [np.zeros((n[l], m)) for l in range(1, L+1)]
        dZ = [None] + [np.zeros((n[l], m)) for l in range(1, L+1)]
        dW = [None] + [np.zeros((n[l], n[l-1])) for l in range(1, L+1)]
        db = [None] + [np.zeros((n[l], 1)) for l in range(1, L+1)]
        
        cost = float("inf")
        for i in range(max_iterations):

            # forward propagation from layer 1 to layer L
            for l in range(1, L+1):
                Z[l] = np.dot(W[l], A[l-1]) + b[l]
                A[l] = G[l](Z[l]) # applying activation function for layer l on Z[l]
                        
            # backward propagation from layer L to layer 1    
            for l in range(L, 0, -1): # from L <= l <= 1         
                if l == L:              
                    dZ[L] = DeepNetwork.loss(A[L], Y, derivative=True) * G[L](Z[L], derivative=True)            
                else:
                    dZ[l] = np.dot(W[l+1].T, dZ[l+1]) * G[l](Z[l], derivative=True) # dA[l]= np.dot(W[l+1].T, dZ[l+1])
                dW[l] = 1/m * np.dot(dZ[l], A[l-1].T)
                db[l] = 1/m * np.sum(dZ[l], axis=1, keepdims=True)

                W[l] = W[l] - alpha * dW[l]
                b[l] = b[l] - alpha * db[l]
            
            new_cost = DeepNetwork.cost(A[L], Y)    
            if 0 < cost - new_cost < terminate_on_cost_change:
                cost = new_cost
                break
            cost = new_cost
            if i % print_cost_every == 0:
                print('iteration: {}, cost: {}'.format(i, cost))
            
        print('iteration: {}, cost: {}'.format(i, cost))
        self._W = W
        self._b = b

    def classify(self, X):        
        assert X.shape[0] == self._W[1].shape[1], 'invalid input'
        from copy import copy
        A = X
        G = [None] + self.activation_functions        
        for l in range(1, len(self._W)):
            w = self._W[l]
            b = self._b[l]
            Z = np.dot(w, A) + b
            A = G[l](Z)
        return A
        