from neuron_synapse_info import *
import numpy as np
import random 

def neuron_calc(Nrkv, dNrkv, Nov, Iv, neuron_type):
 if neuron_type==Neuron_Types.PY:
  dNrkv[0] = PY.gL * (PY.E_R - Nrkv[0])
# elif neuron_type==1:
 return dNrkv, Nov


# TODO: try to use classes in cython 
### Calc synaptic currents 
def synapse_calc(Srkv, dSrkv, Sov, Iv, spike, syn_type):
 if syn_type==Syn_Types.AMPA:
  if spike:
   Sov[0] = Sov[0] + AMPA.gamma
  Iv = Iv * AMPA.de
 elif syn_type==Syn_Types.GABA:
  if spike:
   Sov[0] = Sov[0] + GABA.gamma
  Iv = Iv * GABA.de
 return dSrkv, Sov


# can be cythonized
def rk_steps(y,dy,Rk,T,step):
# Rk  - 0:s, 1:yk
 I = Rk.shape[1]
 tau = 0.02
 if (step==0):
  for i in range(0, I):
   Rk[0,i] = dy[i]
   Rk[1,i] = y[i] + (tau/2.0)*dy[i] 
   T = T + tau/2.0
 elif(step==1):
  for i in range(0, I):  
   Rk[0,i] = Rk[0,i] + 2.0*dy[i] 
   Rk[1,i] = y[i] + (tau/2.0)*dy[i] 
 elif(step==2):
  for i in range(0, I):
   Rk[0,i] = Rk[0,i] + 2.0*dy[i] 
   Rk[1,i] = y[i] + tau*dy[i] 
   T = T + tau/2.0
 elif(step==3):
  for i in range(0, I):
   y[i] = y[i] + (tau/6.0)*(Rk[0,i] + dy[i])


# define connections --- for now only connections from type 0 to 0 --- TODO to use gen_network functions
def gen_connectivity(no_neurons,prob):
 connectivity_matrix=np.zeros((no_neurons,no_neurons))
 for i in range(0,no_neurons):  # from neuron
  for k in range(0,no_neurons): # to neuron
   if (random.random()>prob) and (i != k):
    connectivity_matrix[i,k]=1
 return connectivity_matrix


def gather_synaptic_currents_index(connectivity_matrix):
 inp_index_si=np.empty((connectivity_matrix.shape[0]))
 inp_index=np.empty((0))
 for ci in range(0,connectivity_matrix.shape[0]):
   inp_index=np.append(inp_index,np.where(connectivity_matrix[ci,:]==1)[0])
   inp_index_si[ci]=len(inp_index)
 return inp_index, inp_index_si


def gather_synaptic_currents_index_list(connectivity_matrix):
 inp_index=np.empty(())
 for ci in range(0,connectivity_matrix.shape[0]):
  inp_index.append(np.where(connectivity_matrix[ci,:]==1)[0])
 return inp_index

