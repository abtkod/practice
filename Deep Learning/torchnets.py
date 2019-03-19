import torch
from torch import nn, optim
from torch.autograd import Variable

# pytorch: y = x A.T +b
class FullyConnectedNetwork(nn.Module): # It is mandatory to inherit from `nn.Module` when you're creating a class for your network.
    # activation classes
    SIGMOID = nn.Sigmoid()
    TANH = nn.Tanh()
    RELU = nn.ReLU()
    SOFTMAX = nn.Softmax(dim=1) # Setting `dim=1` in `nn.Softmax(dim=1)` calculates softmax across the columns
    LOGSOFTMAX = nn.LogSoftmax(dim=1)
    
    # loss functions
    CROSSENTROPYLOSS = nn.CrossEntropyLoss()    
    NLLLOSS = nn.NLLLoss()
    
    # Optimizer classes
    ADAM = optim.Adam
    SGD = optim.SGD
    
    def __init__(self, in_features, units_per_layer, activation_functions, loss_function, optimizer_class):
        assert len(units_per_layer) == len(activation_functions), 'layer mismatch'                 
        
        super().__init__()
                
        units = [in_features] + units_per_layer
        activations = [None] + activation_functions
        self.layers = len(units) - 1
        for l in range(1, self.layers+1):
            setattr(self, 'fc%d'% l, nn.Linear(units[l-1], units[l]))
            setattr(self, 'ac%d'% l, activations[l])
        self.criterion = loss_function
        self.Optimizer = optimizer_class
        
    def forward(self, x):
        x = x.view(x.shape[0], -1)
        for l in range(1, self.layers+1):
            fc = getattr(self, 'fc%d'% l)
            ac = getattr(self, 'ac%d'% l)
            x = fc(x)
            x = ac(x)
        return x
        
    
    def train(self, trainset, lr, epochs, batch_size=64):
        trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True)
        optimizer = self.Optimizer(self.parameters(), lr=lr)
        
        for e in range(epochs):
            running_loss = 0
            for samples, labels in trainloader:                
                samples, labels = Variable(samples), Variable(labels)
                
                out = self.forward(samples)
                loss = self.criterion(out, labels)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                running_loss += loss[0]
            else:                
                print(f'Epoch {e}. Training loss: {running_loss/len(trainloader)}')
    
    def weight(self, layer):
        assert 0 < layer <= self.layers, 'invalid layer'
        linear = getattr(self, 'fc%d'% layer)
        return linear.weight.data
    
    def bias(self, layer):
        assert 0 < layer <= self.layers, 'invalid layer'
        linear = getattr(self, 'fc%d'% layer)
        return linear.bias.data
