# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 00:07:18 2018

@author: pj417216
"""

####python implementation of model
import pandas as pd
from gurobipy import *

#The capacity of the candidate facility are relaxed in this model, the capacity of existing candidate facility can be increased to cmax if required##
def dependent_model_reg(demand,candidate,candidate_pre,pre_cap,ss_layer,rank,fixed_cost,var_cost,demand_size,distance,prob,cjmr3,delta,cmin, cmax,pi,n):
     
     #initializing the model
     m = Model()
     m.update()
     

     #assigning some "default values" the model specific
     pop = demand_size
     bigN = 1000000                   
     rmax = len(rank)

     #variable assignment

     loc = m.addVars(candidate,name = "x", vtype = GRB.BINARY)  #facility located 
     sup = m.addVars(demand, candidate, name = "y")
     cap = m.addVars(candidate, name ="k")
     addcap = m.addVars(candidate, name ="w")
     
     
     #Objective function breakdown    
     #operating cost 
     obj1 = quicksum((prob[m]**(int(r)-1))*(1-prob[m])*cjmr3[(j,m,r)]*n*sup[i,j] for r in rank for m in ss_layer for j in candidate for i in demand)
     
     #transportation cost
     obj2 = quicksum(distance[i,j] *n* sup[i,j] for j in candidate for i in demand)
     
     #Fixed_establishment cost
     obj3 = quicksum(loc[j]*fixed_cost[j] for j in candidate)
     
     #var_establishment cost
     obj4 = quicksum(addcap[j]*var_cost[j] for j in candidate)
     
     #Penalty cost
     obj5 = quicksum((prob[m]**rmax) *n* (1-delta[j,m])* sup[i,j] * pi for m in ss_layer for j in candidate for i in demand)
     
     #Adding up all the parts of objective functions
     obj = obj1 +obj2 +obj3 + obj4 + obj5
          
     
     #constraints
             
     #supply constraints stating supply is only possible from established facility
     for i in demand:
          for j in candidate:
               m.addConstr(sup[i,j] <= bigN * loc[j])
     
     
     #Demand fulfillment constraints
     for i in demand:
          m.addConstr(quicksum(sup[i,j] for j in candidate) >= pop[i])

     
     #supply limit constraints 
     for j in candidate:
          m.addConstr(quicksum(sup[i,j] for i in demand) <= cap[j])

        
     
     #value for additional capacity constraints
     for j in candidate:
          if j in candidate_pre:
               m.addConstr(cap[j] - pre_cap[j] <= addcap[j])               
          else:
               m.addConstr(cap[j]- cmin <= addcap[j])
     
     
     #max capacity constraints
     for j in candidate:
          m.addConstr(cap[j] <= cmax)
     
     
     #non negativity constraints
     for i in demand:
          for j in candidate:
               m.addConstr(sup[i,j] >= 0)
     
     for j in candidate:
          m.addConstr(loc[j] >= 0)
     
     for j in candidate:
          m.addConstr(cap[j] >= 0)
     
     for j in candidate:
          m.addConstr(addcap[j] >= 0)

     
     #set the objective function
     m.setObjective(obj, GRB.MINIMIZE)
              
     
     #optimize the objective function wrt constraints defined
     m.optimize()
     #printSolution()
     Opt = m.getObjective()
     
     
     
     if m.status == GRB.Status.OPTIMAL:
          #print("\nTotalcost : %s" %(Opt.getValue()))
          Totalcost = Opt.getValue()
          #print("\nLocated Facility:")
          locx = m.getAttr('x',loc)
          supx = m.getAttr('x',sup)
          addcapx = m.getAttr('x',addcap)
          capx = m.getAttr('x',cap)
          #print(locx)
          #print(supx)
          fac = []
          allo =[]
          cap1 = []
          adcap1 =[]
          for i in candidate:
               if loc[i].x > 0.0001:
                    #print("%s" %(i))
                    fac.append(i)
          facility_located = pd.DataFrame(fac)
          #print("\nSupply :")
          for i in demand:
               for j in candidate:
                    if sup[i,j].x > 0.0001:
                         #print("supply from %s to %s:%s" %(j,i,supx[i,j]))
                         ad = [j,i,supx[i,j]]
                         allo.append(ad)
          demand_allocation = pd.DataFrame(allo)
          
          for i in candidate:
               if cap[i].x > 0.0001:
                    #print("%s" %(i))
                    cap2 = [i,capx[i]]
                    cap1.append(cap2)
          facility_capacity = pd.DataFrame(cap1)
          
          for i in candidate:
               if addcap[i].x > 0.0001:
                    #print("%s" %(i))
                    cap3 = [i,addcapx[i]]
                    adcap1.append(cap3)
          add_capacity = pd.DataFrame(adcap1)
          
     else:
          print("no solution")
               
     
     #get the individual cost component
     if m.status == GRB.Status.OPTIMAL:
          supx = m.getAttr('x',sup)
          locx = m.getAttr('x',loc)
          capx = m.getAttr('x',cap)
          locx = m.getAttr('x',loc)
          
          O_cost = quicksum((prob[m]**(int(r)-1))*(1-prob[m])*cjmr3[(j,m,r)]*(n)*supx[i,j] for r in rank for m in ss_layer for j in candidate for i in demand).getValue()
          P_cost= quicksum((prob[m]**rmax) * (1-delta[j,m])*(n)* supx[i,j] * pi for m in ss_layer for j in candidate for i in demand).getValue()
          E_cost = quicksum(loc[j]*fixed_cost[j] for j in candidate).getValue()
          VE_cost = quicksum(addcap[j]*var_cost[j] for j in candidate).getValue()
          Tran_cost = quicksum(distance[i,j] *(n)* sup[i,j] for j in candidate for i in demand).getValue()
          Totalcost = Opt.getValue()
     
     return facility_located ,demand_allocation,facility_capacity,add_capacity,O_cost,P_cost,E_cost,VE_cost,Tran_cost,Totalcost

