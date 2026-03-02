# algorithms/srtf.py

from typing import List, Dict, Any, Tuple
# Loglama fonksiyonu artık utils.parser'dan geliyor.
from utils.parser import log_event 

def run_srtf(processes):
    """
    Shortest Remaining Time First (SRTF) preemptive algoritmasını çalıştırır.
    """
    
    sim_processes = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    context_switch_count = 0
    
    ready_queue = []
    completed_processes = []
    running_process = None
    gantt_chart = []
    
    while len(completed_processes) < len(sim_processes):
        
        # 1. Yeni Gelen Süreçleri Ready Queue'ya Ekle ve Logla
        newly_arrived = [p for p in sim_processes if p.arrival_time == current_time 
                         and p not in ready_queue 
                         and not p.is_completed
                         and p != running_process 
                         ]

        ready_queue.extend(newly_arrived) 
        for p in newly_arrived:
             # Loglama: ARRIVED olayı
             log_event(p, p.arrival_time, "ARRIVED", "Kuyruğa eklendi") 

        # 2. Hazır Kuyruğa Giren Süreçler Arasından En İyisini Seçme
        current_candidates = ready_queue.copy()
        if running_process and running_process.remaining_time > 0:
            current_candidates.append(running_process)
        
        if not current_candidates:
            # IDLE durumu kontrolü
            remaining = [p for p in sim_processes if not p.is_completed]
            if remaining:
                next_arrival_time = min(p.arrival_time for p in remaining)
                if next_arrival_time > current_time:
                    if not gantt_chart or gantt_chart[-1]['pid'] != 'IDLE':
                        gantt_chart.append({'pid': 'IDLE', 'start': current_time, 'end': next_arrival_time})
                    current_time = next_arrival_time
                else:
                    current_time += 1
            else:
                break 
            continue 

        # SRTF Kuralı
        current_candidates.sort(key=lambda p: (p.remaining_time, p.arrival_time, p.pid))
        next_process = current_candidates[0]
        
        # 3. Preemption Kontrolü ve Context Switch
        if running_process != next_process:
            
            # Eğer kesinti oluyorsa
            if running_process is not None and running_process.remaining_time > 0:
                if running_process not in ready_queue: 
                    ready_queue.append(running_process)
                # Loglama: PREEMPTED olayı
                log_event(running_process, current_time, "PREEMPTED", f"Kalan süre: {running_process.remaining_time}") 

            # Yeni süreci çalıştırmaya başla
            running_process = next_process
            if running_process in ready_queue:
                ready_queue.remove(running_process)
            
            # İlk başlama zamanını kaydet ve logla
            if running_process.first_start_time == -1:
                running_process.first_start_time = current_time
                # Loglama: STARTED olayı
                log_event(running_process, current_time, "STARTED", f"Kalan süre: {running_process.burst_time}")
                
            # Gantt bloğunu başlat
            if not gantt_chart or gantt_chart[-1]['pid'] != running_process.pid:
                gantt_chart.append({'pid': running_process.pid, 'start': current_time, 'end': current_time + 1})
        
        # 4. Süreci İlerletme ve Zamanı Artırma
        if running_process:
            running_process.remaining_time -= 1
            
            if gantt_chart[-1]['pid'] == running_process.pid:
                gantt_chart[-1]['end'] = current_time + 1
            
            current_time += 1
            
            # 5. Tamamlanma Kontrolü 
            if running_process.remaining_time == 0:
                running_process.completion_time = current_time
                running_process.is_completed = True
                completed_processes.append(running_process)
                # Loglama: COMPLETED olayı
                log_event(running_process, current_time, "COMPLETED", f"Toplam süre: {running_process.burst_time}")
                running_process = None 
        else:
             current_time += 1 

    # Context Switch Sayısını Gantt Verisine Göre Düzeltme
    cs_count_recalculated = 0
    if gantt_chart:
        non_idle_blocks = [d for d in gantt_chart if d['pid'] != 'IDLE']
        if len(non_idle_blocks) > 0:
            cs_count_recalculated = len(non_idle_blocks) - 1

    context_switch_count = cs_count_recalculated

    for original_p in processes:
        for completed_p in completed_processes:
            if original_p.pid == completed_p.pid:
                original_p.__dict__.update(completed_p.__dict__)

    return processes, gantt_chart, context_switch_count