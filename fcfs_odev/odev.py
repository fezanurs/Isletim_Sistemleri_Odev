import csv
import sys

CS_TIME = 0.001 

def read_file(filename):
    procs = []
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            if reader.fieldnames is None:
                print(f"\n[UYARI] '{filename}' dosyasi BOS veya okunamadi! Atlaniyor...")
                return []
            
            reader.fieldnames = [x.strip() for x in reader.fieldnames] 
            
            for row in reader:
                if not row: continue 

                try:
                    p_str = row['Priority'].strip().lower()
                except:
                    p_str = "normal"

                if p_str == 'high': p_val = 1
                elif p_str == 'normal': p_val = 2
                else: p_val = 3
                
                procs.append({
                    'id': row['Process_ID'],
                    'arrival': int(row['Arrival_Time']),
                    'burst': int(row['CPU_Burst_Time']),
                    'priority': p_val
                })
                
    except FileNotFoundError:
        print(f"\n[HATA] '{filename}' bulunamadi. Dosya ismini kontrol et.")
        return []
    except Exception as e:
        print(f"\n[HATA] Beklenmedik hata: {e}")
        return []
        
    return procs

def run_fcfs(processes):
    processes.sort(key=lambda x: x['arrival'])
    
    current_time = 0
    cs_count = 0
    log = ["--- FCFS GANTT CHART ---"]
    
    wait_times = []
    turnarounds = []
    completed_times = [] 
    
    for p in processes:
        if current_time < p['arrival']:
            log.append(f"[{current_time:.3f}] -- IDLE -- [{p['arrival']:.3f}]")
            current_time = p['arrival']
            
        current_time += CS_TIME
        cs_count += 1
        
        start_t = current_time
        current_time += p['burst']
        end_t = current_time
        
        log.append(f"[{start_t:.3f}] -- {p['id']} -- [{end_t:.3f}]")
        
        tat = end_t - p['arrival']
        wt = tat - p['burst']
        
        turnarounds.append(tat)
        wait_times.append(wt)
        completed_times.append(end_t)
        
    return wait_times, turnarounds, completed_times, cs_count, current_time, log

print("Program baslatiliyor...")
files = ["case1.csv", "case2.csv"]

for f_name in files:
    print(f"\nProcessing {f_name}...")
    data = read_file(f_name)
    
    if not data:
        print(f"-> {f_name} icin veri alinamadi.")
        continue 

    wt, tat, completed, cs, total_time, logs = run_fcfs(data)

    print(f"--- SONUC: {f_name} ---")
    print(f"Avg Waiting: {sum(wt)/len(wt):.4f}")
    
    throughput_str = ""
    for t in [50, 100, 150, 200]:
        c = sum(1 for x in completed if x <= t)
        throughput_str += f"Throughput T={t}: {c}\n"

    efficiency = (sum(p['burst'] for p in data) / total_time) * 100
    

    out_name = f"FCFS_Result_{f_name}.txt"
    with open(out_name, 'w', encoding='utf-8') as f:
        f.write("\n".join(logs))
        f.write(f"\n\n=== RESULTS FOR {f_name} ===\n")
        f.write(f"Avg Waiting Time: {sum(wt)/len(wt):.4f}\n")
        f.write(f"Avg Turnaround Time: {sum(tat)/len(tat):.4f}\n")
        f.write(throughput_str)
        f.write(f"Total Context Switches: {cs}\n")
        f.write(f"CPU Efficiency: %{efficiency:.2f}\n")
        
    print(f">> Kaydedildi: {out_name}")

print("\nISLEM TAMAMLANDI.")