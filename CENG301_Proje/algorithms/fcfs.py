# algorithms/fcfs.py

from typing import List, Dict, Any, Tuple
from utils.parser import log_event # Loglama için Process nesnesini import etmeye gerek yok

def run_fcfs(processes: List[Any]) -> Tuple[List[Any], List[Dict[str, Any]], int]:
    """
    First Come First Served (FCFS) non-preemptive algoritmasını çalıştırır.
    """
    
    # Süreçleri varış zamanına göre sırala
    sim_processes = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    completed_processes = []
    gantt_chart = []
    
    # FCFS non-preemptive olduğu için Context Switch sayısı 0'dır (IDLE'dan sonraki ilk geçiş sayılmaz).
    # Ancak FCFS'te de IDLE durumundan çalışmaya geçişler teknik olarak Context Switch sayılmaz. 
    # Genellikle CS sayısı non-preemptive algoritmalar için 0 kabul edilir.
    context_switch_count = 0 
    
    # Tüm süreçlerin işi bitene kadar döngü
    i = 0
    while i < len(sim_processes):
        p = sim_processes[i]
        
        # 1. Varış kontrolü ve IDLE süresi
        if p.arrival_time > current_time:
            # IDLE durumu: CPU boşta, süreç gelene kadar bekle
            if not gantt_chart or gantt_chart[-1]['pid'] != 'IDLE':
                gantt_chart.append({'pid': 'IDLE', 'start': current_time, 'end': p.arrival_time})
            current_time = p.arrival_time

        # Loglama: ARRIVED olayı (Varış zamanında logla)
        log_event(p, p.arrival_time, "ARRIVED", "Kuyruğa eklendi")
        
        # 2. Süreci Çalıştırma (Non-preemptive olduğu için tamamlanana kadar çalışır)
        
        # İlk başlama zamanını kaydet ve logla
        p.first_start_time = current_time
        log_event(p, current_time, "STARTED", f"Toplam süre: {p.burst_time}")
        
        start_time = current_time
        finish_time = start_time + p.burst_time
        
        # Gantt kaydını ekle
        gantt_chart.append({'pid': p.pid, 'start': start_time, 'end': finish_time})
        
        current_time = finish_time
        
        # 3. Tamamlanma
        p.remaining_time = 0
        p.completion_time = current_time
        p.is_completed = True
        completed_processes.append(p)
        
        # Loglama: COMPLETED olayı
        log_event(p, current_time, "COMPLETED", f"Toplam süre: {p.burst_time}")

        i += 1
        

    return processes, gantt_chart, context_switch_count