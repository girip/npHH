
#----- Create vectors for variables
Nrk_var = np.array([1]) # number of RK variables per neuron type
Srk_var = np.array([0]) # number of RK variables per synapse type

No_var = np.array([0]) # number of other variables per neuron
So_var = np.array([1]) # number of other variables per synapse

Nrkv = np.zeros((np.sum(no_neurons*Nrk_var))) # vector of all the RK neuron variables
Srkv = np.zeros((np.sum(no_synapses*Srk_var)))

neuron_rk_vars=np.sum(no_neurons*Nrk_var)
synapse_rk_vars=np.sum(no_synapses*Srk_var)

# derivatives
dNrkv = np.zeros((np.sum(no_neurons*Nrk_var))) # vector of all the RK neuron variables
dSrkv = np.zeros((np.sum(no_synapses*Srk_var)))
# intermediate Rk variable
Nrk_tmp = np.zeros((2,neuron_rk_vars))
Srk_tmp = np.zeros((2,synapse_rk_vars))

no_ov_vars=np.sum(no_neurons*No_var)+np.sum(no_synapses*So_var)
Nov = np.zeros((np.sum(no_neurons*No_var))) # vector of all the RK neuron variables
Sov = np.zeros((np.sum(no_synapses*So_var)))

#----- initialize variables -----
# Nrkv, Srkv, ...
Iv = np.zeros((np.sum(no_neurons))) # vector with the input current to each neuron
Nspike = np.zeros((np.sum(no_neurons)), dtype=bool) # state of neuron -- spiked
Sspike = np.zeros((np.sum(no_synapses)), dtype=bool)

# ----- get arrays for neuron/synapse types and start index -----
Is = np.zeros((np.sum(no_synapses))) # vector with the input current to each neuron
Stypes = np.zeros((np.sum(no_synapses)))  #tag:1 ## for now use one type --- TODO modify this based on connections
Ntypes = np.zeros((np.sum(no_neurons)))
Ntypes[0:no_neurons] = 0

# for nt in range(1,no_neuron_types):
#  Ntypes[np.sum(no_neurons[0:nt]):np.sum(no_neurons[0:nt])+no_neurons[nt]]=nt

#------- Not vectorized, but parallelizable -----

#---- start index for neurons/synapse
Nsi_rk = np.zeros((1+np.sum(no_neurons)), dtype=int) 
Ssi_rk = np.zeros((1+np.sum(no_synapses)), dtype=int)  #tag:1

Nsi_ov = np.zeros((1+np.sum(no_neurons)), dtype=int) 
Ssi_ov = np.zeros((1+np.sum(no_synapses)), dtype=int)  #tag:1

running_nrki=0
running_novi=0
for nt in range(0,no_neuron_types):
 for ni in range(0,no_neurons[nt]):
  Nsi_rk[np.sum(no_neurons[0:nt])+ni]=running_nrki
  running_nrki=running_nrki+Nrk_var[nt]  
  Nsi_ov[np.sum(no_neurons[0:nt])+ni]=running_novi
  running_novi=running_novi+No_var[nt]

Nsi_rk[int(np.sum(no_neurons))]=np.sum(no_neurons*Nrk_var)
Nsi_ov[int(np.sum(no_neurons))]=np.sum(no_neurons*No_var)

running_srki=0
running_sovi=0
for st in range(0,no_synapse_types):
 for si in range(0,no_synapses[st]):
  Ssi_rk[int(np.sum(no_synapses[0:st]))+si]=running_srki
  running_srki=running_srki+int(Srk_var[st])
  Ssi_ov[np.sum(no_synapses[0:st])+si]=running_sovi
  running_sovi=running_sovi+So_var[st]

Ssi_rk[no_synapses]=np.sum(no_synapses*Srk_var) #tag:1
Ssi_ov[no_synapses]=np.sum(no_synapses*So_var) #tag:1
