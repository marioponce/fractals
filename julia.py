# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 15:02:07 2020

@author: mapp2
"""


import numpy as np
import matplotlib.pyplot as plt

class julia:
    def __init__(self, pars):
        try:
            self.max_iter = pars["max_iter"]
        except:
            self.max_iter = 1
        try:
            self.res = pars["res"]
        except:
            self.res = [10, 10]
        try:
            self.r_lim = pars["r_lim"]
        except:
            self.r_lim = [-1, 1]
        try:
            self.j_lim = pars["j_lim"]
        except:
            self.j_lim = [-1, 1]
        try:
            self.c = complex(pars["C"][0], pars["C"][1])
        except:
            self.c = complex(0, 0)
        try:
            if pars["func"] == "pow2":
                self.func = self.pow2 
            elif pars["func"] == "pow3":
                self.func = self.pow3      
            elif pars["func"] == "pow4":
                self.func = self.pow4      
            elif pars["func"] == "pow5":
                self.func = self.pow5      
            elif pars["func"] == "cos":
                self.func = np.cos 
            elif pars["func"] == "sin":
                self.func = np.sin  
            elif pars["func"] == "exp":
                self.func = np.exp
            else:
                self.func = pow2 
        except:
            self.func = self.pow2 
        try:
            self.col = pars["col"]
        except:
            self.col ="jet"
            
        self.z = np.array([[complex(r,i) for r in np.linspace(self.r_lim[0],self.r_lim[1],self.res[0])] for i in np.linspace(self.j_lim[0],self.j_lim[1],self.res[1])])
        self.i = np.zeros(self.z.shape)
    
    def pow2(self,m):
        m = np.array(m)
        return list(pow(m,2))
    def pow3(self,m):
        m = np.array(m)
        return list(pow(m,3))
    def pow4(self,m):
        m = np.array(m)
        return list(pow(m,4))
    def pow5(self, m):
        m = np.array(m)
        return list(pow(m,5))

    def do_iter(self):
        i = 0
        while i < self.max_iter:
            #print(sum(sum(abs(self.z)<2)))
            #self.z = self.z**2 +self.c
            self.z[abs(self.z)<2] = self.func(self.z[abs(self.z)<2])
            self.z[abs(self.z)<2] += self.c
            i += 1
            self.i[abs(self.z)<2] = i
            
    def do_plot(self):
        fig1, (ax) = plt.subplots(1, 1)
        #ax = plt.pcolor(abs(self.i))
        #plt.clim(0, 2)
        ax.imshow(self.i, 
                  extent=(self.r_lim[0], self.r_lim[1],self.j_lim[0], self.j_lim[1]),
                  cmap = self.col)
        plt.show()

class mandelbrot(julia):
    def __init__(self, pars):
        julia.__init__(self, pars)
        self.c = np.array([[complex(r,i) for r in np.linspace(self.r_lim[0],self.r_lim[1],self.res[0])] for i in np.linspace(self.j_lim[0],self.j_lim[1],self.res[1])])
        self.z = np.array([[complex(0,0) for r in np.linspace(self.r_lim[0],self.r_lim[1],self.res[0])] for i in np.linspace(self.j_lim[0],self.j_lim[1],self.res[1])])
    def do_iter(self):
        i = 0
        while i < self.max_iter:
            #print(sum(sum(abs(self.z)<2)))
            #self.z = self.z**2 +self.c
            self.z[abs(self.z)<2] = self.func(self.z[abs(self.z)<2])
            self.z[abs(self.z)<2] += self.c[abs(self.z)<2]
            i += 1
            self.i[abs(self.z)<2] = i

class newton:
    def __init__(self, pars):
        try:
            self.coef = pars["coef"]
        except:
            self.coef = [1,1]
        try:
            self.tol = 1/(10**pars["tol"])
            self.dec = pars["tol"]
        except:
            self.tol = 1
            self.dec = 0
        try:
            self.res = pars["res"]
        except:
            self.res = [10, 10]
        try:
            self.r_lim = pars["r_lim"]
        except:
            self.r_lim = [-1, 1]
        try:
            self.j_lim = pars["j_lim"]
        except:
            self.j_lim = [-1, 1]
        try:
            self.col = pars["col"]
        except:
            self.col ="jet"
        
        #self.d_coef = [i*self.coef[i] for i in range(len(self.coef)-1,0,-1)]
        self.d_coef = np.polyder(self.coef)
        r = np.round(np.roots(self.coef), self.dec)
        self.roots = {i+1:r[i] for i in range(len(r))}
        self.z = np.array([[complex(r,i) for r in np.linspace(self.r_lim[0],self.r_lim[1],self.res[0])] for i in np.linspace(self.j_lim[0],self.j_lim[1],self.res[1])])
        self.delta = np.polyval(self.coef,self.z)/np.polyval(self.d_coef,self.z)
        self.r = np.zeros(self.z.shape)
    def do_iter(self):
        while abs(self.delta).max() > self.tol:
            self.z -= self.delta
            self.delta = np.polyval(self.coef,self.z)/np.polyval(self.d_coef,self.z)
       
        self.z = np.round(self.z,self.dec)
        for i in self.roots.keys():
            self.r[abs(self.z-self.roots[i]) <= 0] = i

    def do_plot(self):
        fig1, (ax) = plt.subplots(1, 1)
        #ax = plt.pcolor(abs(self.i))
        #plt.clim(0, 2)
        ax.imshow(self.r, 
                  extent=(self.r_lim[0], self.r_lim[1],self.j_lim[0], self.j_lim[1]),
                  cmap = self.col)
        plt.show()       
        

if __name__ == "__main__":
    # pars = {
    #     "max_iter" : 100,
    #     "res" : [1000, 1000],
    #     "r_lim" : [-1, 1],
    #     "j_lim" : [-1, 1],
    #     "C" : [0.285,-0.01],
    #     "func" : "exp2",
    #     "col" : "gist_stern"
    #     }  
    # js = julia(pars)
    # js.do_iter()
    # js.do_plot()
    # ms = mandelbrot(pars)
    # ms.do_iter()
    # ms.do_plot()
    pars ={
        "coef" : [1,0,0,-1],
        "tol" : 6,
        "res" : [1000, 1000],
        "r_lim" : [-2.5, 2.5],
        "j_lim" : [-2.5, 2.5],
        "col" : "jet"
        }
    
    ns = newton(pars)
    ns.do_iter()
    ns.do_plot()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
