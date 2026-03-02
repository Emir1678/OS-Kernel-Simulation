# utils/statistics.py

from typing import List, Dict, Any, Tuple
# Process sınıfını, metrik hesaplamaları için import etmeye gerek yok
# çünkü Process nesneleri zaten metrikleri property olarak barındırıyor.

def print_detailed_statistics(processes: List[Any], cs_count: int):
    """
    Her süreç için detaylı metrikleri ve algoritma ortalamalarını yazdırır.
    """
    total_turnaround = sum(p.turnaround_time for p in processes)
    total_waiting = sum(p.waiting_time for p in processes)
    total_response = sum(p.response_time for p in processes)
    num_processes = len(processes)

    print("\n======================================================================")
    print("📊 PER-PROCESS & SUMMARY STATISTICS")
    print("======================================================================")
    
    # Başlık
    print(f"{'PID':<4} {'Arr':<5} {'Burst':<5} {'Compl':<5} {'Turnaround':<11} {'Waiting':<10} {'Response':<8}")
    print("-" * 75)
    
    # Süreç bazlı veriler
    for p in sorted(processes, key=lambda p: p.pid):
        print(
            f"{p.pid:<4} "
            f"{p.arrival_time:<5} "
            f"{p.burst_time:<5} "
            f"{p.completion_time:<5} "
            f"{p.turnaround_time:<11} "
            f"{p.waiting_time:<10} "
            f"{p.response_time:<8}"
        )

    print("-" * 75)

    # Özet istatistikler
    if num_processes > 0:
        avg_turnaround = total_turnaround / num_processes
        avg_waiting = total_waiting / num_processes
        avg_response = total_response / num_processes
        
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Waiting Time:    {avg_waiting:.2f}")
        print(f"Average Response Time:   {avg_response:.2f}")
        print(f"Total Context Switches:  {cs_count}")
    
    print("-" * 75)
    
    
def get_summary_statistics(processes: List[Any], algorithm_name: str, cs_count: int) -> Dict[str, Any]:
    """
    COMPARE modu için sadece özet metrikleri hesaplar ve döndürür.
    """
    num_processes = len(processes)
    
    if num_processes == 0:
        return {
            'Algorithm': algorithm_name,
            'Avg_Turnaround': 0,
            'Avg_Waiting': 0,
            'Avg_Response': 0,
            'Context_Switches': 0
        }

    total_turnaround = sum(p.turnaround_time for p in processes)
    total_waiting = sum(p.waiting_time for p in processes)
    total_response = sum(p.response_time for p in processes)

    return {
        'Algorithm': algorithm_name,
        'Avg_Turnaround': total_turnaround / num_processes,
        'Avg_Waiting': total_waiting / num_processes,
        'Avg_Response': total_response / num_processes,
        'Context_Switches': cs_count
    }
import matplotlib.pyplot as plt
import os

def save_comparison_graphs(results: List[Dict[str, Any]]):
    """Hocanın istediği graphs/ klasörüne PNG çıktılarını kaydeder."""
    if not os.path.exists("graphs"):
        os.makedirs("graphs")
    
    algos = [r['Algorithm'] for r in results]
    wait_times = [r['Avg_Waiting'] for r in results]
    turn_times = [r['Avg_Turnaround'] for r in results]

    # Graph 1: Waiting Time
    plt.figure(figsize=(10, 5))
    plt.bar(algos, wait_times, color='skyblue')
    plt.title('Average Waiting Time vs Algorithm')
    plt.ylabel('Time')
    plt.savefig('graphs/waiting.png')
    plt.close()

    # Graph 2: Turnaround Time
    plt.figure(figsize=(10, 5))
    plt.bar(algos, turn_times, color='salmon')
    plt.title('Average Turnaround Time vs Algorithm')
    plt.ylabel('Time')
    plt.savefig('graphs/turnaround.png')
    plt.close()
    print("\n[SUCCESS] Graphs saved to graphs/ directory.")