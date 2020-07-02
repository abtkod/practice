import numpy as np
from functools import reduce

"""
Build a fully connected neural network from scratch.
**Reminder**: The general methodology to build a Neural Network is to:
    1. Define the neural network structure ( # of input units,  # of hidden units, etc). 
    2. Initialize the model's parameters
    3. Loop:
        - Implement forward propagation
        - Compute loss
        - Implement backward propagation to get the gradients
        - Update parameters (gradient descent)
"""

class NN(object):
    
    # activation functions with derivatives
    IDENTITY = lambda z, derivative=False: z if not derivative else np.ones(z.shape)
    RELU = lambda z, derivative=False: np.maximum(0, z) if not derivative else np.where(z<0, 0, 1)

    def SIGMOID(z, derivative=False):        
        if not derivative:
            r = 1/(1 + np.exp(-z))
        else:
            r = np.exp(-z)/(1+np.exp(-z))**2
        r[r == 0.0] = np.nextafter(0, 1)
        r[r == 1.0] = np.nextafter(1, -1)
        return r
    
    def TANH(z, derivative=False):        
        if not derivative:
            r = np.tanh(z)
        else:
            r = 1 - np.tanh(z)**2
        r[r == 0.0] = np.nextafter(0, 1)
        r[r == 1.0] = np.nextafter(1, -1)
        return r        
    
    # logloss for classification
    LOGLOSS = lambda yhat, y, derivative=False: (-1) * (y * np.log(yhat) + (1-y) * np.log(1-yhat)) if not derivative else\
                                            (-1)*y/yhat + (1-y)/(1-yhat)
    
    SQUARELOSS = lambda yhat, y, derivative=False: (yhat-y)**2 if not derivative else 2 * (yhat-y)
        
            
    _COST_FUNC = lambda yhat, y, loss_func, regularization_value: 1/y.shape[1] * np.sum(loss_func(yhat, y), axis=1) + regularization_value
    
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
                return kw['lambd']/kw['m']/2 * reduce((lambda x,y: x+y), map(lambda W: np.linalg.norm(W, ord='fro')**2, kw['W']))        

    def __init__(self, units_per_layer, activation_functions, loss_func, regularization_type='L2'):
        from inspect import signature
        assert (callable(loss_func)), 'loss_func is not callable'        
        assert (len(signature(loss_func).parameters) > 2), 'insufficient parameters for loss_func'
        assert ('derivative' in signature(loss_func).parameters), "loss_func must have a 'derivative' parameter"
        assert len(units_per_layer) == len(activation_functions), 'layer mismatch'        
        for i, af in enumerate(activation_functions):
            assert (callable(af)), f'entry at index {i} of activation_functions is not callable'
            func_sig = signature(af)
            assert (len(func_sig.parameters) > 1), f'insufficient parameters for activation function at index: {i}'
            assert ('derivative' in func_sig.parameters), f"activation function at index {i} does not have a 'derivative' parameter"
        
        self.loss_func = loss_func
        self._regularizer = self.Regularization(regularization_type)
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
        
    def train(self, X, Y, alpha, max_iterations, lambd=None, dropout:list=None, 
              terminate_on_cost_change=0.0000001, print_cost_every=False)->np.array:                
        '''Dropout is a list of floats. Each number tells the percentage of neurons to be ignored in each layer'''
        
        L = len(self.units_per_layer) # input is not counted in the number of layers
        
        assert X.shape[1] == Y.shape[1], 'invalid input'
        assert 0<=alpha and (lambd is None or 0<=lambd), 'invalid hyperparameters'
        if dropout is None: # dropout = 1 - keep-prob
            dropout = [False for i in range(L+1)] # L+1: input layer usually has no dropout (keep-prob == 1.0)
        assert len(dropout) == L+1 and reduce((lambda x,y: x and y), map(lambda x: 0.0 <= x < 1.0, dropout)), 'invalid dropout list'
        
        np.random.seed(1)
        m = X.shape[1] # number of examples
        n = [X.shape[0]] + self.units_per_layer # n[0] is the size of the input layer
        G = [None] + self.activation_functions # different functions across layers        
        
        A = [X] + [np.zeros((n[l], m)) for l in range(1, L+1)] # for layer l we have n[l] activations per example
        W = [None] + [np.random.randn(n[l], n[l-1])/np.sqrt(n[l-1]) for l in range(1, L+1)] # for each layer w.T= W[l]: (n[l], n[l-1])
        b = [None] + [np.zeros((n[l], 1)) for l in range(1, L+1)] # each unit has only one b but n[l-1] ws

        Z = [None] + [np.zeros((n[l], m)) for l in range(1, L+1)]
        dZ = [None] + [np.zeros((n[l], m)) for l in range(1, L+1)]
        dW = [None] + [np.zeros((n[l], n[l-1])) for l in range(1, L+1)]
        db = [None] + [np.zeros((n[l], 1)) for l in range(1, L+1)]
        
        cost = float("inf")
        for i in range(max_iterations):
            
            if dropout[0]:
                D = np.random.rand(X.shape[0], X.shape[1]) > dropout[0]
                A[0] = np.multiply(A[0], D) / (1-dropout[0])
            else:
                A[0] = X
            
            # forward propagation from layer 1 to layer L
            for l in range(1, L+1):                
                Z[l] = np.dot(W[l], A[l-1]) + b[l]                
                A[l] = G[l](Z[l]) # applying activation function for layer l on Z[l]                                
                
                if dropout[l]:
                    D = np.random.rand(A[l].shape[0], A[l].shape[1]) > dropout[l]
                    A[l] = np.multiply(A[l], D) / (1-dropout[l])
                        
            # backward propagation from layer L to layer 1    
            for l in range(L, 0, -1): # from L <= l <= 1         
                if l == L:
                    # when loss_func is logloss and last layer's activation function is sigmoid: dZ[L] = A[L] - Y
                    dZ[L] = self.loss_func(A[L], Y, derivative=True) * G[L](Z[L], derivative=True)
                else:
                    dZ[l] = np.dot(W[l+1].T, dZ[l+1]) * G[l](Z[l], derivative=True) # dA[l]= np.dot(W[l+1].T, dZ[l+1])
                dW[l] = 1/m * np.dot(dZ[l], A[l-1].T)
                db[l] = 1/m * np.sum(dZ[l], axis=1, keepdims=True)

                wdec = 1.0 if lambd is None else self._regularizer.weight_decay(**{'alpha':alpha, 'lambd':lambd, 'm':m})
                W[l] = wdec * W[l] - alpha * dW[l] # (1 - alpha*lambd/m) is the weight decay coming from L2 regularization
                b[l] = b[l] - alpha * db[l]

            reg_val = 0.0 if lambd is None else self._regularizer.cost_adjustment(**{'lambd':lambd, 'm':m, 'W':W[1:]})
            new_cost = NN._COST_FUNC(yhat=A[L], y=Y, loss_func=self.loss_func, regularization_value=reg_val)
            if 0 < cost - new_cost < terminate_on_cost_change:
                cost = new_cost
                break
            cost = new_cost
            if print_cost_every and i % print_cost_every == 0:
                print('iteration: {}, cost: {}'.format(i, cost))
            
        print('iteration: {}, cost: {}'.format(i, cost))
        self._W = W
        self._b = b

    def predict_proba(self, X):
        assert X.shape[0] == self._W[1].shape[1], 'invalid input'        
        A = X
        G = [None] + self.activation_functions        
        for l in range(1, len(self._W)):
            w = self._W[l]
            b = self._b[l]
            Z = np.dot(w, A) + b
            A = G[l](Z)
        return A
    
    def predict(self, X, classification=True, threshold=0.5):
        if classification:
            yhat = self.predict_proba(X)
            return np.where(yhat>=threshold, 1, 0)
        else:
            return self.predict_proba(X)
    

import unittest
class Test(unittest.TestCase):    
    
    def test_linear_regression(self):
        print('-'*20)
        print('testing simple linear regression model...')
                
        W = np.array([3, 5]).reshape(1,2)
        b = np.array([-4])
        
        np.random.seed(1)
        X_train = np.random.uniform(low=-1, high=1, size=(2,100)) # random points on a plane (-1, 1)
        noise = 0.1 * np.random.randn(1, X_train.shape[1])
        y_train = b + np.dot(W, X_train) + noise

        X_test = np.random.uniform(low=-1, high=1, size=(2,10)) # random points on a plane (-1, 1)
        noise = 0.1 * np.random.randn(1, X_test.shape[1])
        y_test = b + np.dot(W, X_test) + noise
        
        nn = NN(units_per_layer=[1], activation_functions=[NN.IDENTITY], loss_func=NN.SQUARELOSS)
        nn.train(X_train, y_train, alpha=0.5, max_iterations=1000, print_cost_every=100)
        y_pred = nn.predict(X_test, classification=False)
        
        self.assertTrue((nn.W[0].round(0) == W).all() and nn.b[0].round(0) == b)
    
    def test_binary_logistic_regression(self):
        print('-'*20)
        print('testing binary logistic regression model...')
        
        def in_sphere(X, radius, center):
            return np.where(np.sum((X - center)**2, axis=0, keepdims=True) < radius**2, 1, 0)
        
        np.random.seed(1)
        X_train = np.random.uniform(low=-2, high=2, size=(3,10000)) # random points in a cube with volume = 64
        y_train = in_sphere(X_train, 1.0, 0.0)        
        X_test = np.random.uniform(low=-2, high=2, size=(3,1000))    
        y_test = in_sphere(X_test, 1.0, 0.0)
        
        nn = NN(units_per_layer=[4,1], activation_functions=[NN.RELU, NN.SIGMOID], loss_func=NN.LOGLOSS)
        nn.train(X_train, y_train, alpha=0.5, max_iterations=1000, print_cost_every=100)
        y_pred = nn.predict(X_test)
        acc = np.sum(y_pred == y_test) / y_test.shape[1]
        
        self.assertTrue(acc > 0.97)
        
    def test_XOR(self):        
        print('-'*20)
        print('testing an XOR classifier...')
        
        def XOR(X):
            '''
            This function requires exponential(2^(n-1)) units if not represented in deep layers.
            '''
            from functools import reduce
            xor_func = lambda vec: reduce((lambda x,y: bool(x)!= bool(y)), vec)
            return np.apply_along_axis(xor_func, axis=0, arr=X).reshape(1, X.shape[1])
        
        X_train = np.random.randint(low=0, high=2, size=(8, 1000))
        y_train = XOR(X_train)                
        X_test = np.random.randint(low=0, high=2, size=(8, 100))
        y_test = XOR(X_test)
        
        nn = NN([13, 13, 13, 1], [NN.RELU, NN.RELU, NN.RELU, NN.SIGMOID], loss_func=NN.LOGLOSS)
        nn.train(X_train, y_train, alpha=0.01, max_iterations=15000, print_cost_every=500)
        y_pred = nn.predict(X_test)
        acc = np.sum(y_pred == y_test) / y_test.shape[1]        
        self.assertTrue(acc > 0.8)
        

if __name__ == '__main__':
        unittest.main()