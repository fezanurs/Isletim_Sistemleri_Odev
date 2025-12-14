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
                    'remaining': int(row['CPU_Burst_Time']),
                    'priority': p_val,
                    'start_time': -1,
                    'finish_time': 0
                })
    except: return []
    return procs

def run_priority_preemptive(processes):
    processes.sort(key=lambda x: x['arrival'])
    n = len(processes)
    current_time = 0
    completed = 0
    cs_count = 0
    log = ["--- PREEMPTIVE PRIORITY GANTT ---"]
    
    last_proc_id = None 
    active_pool = []
    proc_idx = 0
    
    while completed < n:
        while proc_idx < n and processes[proc_idx]['arrival'] <= current_time:
            active_pool.append(processes[proc_idx])
            proc_idx += 1
            
        if not active_pool:
            if proc_idx < n:
                next_arrival = processes[proc_idx]['arrival']
                log.append(f"[{current_time:.3f}] -- IDLE -- [{next_arrival:.3f}]")
                current_time = next_arrival
            continue
            
        current_proc = min(active_pool, key=lambda x: x['priority'])
        
        if last_proc_id != current_proc['id']:
            current_time += CS_TIME
            cs_count += 1
            last_proc_id = current_proc['id']
            if current_proc['start_time'] == -1:
                current_proc['start_time'] = current_time
        
        if proc_idx < n:
            time_to_next = processes[proc_idx]['arrival'] - current_time
            if time_to_next < 0: time_to_next = 0
        else:
            time_to_next = 99999999
            
        time_to_finish = current_proc['remaining']
        run_time = min(time_to_next, time_to_finish)
        
        if run_time <= 0 and proc_idx < n:
             run_time = 1
             
        start_t = current_time
        current_time += run_time
        current_proc['remaining'] -= run_time
        end_t = current_time
        
        log.append(f"[{start_t:.3f}] -- {current_proc['id']} -- [{end_t:.3f}]")
        
        if current_proc['remaining'] <= 0:
            completed += 1
            current_proc['finish_time'] = current_time
            active_pool.remove(current_proc)
            last_proc_id = None
            
    wt_list = []
    tat_list = []
    
    for p in processes:
        tat = p['finish_time'] - p['arrival']
        wt = tat - p['burst']
        if wt < 0: wt = 0
        tat_list.append(tat)
        wt_list.append(wt)
        
    return wt_list, tat_list, cs_count, current_time, log

files = ["case1.csv", "case2.csv"]

for f_name in files:
    print(f"Processing {f_name} for Preemptive Priority...")
    data = read_file(f_name)
    if not data: continue

    wt, tat, cs, total_time, logs = run_priority_preemptive(data)

    avg_wt = sum(wt)/len(wt)
    avg_tat = sum(tat)/len(tat)
    efficiency = (sum(p['burst'] for p in data) / total_time) * 100
    
    out_name = f"Preemptive_Priority_Result_{f_name}.txt"
    with open(out_name, 'w', encoding='utf-8') as f:
        f.write("\n".join(logs))
        f.write(f"\n\n=== RESULTS ===\nAvg Waiting: {avg_wt:.4f}\nAvg Turnaround: {avg_tat:.4f}\n")
        f.write(f"Total Context Switches: {cs}\nCPU Efficiency: %{efficiency:.2f}\n")
        
    print(f">> Saved: {out_name}")