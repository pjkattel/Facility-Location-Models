



import numpy as np
import pandas as pd
import math 
from data_pre processing import *
from Optimization_models import *

import matplotlib.pyplot as plt


plt.style.use('seaborn-whitegrid')

#%%


#%%
# file locations ########
Hospitals ='..\Final data_present\Data of Present Hospitals.csv'
cell_tower = '..\Final data_present\CellTowers.csv'
Power_station = '..\Final data_present\power_plants.csv'
fire_station = '..\Final data_present\stations.csv'
police_station = '..\Final data_present\police_station.csv'
population = '..\Final data_present\population.csv'
cost = '..\Final data_present\cost_of_candidate.csv'
fordelta = '..\Final data_present\delta.csv'

#%%
# ---- Read the data ---#####

C = read_file(Hospitals)   # CI Dataframe (df)
C_pre = C[0:54]           # selecting the already established CI 
D = read_file(population)   # Demand location df
ss1 = read_file(Power_station)   # Supporting stations 1 df 
ss2 = read_file(cell_tower)      # Supporting stations 1 df 
ss3 = read_file(fire_station)   # Supporting stations 1 df 
ss4 = read_file(police_station)   # Supporting stations 1 df 
costdf = read_file(cost)        # Supporting stations 1 df 
deltadf = read_file(fordelta)     # Supporting stations 1 df 

#%%  ### --Find the distance --####

##----find the distance between the candidate facility and the supporting stations 

####----find_distance( Critcal_Infrastructure df, Supporting_stations df , per_unit_distance_rate (pdr), desired Ranking , Layer specified )-----

d_C_ss1 = find_distance(C,ss1,1.5,3,'l1')      #df with pdr between CI and SS1
d_C_ss2 = find_distance(C,ss2,1.5,3,'l2')       #df with pdr between CI and SS2
d_C_ss3 = find_distance(C,ss3,1.0,3,'l3')       #df with pdr between CI and SS3
d_C_ss4 = find_distance(C,ss4,1.0,3,'l4')        #df with pdr between CI and SS4

##### Stacking the supporting stations data frame to from a single df of all supporting stations and their pdr to CI 
d_C_SS= pd.concat([d_C_ss1,d_C_ss2,d_C_ss3,d_C_ss4],axis =0)       

######  -find the distance and transportation cost between the candidate facility and Demand Locations 
#given rate for transportation 
rate_per_mile = 0.0057485
d_C_D = distance_C_D(C,D, rate_per_mile)      ###distance_C_D(CI df , Demand df , rate_per_mile)


#%%
##----filtering the CI-demand pairs with fixed given radius:
     
###maximal_covering_out(DataFrame_with_distance, Max_Covering_radius) ---- This does not include CI-Demand pair with in the Given radius
max_cov1 = maximal_covering_out(d_C_D,17)
max_cov1['cost']= 0  #assign the lower weight (values) to connect 


###maximal_covering_in(DataFrame_with_distance, Max_Covering_radius) ---- This includes CI-Demand pair with in the Given radius

max_cov2 = maximal_covering_in(d_C_D,17)
max_cov2['cost']= 400 #assign the higher weight (values) to connect

###--- Combine both in and out dataframes
max_covdf = pd.concat([max_cov1,max_cov2],axis = 0) 


#%%   Creating the Input files #############

#%% Creating the list  :
     
#list of Demand 
demand = D['Name'].values.tolist()

#list of Candidate
candidate = C['Code'].values.tolist()

#list of existing candidate
candidate_pre = candidate[0:54]

#list of supporting station layer 
ss_layer = ['l1','l2','l3', 'l4']

#list of rank
rank = [1,2,3]

#%%   #####---- Creating Dictionary----------------

distance = dictionary_distance(d_C_D)  #Demand-CI distance dictionary ( CI-demand distace Df)

cjmr3 = dictionary_cjmr(d_C_SS) #Demand-CI distance dictionary ( CI-SS distace Df)

delta = dictionary_delta(deltadf) # Delta value dictionary (delta df )

max_cov = dictionary_setcov(max_covdf)  # max covering dictionary (max cov df)

demand_size = cj(D,'Name','Bedsize')   # demand size dictionary (demand data frame)

fixed_cost = cj(costdf,'Candidate','Fixed cost')   ##fixed cost for candidate facility

var_cost = cj(costdf,'Candidate','Variable cost')   ## var_cost for capacity increment

pre_cap = pre_capacity(C)   # acpacity of the existing candidate facility

## Probability of faiure of supporting station layers 
prob = {
       "l1":0.3,"l2":0.3, "l3":0.3,"l4":0.3  
       }

#%%  numeric values input 
# penalty cost
pi = 50
#minimum capacity 
cmin = 30
#maximum capacity
cmax = 350

#time horizon index
n = 50




#%%
# SET Covering  to located the CI based in RFLP-SS  

writer = pd.ExcelWriter('scenario_S2.xlsx', engine='xlsxwriter')

facility_located,demand_allocation,facility_capacity,add_capacity,O_cost,P_cost,E_cost,VE_cost,Tran_cost,Totalcost = dependent_model_reg(demand,candidate,candidate_pre,pre_cap,ss_layer,rank,fixed_cost,var_cost,demand_size,distance,prob,cjmr3,delta,cmin, cmax,pi,n)


facility_located.to_excel(writer,sheet_name = 'facility_located')
demand_allocation.to_excel(writer,sheet_name = 'demand_allocation')
facility_capacity.to_excel(writer, sheet_name = 'facility_capacity')
add_capacity.to_excel(writer, sheet_name = 'add_capacity')
costs = {'O_cost': O_cost,
          'Pcost':P_cost,
          'E_cost':E_cost,
          'VE_cost':VE_cost,
          'Tran_cost':Tran_cost,
          'Totalcost':Totalcost
          }



costs2 =pd.DataFrame.from_dict(costs,orient='index')
costs2.to_excel(writer,sheet_name = 'costs2')