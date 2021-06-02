#!/usr/bin/env python
# coding: utf-8

# # Mohammed Ashad
# # Decibels
# importing required libraries

# In[26]:


from ADRpy import atmospheres as at
from ADRpy import constraintanalysis as ca
import numpy as np
import matplotlib.pyplot as plt
from ADRpy import unitconversions as co


# In[4]:


designatm = at.Atmosphere()
print(designatm)


# In[8]:


designbrief = {'groundrun_m' : 60}
desgindefinition = {'aspectratio':9, 'bpr':1}
desginperformance = {'CDTO':0.0898, 'CLTO':0.97, 'CLmax':1.7, 'mu_R':0.08}


# In[9]:


concept = ca.AircraftConcept(designbrief,desgindefinition,desginperformance,designatm)


# Wing loading

# In[13]:


wingloadinglist_pa = np.arange(80,251,1)


# Thrust to Weight ratio

# In[14]:


twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)


# minimum thrust to weight ratio required during takeoff

# In[16]:


plt.plot(wingloadinglist_pa,twratio)
plt.ylabel("T/W")
plt.xlabel("W/S (N/m^2)")
plt.title("Minimum thrust to weight ratio required")
plt.grid(True)


# In[20]:


plt.plot(wingloadinglist_pa,liftoffspeed_mps)
plt.ylabel("CL")
plt.xlabel("W/S")
plt.title("Lift-off speed as a function of wing loading")
plt.grid(True)


# Sensitivity Analysis

# Change in ground run

# In[25]:


for groundrun_m in [20,30,40,50,60,70,80,90]:
    designbrief = {'groundrun_m' : groundrun_m}
    concept = ca.AircraftConcept(designbrief,desgindefinition,desginperformance,designatm)
    twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
    plt.plot(wingloadinglist_pa,twratio, label = str(groundrun_m)+'m')
    
legend = plt.legend(loc = 'upper left', fontsize = 'medium')
plt.ylabel("T/W")
plt.xlabel("W/S")
plt.title("Sensivity of minimum thrust to weight required for take off")
plt.grid(True)


# Change in elevation height

# In[34]:


designbreif = {'groundrun_m' : 30}

for elevation_ft in [0, 1000, 2000, 3000, 4000, 5000]:
    designbrief = {'groundrun_m' :30, 'rwyelevation_m ': co.feet2m(elevation_ft)}
    concept = ca.AircraftConcept(designbrief,desgindefinition,desginperformance,designatm)
    twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
    plt.plot(wingloadinglist_pa,twratio, label = str(elevation_ft)+'ft')
legend = plt.legend(loc = 'upper left', fontsize = 'medium')
plt.ylabel("T/W")
plt.xlabel("W/S")
plt.title("Sensivity pf minimum thrust to weight wrt to runway elevation")
plt.grid(True)
    


# In[37]:


designbreif = {'groundrun_m' : 30, 'rwyelevation_m ':0}
for tmp_offset_deg in [-20,-10,0,10,20,30,40]:
    designatm = at.Atmosphere(offset_deg = tmp_offset_deg)
    concept = ca.AircraftConcept(designbrief,desgindefinition,desginperformance,designatm)
    twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
    plt.plot(wingloadinglist_pa,twratio, label = str(elevation_ft)+'ft')
legend = plt.legend(loc = 'upper left', fontsize = 'medium')
plt.ylabel("T/W")
plt.xlabel("W/S")
plt.title("Sensivity pf minimum thrust to weight wrt to runway elevation")
plt.grid(True)


# Thrust Mapping

# Piston Engine

# In[47]:


designdefinition = {'aspectratio':9, 'bpr':-1}

etap = {'take-off' :0.6, 'climb':0.75,'cruise':0.85, 'turn':0.85, 'servceil':0.6}

designperformance = {'CDTO':0.0898, 'CLTO':0.97, 'CLmaxTo':1.7, 'mu_r':0.08, 'etaprop':etap}

designatm = at.Atmosphere()

for elevation_ft in [0,1000, 2000, 3000, 4000, 5000]:
    designbreif = {'groundrun_m' :30, 'rwyelevation_m': co.feet2m(elevation_ft)}
    
    concept = ca.AircraftConcept(designbrief, desgindefinition, desginperformance, designatm)
    
    gffactor = at.pistonpowerfactor(designatm.airdens_kgpm3(co.feet2m(elevation_ft))) 
    
    twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)
    
    pwratio= (1/gffactor)*ca.tw2pw(twratio, liftoffspeed_mps ,etap['take-off'])
    
    plt.plot(wingloadinglist_pa,pwratio,label = str(elevation_ft)+'ft')
legend = plt.legend(loc = 'upper left', fontsize = 'medium')
plt.ylabel("P/W (W/N)")
plt.xlabel("W/S")
plt.grid(True)


# In[49]:


designbreif = {'groundrun_m' :1200, 'rwyelevation_m':1000}
desgindefinition = {'aspectratio':9.3, 'bpr':3.9, 'tr':1.05}
desginperformance = {'CDTO':0.04, 'CLTO':0.9, 'CLmaxID':1.6, 'mu_R':0.02}


# Wing Loading

# In[51]:


wingloading_pa = np.arange(2000,5000,10)


# Atmosphere

# In[54]:


designatm = at.Atmosphere()
concept = ca.AircraftConcept(designbreif,desgindefinition,desginperformance,designatm)


# Thrust to weight ratio for take off

# In[55]:


twratio, liftoffspeed_mps = concept.thrusttoweight_takeoff(wingloadinglist_pa)


# In[71]:


twratio1 = concept.map2static()*twratio


# In[66]:


temp_c = designatm.airtemp_c(designbrief['rwyelevation_m'])
pressure_pa = designatm.mach(liftoffspeed_mps, designbrief['rwyelevation_m'])
mach = designatm.mach(liftoffspeed_mps, designbrief['rwyelevation_m'])
correctionvec = []

throttleratio = desgindefinition['tr']
for i, tw in enumerate(twratio):
    twratio_altcorr = at.turbofanthrustfactor(temp_c,pressure_pa,mach[i],throttleratio,"lowbpr")
    correctionvec.append(twratio_altcorr)
                          


# In[67]:


twratio2 = twratio/twratio_altcorr


# In[73]:


plt.plot(wingloadinglist_pa,twratio,label = '1')
plt.plot(wingloadinglist_pa,twratio1,label = '2')
plt.plot(wingloadinglist_pa,twratio2,label = '3')
legend = plt.legend(loc = 'upper left', fontsize = 'medium')
plt.ylabel("P/W (W/N)")
plt.xlabel("W/S")
plt.grid(True)


# In[ ]:




