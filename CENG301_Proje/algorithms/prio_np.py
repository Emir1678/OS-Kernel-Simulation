# algorithms/prio_np.py 

from typing import List, Dict, Any, Tuple
from utils.parser import log_event 
import sys

def run_prio_np(processes: List[Any]) -> Tuple[List[Any], List[Dict[str, Any]], int]:
    """
    Non-Preemptive Priority (PRIO NP) algoritmasını çalıştırır.
    Düşük öncelik değeri, yüksek öncelik anlamına gelir.
    """
    
    sim_processes = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    completed_processes = []
    ready_queue = []
    gantt_chart = []
    context_switch_count = 0 
    
    while len(completed_processes) < len(sim_processes):
        
        # 1. Yeni gelen süreçleri hazır kuyruğa ekle
        for p in sim_processes:
            if p.arrival_time <= current_time and not p.is_completed and p not in ready_queue:
                ready_queue.append(p)
                log_event(p, p.arrival_time, "ARRIVED", f"Kuyruğa eklendi (Öncelik: {p.priority})")
        
        # 2. Çalıştırılacak süreci seç
        if ready_queue:
            # PRIO NP Kuralı: Hazır kuyruktaki en düşük öncelik değerine (en yüksek öncelik) sahip süreci seç.
            # Beraberlik durumunda: Varış zamanı daha erken olanı seç.
            ready_queue.sort(key=lambda p: (p.priority, p.arrival_time, p.pid))
            running_process = ready_queue.pop(0)
            
            # 3. Süreci Çalıştırma (Non-preemptive)
            
            # İlk başlama zamanını kaydet ve logla
            running_process.first_start_time = current_time
            log_event(running_process, current_time, "STARTED", f"Toplam süre: {running_process.burst_time}")
            
            start_time = current_time
            finish_time = start_time + running_process.burst_time
            
            gantt_chart.append({'pid': running_process.pid, 'start': start_time, 'end': finish_time})
            current_time = finish_time
            
            # 4. Tamamlanma
            running_process.remaining_time = 0
            running_process.completion_time = current_time
            running_process.is_completed = True
            log_event(running_process, current_time, "COMPLETED", f"Toplam süre: {running_process.burst_time}")
            completed_processes.append(running_process)

        else:
            # IDLE Durumu
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

    # Context Switch Sayısını Hesapla
    non_idle_blocks = [d for d in gantt_chart if d['pid'] != 'IDLE']
    if len(non_idle_blocks) > 0:
        context_switch_count = len(non_idle_blocks) - 1

    return processes, gantt_chart, context_switch_count