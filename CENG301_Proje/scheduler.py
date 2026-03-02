import sys
import os
import argparse
import copy
from typing import List, Dict, Any

# Proje dizinini sisteme ekle
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Modül importları
try:
    from utils.parser import parse_processes, Process
    from algorithms.fcfs import run_fcfs
    from algorithms.sjf import run_sjf
    from algorithms.srtf import run_srtf
    from algorithms.rr import run_rr
    from utils.statistics import (
        print_detailed_statistics, 
        get_summary_statistics, 
        save_comparison_graphs  # Grafik fonksiyonu
    )
    from utils.gantt import generate_ascii_gantt
except ImportError as e:
    print(f"Error: Required modules not found. Detail: {e}")
    sys.exit(1)

def print_execution_log(processes: List[Process]):
    """
    Süreç olaylarını zaman sırasına göre yazdırır.
    """
    all_logs = []
    for p in processes:
        if hasattr(p, 'execution_log'): 
            for log in p.execution_log:
                all_logs.append({
                    'time': log['time'],
                    'pid': p.pid,
                    'event': log['event'],
                    'details': log['details']
                })
            
    all_logs.sort(key=lambda x: (x['time'], x['pid']))

    print("\n==============================================")
    print("📝 EXECUTION LOG (Detailed Timeline)")
    print("==============================================")
    print(f"{'Time':<6} | {'PID':<5} | {'Event'}")
    print("-" * 46)
    
    for log in all_logs:
        details = f" ({log['details']})" if log['details'] else ""
        print(f"{log['time']:<6} | {log['pid']:<5} | {log['event']}{details}")

def run_comparison(input_file: str, quantum: int):
    """
    Tüm algoritmaları çalıştırır, tablo basar ve grafikleri kaydeder.
    """
    try:
        from algorithms.prio_np import run_prio_np
        from algorithms.prio_p import run_prio_p
    except ImportError:
        print("Error: Priority algorithm modules not found.")
        return

    comparison_results = []
    algorithms_to_run = {
        'FCFS': run_fcfs,
        'SJF': run_sjf,
        'SRTF': run_srtf,
        'RR': run_rr,
        'PRIO NP': run_prio_np,
        'PRIO P': run_prio_p,
    }
    
    print("\nRunning all algorithms for comparison...")
    
    for algo_name, run_func in algorithms_to_run.items():
        clean_processes = parse_processes(input_file)
        if algo_name == 'RR':
            completed_procs, _, cs_count = run_func(clean_processes, quantum)
        else:
            completed_procs, _, cs_count = run_func(clean_processes)
        
        summary = get_summary_statistics(completed_procs, algo_name, cs_count)
        comparison_results.append(summary)

    # Karşılaştırma Tablosu
    print("\n=========================================================================")
    print("🏆 ALGORITHM COMPARISON SUMMARY")
    print("=========================================================================")
    header = f"{'ALGORITHM':<10} | {'AVG. TURN.':<12} | {'AVG. WAIT.':<13} | {'AVG. RESP.':<10} | {'CS COUNT'}"
    print(header)
    print("-" * len(header))
    
    for res in comparison_results:
        print(f"{res['Algorithm']:<10} | "
              f"{res['Avg_Turnaround']:<12.2f} | "
              f"{res['Avg_Waiting']:<13.2f} | "
              f"{res['Avg_Response']:<10.2f} | "
              f"{res['Context_Switches']:<9}")
    print("-" * len(header))

    # Matplotlib Grafiklerini Oluştur (Hocanın istediği graphs/ klasörüne)
    save_comparison_graphs(comparison_results)

def main():
    parser = argparse.ArgumentParser(description="CPU Process Scheduling Simulator")
    parser.add_argument('--input', type=str, required=True, help='Path to processes.txt')
    parser.add_argument('--algo', type=str, required=True, 
                        choices=['FCFS', 'SJF', 'SRTF', 'RR', 'PRIO NP', 'PRIO P', 'COMPARE'])
    parser.add_argument('--quantum', type=int, default=2, help='Quantum for RR')
    
    args = parser.parse_args()
    
    if args.algo == 'COMPARE':
        run_comparison(args.input, args.quantum)
        return

    # Tekil Algoritma Modu
    processes = parse_processes(args.input)
    if not processes: sys.exit(1)

    print(f"\n🚀 Starting Simulation: {args.algo}")

    if args.algo == 'FCFS': results = run_fcfs(processes)
    elif args.algo == 'SJF': results = run_sjf(processes)
    elif args.algo == 'SRTF': results = run_srtf(processes)
    elif args.algo == 'RR': results = run_rr(processes, args.quantum)
    elif args.algo == 'PRIO NP':
        from algorithms.prio_np import run_prio_np
        results = run_prio_np(processes)
    elif args.algo == 'PRIO P':
        from algorithms.prio_p import run_prio_p
        results = run_prio_p(processes)

    completed_processes, gantt_data, cs_count = results
    
    print(generate_ascii_gantt(gantt_data))
    print_detailed_statistics(completed_processes, cs_count)
    print_execution_log(completed_processes)

if __name__ == "__main__":
    main()