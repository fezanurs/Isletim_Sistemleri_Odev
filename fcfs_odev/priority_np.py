import csv

CS_TIME = 0.001 

def read_file(filename):
    procs = []
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None: return []
            reader.fieldnames = [x.strip() for x in reader.fieldnames]
            
            for row in reader:
                if not row: continue
                try: p_str = row['Priority'].strip().lower()
                except: p_str = "normal"
                
                if p_str == 'high': p_val = 1
                elif p_str == 'normal': p_val = 2
                else: p_val = 3
                
                procs.append({
                    'id': row['Process_ID'],
                    'arrival': int(row['Arrival_Time']),
                    'burst': int(row['CPU_Burst_Time']),
                    'priority': p_val,
                    'done': False 
                })
    except: return []
    return procs

def run_priority_np(processes):
    processes.sort(key=lambda x: x['arrival'])
    
    n = len(processes)
    current_time = 0
    completed_count = 0
    cs_count = 0
    log = ["--- PRIORITY GANTT ---"]
    
    wait_times = []
    turnarounds = []
    completed_times = []
    
    pool = [p.copy() for p in processes]

    while completed_count < n:
        available_procs = [p for p in pool if p['arrival'] <= current_time and not p['done']]
        
        if not available_procs:
            future_procs = [p for p in pool if not p['done']]
            if future_procs:
                future_procs.sort(key=lambda x: x['arrival'])
                next_arrival = future_procs[0]['arrival']
                log.append(f"[{current_time:.3f}] -- IDLE -- [{next_arrival:.3f}]")
                current_time = next_arrival
            continue

        highest_priority_job = min(available_procs, key=lambda x: x['priority'])
        
        current_time += CS_TIME
        cs_count += 1
        
        start_t = current_time
        current_time += highest_priority_job['burst']
        end_t = current_time
        
        highest_priority_job['done'] = True
        completed_count += 1
        
        log.append(f"[{start_t:.3f}] -- {highest_priority_job['id']} -- [{end_t:.3f}]")
        
        tat = end_t - highest_priority_job['arrival']
        wt = tat - highest_priority_job['burst']
        
        turnarounds.append(tat)
        wait_times.append(wt)
        completed_times.append(end_t)
        
    return wait_times, turnarounds, completed_times, cs_count, current_time, log

files = ["case1.csv", "case2.csv"]

for f_name in files:
    print(f"Processing {f_name} for Priority...")
    data = read_file(f_name)
    if not data: continue

    wt, tat, completed, cs, total_time, logs = run_priority_np(data)

    avg_wt = sum(wt)/len(wt)
    avg_tat = sum(tat)/len(tat)
    efficiency = (sum(p['burst'] for p in data) / total_time) * 100
    
    throughput_str = ""
    for t in [50, 100, 150, 200]:
        c = sum(1 for x in completed if x <= t)
        throughput_str += f"Throughput T={t}: {c}\n"

    out_name = f"Priority_NP_Result_{f_name}.txt"
    with open(out_name, 'w', encoding='utf-8') as f:
        f.write("\n".join(logs))
        f.write(f"\n\n=== RESULTS FOR {f_name} ===\n")
        f.write(f"Avg Waiting: {avg_wt:.4f}\n")
        f.write(f"Avg Turnaround: {avg_tat:.4f}\n")
        f.write(throughput_str)
        f.write(f"Total Context Switches: {cs}\n")
        f.write(f"CPU Efficiency: %{efficiency:.2f}\n")
        
    print(f">> Saved: {out_name}")