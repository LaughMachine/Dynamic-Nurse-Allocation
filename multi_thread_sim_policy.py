#!/apps/anaconda-2.3.0/bin/python

import six_server_queue as ssq
import sys
import csv
import os
import time
# Usage: multi_thread filename tau nurse util trial
def writeLog(fil, table):
    c1 = csv.writer(fil)
    for val in table:
        c1.writerow(val)

tau_arr = [2, 4, 8, 12, 16]
rho_arr = [.92, .96]
mu_arr = [[1,.5],[.5,.5],[.5,1]]
load_arr = [1/4.0, 1/2.0, 3/4.0]
n_array = [20, 50, 80]
safety = [1,2,3,4]
trials = range(11,21)

test_lib = []
for t in tau_arr:
    for r in rho_arr:
        for m in mu_arr:
            for l in load_arr:
                for n in n_array:
                    for s in safety:
                        for c in trials:
                            test_lib.append([t, r, m, l, n, s, c])

# test_parameters = test_lib[int(sys.argv[1])-1]
test_parameters = [10, .96, [.5,.5], 1/2.0, 300, 1, 11]

arr = []
tot_par = 1
Nurses = int(test_parameters[4])

mu = test_parameters[2]
ku = mu[1]/mu[0]
beta = test_parameters[3]/((1-test_parameters[3])*ku)
l1 = Nurses*test_parameters[1]/(1/mu[0]+1/(beta*ku*mu[0]))
lbda_rate = [l1 , l1/beta]
std_out = [0, 0]
tau_out = [int(test_parameters[0]) for x in range(tot_par)]
k_out = 2
Total_Time = 100
lbda_out = [1/x for x in lbda_rate]
mu_out = [1/x for x in mu]
theta_out = [float('inf'), float('inf')]
hcost_out = [2/mu[0], 1/mu[1]]
q_cap_out = [float('inf'), float('inf')]
rebalance1 = [0]
cont_out = [0]
preemption_out = [0]
time_vary = False
s_alloc_out = []
dedicated_alloc = [int(Nurses*.5), int(Nurses*.5)]
safety_out = test_parameters[5]
for i in range(0, tot_par):
    if cont_out[i] == 1:
        s_alloc_out.append([Nurses, Nurses])
    else:
        s_alloc_out.append(dedicated_alloc)


print 'Nurses: ' + str(Nurses)
print 'tau_out: ' + str(tau_out)
print 'classes: ' + str(k_out)
print 'total time: ' + str(Total_Time)
print 'arrival rate: ' + str(lbda_rate)
print 'service rate: ' + str(mu)
print 'service std: ' + str(std_out)
print 'theta: ' + str(theta_out)
print 'holding cost: ' + str(hcost_out)
print 'queue length: ' + str(q_cap_out)
print 'parallel simulations' + str(tot_par)
print 'starting allocation: ' + str(s_alloc_out)
print 'rebalance: ' + str(rebalance1)
print 'continuous: ' + str(cont_out)
print 'preemption: ' + str(preemption_out)
print 'time vary: ' + str(time_vary)


s = ssq.Simulation(Total_Time, Nurses, lbda_out, mu_out, std_out, theta_out, tau_out, k_out, hcost_out, q_cap_out,
                   s_alloc_out, tot_par, rebalance1, cont_out, preemption_out, time_vary)
s.generate_arrivals(time_vary)
s.set_preexisting_rnd([450, 300])
s.safety = [1,2,4,1]
s.safe = 1
# print s.dedicated_alloc
# print s.dedicated_cost

start_time = time.clock()
s.simulate(False,True)
end_time = time.clock()-start_time
print [x/float(s.t[ind]) for ind, x in enumerate(s.holding_cost)]

# out = []
# out.append([x/float(s.t[ind]) for ind, x in enumerate(s.arrival_count)])
# out.append([x/float(s.t[ind]) for ind, x in enumerate(s.holding_cost)])
# out.append([x/float(Nurses*s.t[ind]) for ind, x in enumerate(s.time_server_occupied)])
# out.append([[x/float(s.t[ind]) for ind, x in enumerate(y)] for y in s.weighted_ward])
# out.append([[x/float(s.t[ind]) for ind, x in enumerate(y)] for y in s.weighted_queue])
# out.append([end_time])

# fil = open(os.getcwd() + "/Results" + '_' + str(test_parameters[0]) + '_' + str(int(test_parameters[1] * 100)) + '_'
#           + str(int(1 / test_parameters[2][0])) + '_' + str(int(1 / test_parameters[2][1]))
#           + '_' + str(int(test_parameters[3] * 100)) + '_' + str(test_parameters[4]) + '_' + str(test_parameters[5]) + '_'
#           + str(test_parameters[6]) + ".csv", "wb")
# writeLog(fil, out)

fil0 = open(os.getcwd() + "/Sim_safety_ded_v.csv", "wb")
# fil1 = open(os.getcwd() + "/Sim_safety_2.csv", "wb")
# fil2 = open(os.getcwd() + "/Sim_safety_4.csv", "wb")
# fil3 = open(os.getcwd() + "/Sim_safety_ded.csv", "wb")
#
writeLog(fil0, s.statistics[0])
# writeLog(fil1, s.statistics[1])
# writeLog(fil2, s.statistics[2])
# writeLog(fil3, s.statistics[3])