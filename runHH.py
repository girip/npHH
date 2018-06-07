from npHH import *

length_simulation = 100 # in msec
time_step = 0.02

# setup network
no_neuron_types=2
no_neurons=10 # need to map the number of neurons to type

no_synapse_types=1
connectivity_matrix =gen_connectivity(no_neurons,0.8) 

no_synapses=[int(np.sum(connectivity_matrix))] ## TODO for all types of connections

execfile("/Volumes/Dala/research-dala/npHH/initialize_variables.py")

T=0
ti=0
Vout=np.zeros(((length_simulation/time_step)))
#initialize_variables
while (ti < length_simulation/time_step):
 for step in range(0,4):
  for si in range(0,np.sum(no_synapses)):  # to parallelize this part 
   # dSrkv[Ssi_rk[si]:Ssi_rk[si+1]], Sov[Ssi_ov[si]:Ssi_ov[si+1]] = synapse_calc(Srkv[Ssi_rk[si]:Ssi_rk[si+1]], dSrkv[Ssi_rk[si]:Ssi_rk[si+1]], Sov[Ssi_ov[si]:Ssi_ov[si+1]], Is[si], Sspike[si], Stypes[si])
   Sov[Ssi_ov[si]:Ssi_ov[si+1]] = synapse_calc_ov(Sov[Ssi_ov[si]:Ssi_ov[si+1]], Is[si], Sspike[si], Stypes[si])

  gather_synaptic_currents(Is, Iv, connectivity_matrix)
  for ni in range(0,np.sum(no_neurons)):
   dNrkv[Nsi_rk[ni]:Nsi_rk[ni+1]], Nov[Nsi_ov[ni]:Nsi_ov[ni+1]] = neuron_calc(Nrkv[Nsi_rk[ni]:Nsi_rk[ni+1]], dNrkv[Nsi_rk[ni]:Nsi_rk[ni+1]], Nov[Nsi_ov[ni]:Nsi_ov[ni+1]], Iv[ni], Ntypes[ni])
  rk_steps(Nrkv, dNrkv, Nrk_tmp, T, step) 
 Vout[ti]=Nrkv[0]
 ti=ti+1
 #update_spike_status(Nv,Nspike)
 #distribute_spike_status(Nspike, connectivity, Sspike)

#@tags
# 1: modify when more than 1 synapse type

while (ti < length_simulation/time_step):
 for step in range(0,4):
  for si in range(0,np.sum(no_synapses)): # need to be vectorized
   
