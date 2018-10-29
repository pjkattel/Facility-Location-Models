# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 20:12:53 2018

@author: pj417216
"""

def  dict3(list1, list2,list3,valuelist):
     keys= zip(list1,list2,list3)
     keys = set(keys)
     Mdict = dict(zip(keys,valuelist))
     return Mdict

def dict2(list1, list2,valuelist):
     keys= zip(list1,list2)
     #keys = set(keys)
     Mdict = dict(zip(keys,valuelist))
     return Mdict

def dict1(list1,valuelist):
     Mdict = dict(zip(list1,valuelist))
     return Mdict


def multi_dict(key, value1,value2):
     value= zip(value1,value2)
     Mdict = dict(zip(key,value))
     return Mdict


def test(data,dic):
    list1 = data[0].values.tolist()
    list3 = data[1].values.tolist()
    list2 = data[2].values.tolist()
    test_dict = dict2(list3, list1,list2)
    test2 = [] 
    for  keys in dic:
          if keys in test_dict:
            a = dic.get(keys)
            c = ','.join(keys)
            b = c +','+ str(a)
            test2.append(b)
    return test2


def dictionary_setcov(data):
     df = data
     key=lambda row:((row.Demand),(row.Candidate))
     df['Keys']=df.apply(key,axis=1)
     DICT=dict(zip(df.Keys,df.cost))
     return DICT

def dictionary_distance(data):
     df = data
     key=lambda row:((row.Demand),(row.Candidate))
     df['Keys']=df.apply(key,axis=1)
     DICT=dict(zip(df.Keys,df.Cost))
     return DICT


def dictionary_cjmr(data):
     df = data
     key=lambda row:((row.Candidate),(row.layer),(row.rank1))
     df['Keys']=df.apply(key,axis=1)
     DICT=dict(zip(df.Keys,df.per_unit_cost))
     return DICT



def dictionary_delta(data):
     df = data
     key=lambda row:((row.Candidate),(row.layer))
     df['Keys']=df.apply(key,axis=1)
     DICT=dict(zip(df.Keys,df.value))
     return DICT



def haversine(coord1: object, coord2: object):
    import math

    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    #return meters
    #km = meters / 1000.0  # output distance in kilometers

    meters = round(meters, 3)
    return meters
    #km = round(km, 3)


    #print(f"Distance: {meters} m")
    #print(f"Distance: {km} km")


#haversine([0.116773,51.510357],[-77.009003,38.889931])


def find_distance(x1,x2,costpermile,r,layer):
     

     x1df = pd.DataFrame(x1)
     x2df = pd.DataFrame(x2)

     N1 = x1df.shape[0]
     N2 = x2df.shape[0]
     dist =[]
     for i in range(N1):
          for j in range(N2):
               coord1 = x1df.iloc[i,2:4].values
               coord2 = x2df.iloc[j,2:4].values
               code1 =  x1df.iloc[i,1]
               code2 =  x2df.iloc[j,1]
               dis = haversine(coord1,coord2)
               #a ={} {} {}.format('H'+str(i) +',','P'+str(j)+',' , dis)
               #dist.append(a)
               a = code1 + ',' + code2 +',' + str(dis)
               a = a.split(",")
               dist.append(a)
               #print(dist)
     dist = np.array(dist)
     #print(dist.shape)
               
     #sorting out the top n distance from the 1 point to another
     df = pd.DataFrame(dist)
     #print(df.head())
     my_col = ["Candidate","Supporting_station","distance"]
     df.columns = my_col
     #Distance_in_Km = Series( df['distance']/1000, index = df.index)
     df['distance'] = round(pd.to_numeric(df['distance'])/1609.34,2)
     #print(df.head())
     #df['Distance_in_km'] = round(df['distance']/1000,3)
     #df['Distance_in_miles'] = round(df['distance']/1609.34,3)
     
     #df['Distance_in_miles'] = round(pd.to_numeric(df.distance)/1609.34,3)
     #darray = np.array
               
               
              
     df1 = df.sort_values(['Candidate','distance'],ascending = True).groupby('Candidate').head(r)
     #print (df1.head(20))
     lst1 = []
     for i in range(int(df1.shape[0]/r)):
          a = list(range(r))
          #a = [1,2,3]
          for j in a:
               lst=j+1
               lst1.append(lst)
     
     df1['rank1'] = lst1
     #df1['distance'] = round(pd.to_numeric(df['distance'])/1609.34,2)
     df1['layer'] = layer
     df1['per_unit_cost'] = round((df['distance']*costpermile),2)
     
     return df1


def distance_C_D(Candidate,Demand, rate_per_mile):
     

     x1df = pd.DataFrame(Candidate)
     x2df = pd.DataFrame(Demand)

     N1 = x1df.shape[0]
     N2 = x2df.shape[0]
     dist =[]
     for i in range(N1):
          for j in range(N2):
               coord1 = x1df.iloc[i,2:4].values
               coord2 = x2df.iloc[j,2:4].values
               code2 =  x1df.iloc[i,1]
               code1 =  x2df.iloc[j,1]
               dis = haversine(coord1,coord2)
               #a ={} {} {}.format('H'+str(i) +',','P'+str(j)+',' , dis)
               #dist.append(a)
               a = code2 + ',' + code1 +',' + str(dis)
               a = a.split(",")
               dist.append(a)
               #print(dist)
     dist = np.array(dist)
     df = pd.DataFrame(dist)
     my_col = ["Candidate","Demand","distance"]
     df.columns = my_col
     df['distance'] = round(pd.to_numeric(df['distance'])/1609.34,2)
     df['Cost'] = df['distance']* rate_per_mile * 1000/3
     
     return df


def read_file(file_name):
     x1 = pd.read_csv(file_name, encoding='latin-1')
     return x1

def cjmr(df):
     
     list1= df['Candidate'].values.tolist()
     list2= df['layer'].values.tolist()
     list3= df['rank1'].values.tolist()
     list4= df['per_unit_cost'].values.tolist()

     cjmr = dict3(list1,list2,list3,list4)
     
     return cjmr


def cij(df):
     
     list1= df['Demand'].values.tolist()
     list2= df['Candidate'].values.tolist()
     list3= df['Cost'].values.tolist()

     cij = dict2(list1,list2,list3)
     
     return cij


def cj(df,x,y):
     
     list1= df[x].values.tolist()
     list2= df[y].values.tolist()

     cj = dict1(list1,list2)
     
     return cj

def cij_value(df,key1,key2,value):
     
     list1= df[key1].values.tolist()
     list2= df[key2].values.tolist()
     list3= df[value].values.tolist()

     cij = dict2(list1,list2,list3)
     
     return cij          
          
def maximal_covering_out(data,radius):
     max_cov =[]
     max_cov = pd.DataFrame(max_cov)
     for i in range(len(data)):
          df = data[i:i+1]
          dfxx = df.iloc[0,2:3]
          if float(dfxx)> radius:
               ad = max_cov.append(df) 
               max_cov = ad
     return max_cov    
          
def maximal_covering_in(data,radius):
     max_cov =[]
     max_cov = pd.DataFrame(max_cov)
     for i in range(len(data)):
          df = data[i:i+1]
          dfxx = df.iloc[0,2:3]
          if float(dfxx)<= radius:
               ad = max_cov.append(df) 
               max_cov = ad
     return max_cov 


def pre_capacity(data):
     df = data
     list1 = df['Code'].values.tolist()
     list1 = list1[0:54]
     list2 = df['Bed_Capacity'].values.tolist()
     list2 = list2[0:54]
     cj = dict1(list1,list2)
     
     return cj

def trans_rate(ambulance_fare,amb_part, taxi_fare,taxi_part, standard_mileage, regular_part):
     rate = ambulance_fare*amb_part+taxi_fare*taxi_part+standard_mileage*regular_part
     return rate


