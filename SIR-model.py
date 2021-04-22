#!/usr/bin/env python
# coding: utf-8

# In[1]:


from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.2f' % x)


# ## Read in Data
# - Date, Cases, Deaths, covid_per_10k -> CUMULATIVE
# - SHAPE_Area, SQMI -> Based on County (FIPS)
# - Cluster -> contains many Counties

# In[2]:


mask_df = pd.read_csv('mask-use-by-county.csv')
mask_df.rename({'COUNTYFP': 'fips'}, axis=1, inplace=True)

cluster_df = pd.read_csv('covid_clusters.csv', encoding='latin-1')

df = pd.merge(cluster_df, mask_df, on='fips', how='outer')
df['Mask_Resistance_Score'] = round(df['NEVER']*2 + df['RARELY']*1.5 + df['SOMETIMES']*1 + df['FREQUENTLY']*0.5, 1)

df.head()

#pd.crosstab(cluster_df["STATE_NAME"], cluster_df["cluster"])


# ## Mask Resistance by Cluster
# - Might use the Mean of each Cluster in SIR Model

# In[3]:


#pd.crosstab(df["Mask_Resistance_Score"], df["cluster"])
clusters = [c for c in set(df['cluster']) if c > 0]
print(clusters)

for c in clusters:
    c_df = df[df['cluster'] == c]
    print(c_df[['Mask_Resistance_Score']].describe())
    counts, bins = np.histogram(c_df['Mask_Resistance_Score'])
    plt.hist(bins[:-1], bins, weights=counts)
    print("Cluster {}".format(c))
    plt.show()
    plt.clf()


# ## Cluster Stats

# In[4]:


one_day = df[df['date'] == '1/25/2021']
cluster_stats = one_day.groupby(['cluster'], as_index=False)                        .agg({"FIPS":"nunique", "POPULATION":"sum", "SHAPE_Area":"sum", 
                              "SQMI":"nunique", "POP_SQMI":"sum", "Mask_Resistance_Score": "mean"})
cluster_stats.rename({'FIPS':'Total Counties'}, axis=1, inplace=True)

# Population Density
cluster_stats['Population_per_SQMI'] = cluster_stats['POPULATION']/(cluster_stats['SQMI']*1000)

cluster_stats


# In[5]:


def basic_stats():
    total_population = cluster_stats['POPULATION'].sum()
    print("Total Population", total_population)

    # Total US SQ Miles = 3.797 million
    total_sqmi = cluster_stats['SQMI'].sum()
    print("Total SQ Miles in millons", total_sqmi/1000)

    total_shape = cluster_stats['SHAPE_Area'].sum()
    print("Total Shape", total_shape)
    

basic_stats()


# ## Cumulative Stats by Cluster
# - Date, Cases, Deaths, covid_per_10k

# In[6]:


clusters = [c for c in set(df['cluster']) if c > 0]
print('Clusters: ', clusters)

dfs = []
for c in clusters:
    c_df = df[df['cluster'] == c]
    c_df2 = c_df.groupby(['cluster','date'], as_index=False)                .agg({"cases":"sum", "deaths":"sum", "covid_per_10k":"sum"})
    c_df2['date'] = pd.to_datetime(c_df2['date'])

    c_df2 = c_df2.sort_values(['date'], ascending=True)
    dfs.append(c_df2)


# ## Cases by Day

# In[7]:


for i in range(len(dfs)):
    dfs[i].plot(x="date", y="cases", title="Cluster {}".format(i+1));
    #dfs[i]['cases'].plot(label="Cluster {}".format(i+1))


# ## SIR & New Cases
# - Susceptible (can still be infected, “healthy”)
# - Infected
# - Recovered (were already infected, cannot get infected again)
# - New Cases = Today Cases - Yesterday Cases

# In[8]:


for i in range(len(dfs)):
    dfs[i]['cases_yesterday'] = dfs[i]['cases'].shift(-1)
    dfs[i]['new_cases'] = dfs[i]['cases_yesterday'] - dfs[i]['cases']
    dfs[i]['succeptible'] = cluster_stats['POPULATION'].iloc[i] - dfs[i]['cases']
    dfs[i]['infected'] = dfs[i]['new_cases'].rolling(min_periods=1, window=14).sum() # 14 days
    dfs[i]['recovered'] = dfs[i]['cases'].shift(14) # 14 days
    dfs[i]['recovered'] = dfs[i]['recovered'].fillna(method='bfill')#.fillna(method='bfill')
    dfs[i]['SIR_Total'] = dfs[i]['succeptible'] + dfs[i]['infected'] + dfs[i]['recovered']
    dfs[i]['S_percent'] = (dfs[i]['succeptible'] / dfs[i]['SIR_Total']) *100
    dfs[i]['I_percent'] = (dfs[i]['infected'] / dfs[i]['SIR_Total']) * 100
    dfs[i]['R_percent'] = (dfs[i]['recovered'] / dfs[i]['SIR_Total']) * 100    
    dfs[i]['new_case_rate'] = (dfs[i]['new_cases']/dfs[i]['succeptible']) * 100 

    
dfs[4].tail(5)


# ## Check Work

# In[9]:


def check_work1():
    check_work_df = pd.DataFrame(clusters, columns=['clusters'])

    total_cases_by_cluster = [dfs[i]['new_cases'].sum() for i in range(len(dfs))]
    check_work_df['total_cases'] = total_cases_by_cluster

    total_succeptible_by_cluster_day1 = [dfs[i]['succeptible'].iloc[0] for i in range(len(dfs))]
    check_work_df['total_succeptible_day1'] = total_succeptible_by_cluster_day1

    total_succeptible_by_cluster_last = [dfs[i]['succeptible'].iloc[-1] for i in range(len(dfs))]
    check_work_df['current_S'] = total_succeptible_by_cluster_last

    current_infected_by_cluster = [dfs[i]['infected'].iloc[-1] for i in range(len(dfs))]
    check_work_df['current_I'] = current_infected_by_cluster

    total_recovered_by_cluster = [dfs[i]['recovered'].iloc[-1] for i in range(len(dfs))]
    check_work_df['current_R'] = total_recovered_by_cluster

    check_work_df['total_SIR'] = check_work_df['current_S'] + check_work_df['current_I'] + check_work_df['current_R']
    check_work_df['diff_1'] = check_work_df['total_succeptible_day1'] - check_work_df['total_SIR']

    display(check_work_df)
    
#check_work1()


# In[10]:


def check_work2():
    total_cases_by_cluster = [dfs[i]['new_cases'].sum() for i in range(len(dfs))]
    total_cases = sum(total_cases_by_cluster)

    total_succeptible_by_cluster_day1 = [dfs[i]['succeptible'].iloc[0] for i in range(len(dfs))]
    total_S_day1 = sum(total_succeptible_by_cluster_day1)

    total_succeptible_by_cluster_last = [dfs[i]['succeptible'].iloc[-1] for i in range(len(dfs))]
    total_S_last_day = sum(total_succeptible_by_cluster_last)

    current_infected_by_cluster = [dfs[i]['infected'].iloc[-1] for i in range(len(dfs))]
    current_I = sum(current_infected_by_cluster)

    total_recovered_by_cluster = [dfs[i]['recovered'].iloc[-1] for i in range(len(dfs))]
    total_R = sum(total_recovered_by_cluster)

    print('Total Succeptible Day 1: ', total_S_day1)
    print('Total Cases All Time: ', total_cases)
    print('Population Infected %: ', (total_cases/total_S_day1*100), '\n')

    print('Total Succeptible Last Day: ', total_S_last_day)
    print('Current Infected Last Day: ', current_I)
    print('Total Recovered Last Day: ', total_R)

    # 14 day window might be issue
    difference1 = total_S_day1 - (total_S_last_day+current_I+total_R)
    print('\nDifference 1: ',difference1)

    difference2 = (total_S_day1 - total_cases) - total_S_last_day
    print('Difference 2: ',difference2)
    return ''
 
#check_work2()


# In[11]:


#dfs[0].to_csv('df0.csv')
max_infection_rates = []
min_infection_rates = []
avg_infection_rates = []

for i in range(len(dfs)):
    dfs[i].plot(x="date", y="new_cases", title="Cluster {}".format(i+1)); #new cases
    #dfs[i][['date','infected','recovered','succeptible']].plot.area(x="date", title="Cluster {}".format(i+1)); # SIR
    dfs[i][['date','I_percent','R_percent','S_percent']].plot.area(x="date", title="Cluster {}".format(i+1)); # SIR
    display(dfs[i][['date','I_percent','R_percent','S_percent']].tail(1))
    
    #print("Max Infection Rate - Cluster {}".format(i+1), dfs[i]['new_case_rate'].max())
    temp_case_rates = [i for i in dfs[i]['new_case_rate'] if i > 0]
    max_infection_rates.append(max(temp_case_rates))
    min_infection_rates.append(min(temp_case_rates))
    avg_infection_rates.append(dfs[i]['new_case_rate'].mean())
    


# ## SIR Model - Actual Curve

# In[12]:


def plotsir(t, S, I, R):
    f, ax = plt.subplots(1,1,figsize=(10,4))
    ax.plot(t, S, 'b', alpha=0.7, linewidth=2, label='Susceptible')
    ax.plot(t, I, 'y', alpha=0.7, linewidth=2, label='Infected')
    ax.plot(t, R, 'g', alpha=0.7, linewidth=2, label='Recovered')

    ax.set_xlabel('Time (days)')

    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show();


# In[13]:


for i in range(len(dfs)):
    t = np.array(dfs[i]['date'])
    S = np.array(dfs[i]['succeptible'])
    I = np.array(dfs[i]['infected'])
    R = np.array(dfs[i]['recovered'])
    print("Cluster {}".format(i+1))
    plotsir(t, S, I, R)


# ## SIR Model - Simulation

# In[14]:


def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


# In[15]:


def example_SIR():
    N = 10000 # population of 10000
    beta = 1.0  # infected person infects 1 other person per day
    D = 7.0 # infections lasts 14 days
    gamma = 1.0 / D # 

    # initial conditions: one infected, rest susceptible
    infected_start = 1
    recovered_start = 0
    S0, I0, R0 = (N-infected_start), infected_start, recovered_start  

    t = np.linspace(0, 49, 50) # Grid of time points (in days)
    y0 = S0, I0, R0 # Initial conditions vector

    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    plotsir(t, S, I, R)

#example_SIR()


# In[16]:


#cluster_stats.info()


# # Innovation
# - Create Infection Rate based on Cluster specific factors
# - Mask_Resistance_Score + Population_Density + ?

# In[17]:


for i in range(len(dfs)):
    last_day = dfs[i].iloc[-1]
    
    # Population
    N = 100 #last_day['SIR_Total']
    
    # infected person infects 1 other person per day
    beta = (cluster_stats.iloc[i]['Mask_Resistance_Score']) #+ cluster_stats.iloc[i]['Mask_Resistance_Score']
    
    # infections lasts 14 days
    D = 14.0
    gamma = 1.0 / D
    
    # initial conditions: one infected, rest susceptible
    infected_start = last_day['I_percent']#last_day['infected']
    recovered_start = last_day['R_percent'] #last_day['recovered']
    S0, I0, R0 = (N-infected_start), infected_start, recovered_start  

    t = np.linspace(0, 49, 50) # Grid of time points (in days)
    y0 = S0, I0, R0 # Initial conditions vector

    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T
    
    
    print("Cluster {}".format(i+1))
    plotsir(t, S, I, R)


# ## Assumptions:
# - People are not traveling from cluster to cluster.
# - People can not get COVID more than once
# - Environment across Clusters (Temp) 
# 

# In[20]:


#pd.crosstab(cluster_df["STATE_NAME"], cluster_df["cluster"])


# In[ ]:




