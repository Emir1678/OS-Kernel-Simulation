# algorithms/rr.py

from typing import List, Dict, Any, Tuple
# utils.logger'ın import edilmediği varsayılıyordu, ancak loglama için GEREKLİ:
from utils.parser import log_event 

def run_rr(processes, quantum):
    """
    Round Robin (RR) preemptive algoritmasını çalıştırır.
    """
    if quantum <= 0:
        raise ValueError("Quantum süresi pozitif bir tam sayı olmalıdır.")

    sim_processes = sorted(processes, key=lambda p: p.arrival_time)
    current_time = 0
    context_switch_count = 0
    
    ready_queue = []
    completed_processes = []
    running_process = None
    gantt_chart = []
    
    while len(completed_processes) < len(sim_processes):
        
        # 1. Yeni Gelen Süreçleri Ready Queue'ya Ekle ve Logla
        newly_arrived = [p for p in sim_processes if p.arrival_time <= current_time 
                         and p not in ready_queue 
                         and not p.is_completed]
        
        for p in newly_arrived:
            if p.remaining_time > 0 and p != running_process:
                if p not in ready_queue:
                    ready_queue.append(p)
                    # Loglama: ARRIVED olayı
                    log_event(p, p.arrival_time, "ARRIVED", "Kuyruğa eklendi") 
        
        # 2. CPU'yu Yönetme ve Süreci Seçme
        if running_process is None and ready_queue:
            running_process = ready_queue.pop(0)
            
            # İlk başlama zamanını kaydet ve logla
            if running_process.first_start_time == -1:
                running_process.first_start_time = current_time
                # Loglama: STARTED olayı
                log_event(running_process, current_time, "STARTED", f"Kalan süre: {running_process.burst_time}")

        # 3. Süreç Çalıştırma
        if running_process:
            time_slice = min(quantum, running_process.remaining_time)
            
            i = 0
            while i < time_slice and running_process.remaining_time > 0:
                
                # Gantt kaydını güncelle
                if not gantt_chart or gantt_chart[-1]['pid'] != running_process.pid:
                    gantt_chart.append({'pid': running_process.pid, 'start': current_time, 'end': current_time + 1})
                else:
                    gantt_chart[-1]['end'] = current_time + 1
                    
                running_process.remaining_time -= 1
                current_time += 1
                i += 1
                
                # Çalışma sırasında yeni gelenleri kontrol et
                newly_arrived_in_slice = [p for p in sim_processes if p.arrival_time == current_time and p.remaining_time > 0]
                for p in newly_arrived_in_slice:
                    if p not in ready_queue and not p.is_completed:
                        ready_queue.append(p)

            # 4. Tamamlanma veya Kesinti (Preemption) Kontrolü
            is_completed = (running_process.remaining_time == 0)
            is_preempted = (i == quantum and not is_completed)
            
            if is_completed:
                running_process.completion_time = current_time
                running_process.is_completed = True
                completed_processes.append(running_process)
                # Loglama: COMPLETED olayı
                log_event(running_process, current_time, "COMPLETED", f"Toplam süre: {running_process.burst_time}")
                running_process = None
                
            elif is_preempted:
                ready_queue.append(running_process)
                # Loglama: PREEMPTED olayı
                log_event(running_process, current_time, "PREEMPTED", f"Kalan süre: {running_process.remaining_time}")
                running_process = None
        
        elif not ready_queue:
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


    # Context Switch Sayısını Gantt Verisine Göre Düzeltme
    cs_count_recalculated = 0
    if gantt_chart:
        non_idle_blocks = [d for d in gantt_chart if d['pid'] != 'IDLE']
        if len(non_idle_blocks) > 0:
            cs_count_recalculated = len(non_idle_blocks) - 1

    context_switch_count = cs_count_recalculated
    
    # Metrikleri orijinal süreç listesine kopyala
    for original_p in processes:
        for completed_p in completed_processes:
            if original_p.pid == completed_p.pid:
                original_p.__dict__.update(completed_p.__dict__)

    return processes, gantt_chart, context_switch_count