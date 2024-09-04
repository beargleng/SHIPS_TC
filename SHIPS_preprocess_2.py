import pandas as pd

datas = pd.read_csv('\output.csv',
                    names=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P'
                           ,'Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC'])

## variable in 0 moment
data0 = datas['C']
data6 = datas['D']
datatime = datas['B']
dataname = datas['H']
# IR = data0.iat[7]
# Vm = data0.iat[2]
# sst = (data0.iat[10])/10
# lat = (data0.iat[8])/10
# MPI = data0.iat[66]
IR = [] # 6h kt
Vm = [] # kt
sst = []
lat = []
MPI = [] # kt
vm = [] # m/s
mpi = [] # m/s
ir = [] # 6h m/s

time1 = []
time2 = []

name = []

## The data is taken every 139 rows, and every 139 is a record, 
## but it is different for different basins, and some are 89

for i in range(0,12526):  
    IR.append(data6.iat[7+i*139])
    Vm.append(data0.iat[2+i*139])
    sst.append((data0.iat[10+i*139])/10)
    lat.append((data0.iat[8+i*139])/10)
    MPI.append(data0.iat[66+i*139])
    time1.append(datatime.iat[i*139])
    time2.append(data0.iat[i*139])
    name.append(dataname.iat[i*139])
    

for i in range(0,12526):
    vm.append(Vm[i] * 0.514) # m/s
    mpi.append(MPI[i] * 0.514)
    ir.append(IR[i] * 0.514)


# read time
time2 = [f"{num:02}" for num in time2]
time1 = [f"{num:06}" for num in time1]
time = [None]*12526
for i in range(0,12526):
    time[i] = str(time1[i]) + str(time2[i])

df = pd.DataFrame({'Vm': Vm, 'time': time2})
#############################################
# intensification rate for 24h
def calculate_difference(row):
    i = row.name
    if i > len(df) -5 :
        return 0
    time_diff = (int(df['time'][i+4]) - int(df['time'][i]))  
    if time_diff == 0:
        return df['Vm'][i+4] - df['Vm'][i]
    else:
        return 0


df['Vm_Difference'] = df.apply(calculate_difference, axis=1)

IR24 = pd.Series(df['Vm_Difference'])
#################################################
vm = pd.Series(vm)
Vm = pd.Series(Vm)
mpi = pd.Series(mpi)
MPI = pd.Series(MPI)
time = pd.Series(time)
name = pd.Series(name)
IR24 = pd.Series(IR24)
# IR24.replace(-999, np.nan, inplace=True)

# Shuju is a dataframe the whole case composed of the selected useful physical variables,
# but all tcs are in it.

# you need to extract one, 
# you have to know the name you want, or use the name list traversal loop to extract all tc.

shuju = pd.DataFrame({'vm':vm,'Vm':Vm,'mpi':mpi,'MPI':MPI,'name':name,'time':time,'IR':IR24})


#####################################################
obIRmax = []
LMI = []
MPI_ = []
# mpi_ = []
PIR_ = []

C_D = 2.4 * 10**-3
H = 2000

name = list(set(name)) # a list of names. The following operations are to loop each tc in the name list.
for i in name:
    tc = shuju[shuju['name'] == i] # tc here mean a single TC
    maxIRob = max(tc['IR']) 
    MPIi = tc.loc[tc['IR'] == maxIRob, 'MPI']
    MPIi = MPIi.iat[-1]
    mpii = tc.loc[tc['IR'] == maxIRob, 'mpi']  
    mpii = mpii.iat[-1]
    LMIi = max(tc['Vm'])
    vm_irmax = tc.loc[tc['IR'] == maxIRob, 'vm']
    vm_irmax = vm_irmax.iat[-1]
    obIRmax.append(maxIRob)
    # piri = (C_D/H) * mpii**2 * ((vm_irmax/mpii)**1.5 - (vm_irmax/mpii)**2)
    piri = (27/256) * (C_D/H) * mpii**2 # m/s /s
    PIR24 = (piri/0.514)*3600*24
    PIR_.append(PIR24)
    LMI.append(LMIi)
    MPI_.append(MPIi)
    # mpi_.append(mpii)