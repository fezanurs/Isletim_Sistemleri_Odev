import csv

QUANTUM = 4 
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

def run_rr(processes):
    processes.sort(key=lambda x: x['arrival'])
    
    n = len(processes)
    current_time = 0
    completed = 0
    cs_count = 0
    log = ["--- ROUND ROBIN GANTT ---"]
    
    queue = []
    i = 0
    
    while i < n and processes[i]['arrival'] <= current_time:
        queue.append(processes[i])
        i += 1
        
    while completed < n:
        if not queue:
            if i < n:
                current_time = processes[i]['arrival']
                while i < n and processes[i]['arrival'] <= current_time:
                    queue.append(processes[i])
                    i += 1
                log.append(f"[{current_time:.3f}] -- IDLE")
            else:
                break
                
        p = queue.pop(0)
        
        if p['start_time'] == -1:
            p['start_time'] = current_time
            
        current_time += CS_TIME
        cs_count += 1
        
        start_t = current_time
        exec_time = min(QUANTUM, p['remaining'])
        
        current_time += exec_time
        p['remaining'] -= exec_time
        end_t = current_time
        
        log.append(f"[{start_t:.3f}] -- {p['id']} -- [{end_t:.3f}]")
        
        while i < n and processes[i]['arrival'] <= current_time:
            queue.append(processes[i])
            i += 1
            
        if p['remaining'] > 0:
            queue.append(p)
        else:
            completed += 1
            p['finish_time'] = current_time

    wt_list = []
    tat_list = []
    comp_times = []
    
    for p in processes:
        tat = p['finish_time'] - p['arrival']
        wt = tat - p['burst']
        if wt < 0: wt = 0 
        
        tat_list.append(tat)
        wt_list.append(wt)
        comp_times.append(p['finish_time'])
        
    return wt_list, tat_list, comp_times, cs_count, current_time, log

files = ["case1.csv", "case2.csv"]

for f_name in files:
    print(f"Processing {f_name} for Round Robin...")
    data = read_file(f_name)
    if not data: continue

    wt, tat, completed, cs, total_time, logs = run_rr(data)

    avg_wt = sum(wt)/len(wt)
    avg_tat = sum(tat)/len(tat)
    efficiency = (sum(p['burst'] for p in data) / total_time) * 100
    
    throughput_str = ""
    for t in [50, 100, 150, 200]:
        c = sum(1 for x in completed if x <= t)
        throughput_str += f"Throughput T={t}: {c}\n"

    out_name = f"RR_Result_{f_name}.txt"
    with open(out_name, 'w', encoding='utf-8') as f:
        f.write("\n".join(logs))
        f.write(f"\n\n=== RESULTS FOR {f_name} ===\n")
        f.write(f"Avg Waiting: {avg_wt:.4f}\n")
        f.write(f"Avg Turnaround: {avg_tat:.4f}\n")
        f.write(throughput_str)
        f.write(f"Total Context Switches: {cs}\n")
        f.write(f"CPU Efficiency: %{efficiency:.2f}\n")
        
    print(f">> Saved: {out_name}")