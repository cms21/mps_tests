import matplotlib.pyplot as plt
import numpy as np

# TOTAL RUN TIME for 4 runs is 43 seconds

npartitions = [1,4,8,16,32,48]
run_time = []
for i in npartitions:
    with open(f"test_{i}.out","r") as f:
        lines = f.readlines()

        for line in lines:
            if "TOTAL RUN TIME" in line:
                split_line = line.split()
                run_time.append(float(split_line[7]))
plt.figure()
npartitions = np.array(npartitions)
run_time = np.array(run_time)
plt.plot(npartitions,run_time/npartitions,'o--',label=r"10$^4$")
plt.xlabel("Partition Number")
plt.ylabel("Time per partition per GPU (s)")
plt.savefig("perf.pdf",format="pdf")

plt.figure()

plt.plot(npartitions,run_time/run_time[0],'o--')
plt.xlabel("Partition Number")
plt.ylabel("Time/Time(0)")
plt.savefig("perf_norm.pdf",format="pdf")


plt.figure()

nslices = 250
for i,p in enumerate(npartitions):
    if p == 1:
        continue
    time_per_gpu = run_time[i]
    runs_per_node = 4*p
    num_nodes = []
    tot_run_time_8 = []
    tot_run_time_32 = []
    for n in range(1,201):
        
        num_nodes.append(n)
        nslots = 8*nslices//(runs_per_node*n)
        if 8*nslices/(runs_per_node*n) - nslots > 0:
            nslots += 1
        nslots = max(nslots, 1)
        tot_run_time_8.append(nslots*time_per_gpu)
        
        nslots = 32*nslices//(runs_per_node*n)
        if 32*nslices/(runs_per_node*n) - nslots > 0:
            nslots += 1
        nslots = max(nslots, 1)
        tot_run_time_32.append(nslots*time_per_gpu)
    tot_run_time_8 = np.array(tot_run_time_8)
    print(tot_run_time_8)
    tot_run_time_32 = np.array(tot_run_time_32)
    line, = plt.plot(num_nodes,tot_run_time_8/60,'-',label=f"npartitions={p}")
    plt.plot(num_nodes,tot_run_time_32/60,':',c=line.get_color())
plt.plot([0,200],[1,1],'k--')
plt.ylim(0,5)
plt.xlim(0,200)
plt.xlabel("Nodes")
plt.ylabel("Run time (minutes)")
plt.legend(loc=0,title=f" Single GPU test scaled\n solid:     8 runs per slice \n dotted: 32 runs per slice \n 250 slices, "+r"10$^4$ particles")
plt.savefig("run_time.pdf",format="pdf")
        
