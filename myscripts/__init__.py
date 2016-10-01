import matplotlib.pyplot as plt
import numpy as np

Xgen = lambda N, M : np.random.uniform(-5,5,(N,M))

def pringle(N, M, std):
    X = Xgen(N,M)
    Y = (X[:,0]**2 - X[:,1]**2 + np.random.normal(0,std,(N,)))[...,None]    
    return X, Y

def wave(N, M, std):
    X = Xgen(N,M)
    Y = (np.cos(X[:,0]) + np.sin(X[:,1]) + np.random.normal(0,std,(N,)))[...,None]    
    return X, Y

def gaussians(N, M, mus, stds, one_hot= False):
    X, Y = [],[]
    
    K = len(mus)    
    assert len(mus) == len(stds), "Number of means and stdevs must match"
    assert N % K == 0, "{N} not divisible by number of Gaussians, {K}".format(N=N,K=K)
    
    for i, (mu, std) in enumerate(zip(mus,stds)):
        X.append(np.random.normal(mu, std, (N/K, M)))
        if one_hot:
            Y.append(
                np.repeat(np.eye(K)[i], N/K, axis= 0)
                )
        else:
            Y.append(
                np.repeat(np.array([[i]]), N/K, axis= 0)
            )
            
    X = np.row_stack(X)
    Y = np.row_stack(Y)
    return X, Y

def normalize(X, Y, normalize_outputs= False):
    ## Normalize data
    X -= X.mean(axis= 0)
    X /= X.std(axis= 0)    
    return X, Y

def permute_and_split(X, Y, n_total= 0, n_val= 0):
    ## permute data
    p = np.random.permutation(n_total)
    X, Y = X[p], Y[p]
    
    ## Split data
    X_t, Y_t = X[:n_total-n_val], Y[:n_total-n_val]
    X_v, Y_v = X[-n_val:], Y[-n_val:]
    
    return X_t, Y_t, X_v, Y_v

class Visualizer(object):
    def __init__(self):
        self.tloss = []
        self.vloss = []
        
    def append_data(self, loss, params, itr, elapsed, val_loss= None, verbose= True):
        if verbose:
            print("Epoch: {} == Loss: {} == Val Loss: {}".format(itr,loss,val_loss))
        self.tloss.append(loss)
        self.vloss.append(val_loss)
        
    def plot(self):
        f, ax = plt.subplots(1,1)
        ax.plot(self.tloss,'b')
        ax.plot(self.vloss,'r')
        plt.show()