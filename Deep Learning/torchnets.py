import torch
from torch import nn, optim
from torch.autograd import Variable
from collections import OrderedDict

# pytorch: y = x A.T +b
class FullyConnectedNetwork(object):
    
    # activation functions
    sigmoid = nn.Sigmoid()
    tanh = nn.Tanh()
    relu = nn.ReLU()
    soft_max = nn.Softmax(dim=1) # Setting `dim=1` in `nn.Softmax(dim=1)` calculates softmax across the columns
    log_soft_max = nn.LogSoftmax(dim=1)
    
    # loss functions
    cross_entropy_loss = nn.CrossEntropyLoss()    
    nl_loss = nn.NLLLoss()
    
    # Optimizer classes
    Adam = optim.Adam
    Sgd = optim.SGD
    
    def __init__(self, loss_function, optimizer, model=None, input_size=None, layer_sizes=None, activation_functions=None):        
        assert (isinstance(model, nn.Module) or 
                all(arg is not None for arg in [input_size, layer_sizes, activation_functions])), \
            'Invalid network initialization'
                
        self._criterion = loss_function
        self._Optimizer = optimizer
        self._model = None        
        
        if isinstance(model, nn.Module):            
            self._model = model
        else:
            assert len(layer_sizes) == len(activation_functions), 'layer_sizes/activation_functions mismatch'
            units = [input_size] + layer_sizes
            activations = [None] + activation_functions
            layers = OrderedDict()
            for l in range(1, len(units)):
                layers['fc%d'% l] = nn.Linear(units[l-1], units[l])
                layers['ac%d'% l] = activations[l]
            self._model = nn.Sequential(layers)        
    
    @property
    def model(self):
        return self._model
    
    def __repr__(self):                
        rp = f'FullyConnectedNetwork(\nOptimizer:{self._Optimizer.__name__}\nCriterion:{repr(self._criterion)[:-3]}\nLayers:'
        rp += repr(self._model).replace('Sequential(', '')
        return rp       
    
    def train(self, trainset, testset, lr, epochs, batch_size=64):        
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)
        testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=True)
        optimizer = self._Optimizer(self._model.parameters(), lr=lr)
        
        for e in range(epochs):
            running_loss = 0
            for samples, labels in trainloader:
                samples = samples.view(samples.shape[0], -1)                
                
                logits = self._model(samples)
                loss = self._criterion(logits, labels)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                running_loss += loss.data
            else:
                # inference
                test_accuracy = 0
                test_loss = 0
                with torch.no_grad():
                    for samples, labels in testloader:
                        samples = samples.view(samples.shape[0], -1)
                        logits = self._model(samples)
                        
                        test_loss += self._criterion(logits, labels)
                        top_logit, top_class = logits.topk(1, dim=1)
                        equals = top_class == labels.view(*top_class.shape)
                        test_accuracy += torch.mean(equals.type(torch.FloatTensor))     
                    
                print(f'Epoch {e}.', 
                      f'Training loss: {running_loss/len(trainloader) :.3f},',
                      f'Test loss: {test_loss/len(testloader) :.3f},',
                      f'Test Accuracy: {test_accuracy.item()/len(testloader)*100 :.2f}%')