# utils/parser.py

import sys
from typing import List, Dict, Any

class Process:
    """
    CPU zamanlama simülasyonu için bir süreci temsil eder.
    """
    def __init__(self, pid, arrival_time, burst_time, priority=0):
        self.pid = pid                    
        self.arrival_time = arrival_time  
        self.burst_time = burst_time      
        self.priority = priority          

        # Simülasyon sırasında değişen durumlar
        self.remaining_time = burst_time  
        self.is_completed = False         
        
        # Metrikler
        self.completion_time = -1         
        self.first_start_time = -1        

        # Loglama ve Çıktı için
        self.execution_log: List[Dict[str, Any]] = [] 

    # Metrik hesaplama özellikleri (@property)
    @property
    def turnaround_time(self):
        """Geri dönüş süresi: Tamamlanma Zamanı - Varış Zamanı"""
        if self.completion_time != -1:
            return self.completion_time - self.arrival_time
        return -1

    @property
    def waiting_time(self):
        """Bekleme süresi: Geri Dönüş Süresi - Burst Süresi"""
        tt = self.turnaround_time
        if tt != -1:
            return tt - self.burst_time
        return -1
        
    @property
    def response_time(self):
        """Yanıt süresi: İlk Başlama Zamanı - Varış Zamanı"""
        if self.first_start_time != -1:
            return self.first_start_time - self.arrival_time
        return -1

    def __repr__(self):
        return f"Process(PID={self.pid}, Arr={self.arrival_time}, Burst={self.burst_time}, Rem={self.remaining_time})"


def parse_processes(file_path: str) -> List[Process]:
    """
    Giriş dosyasını okur ve Process nesneleri listesini döndürür.
    Dosya formatı: PID, Varış Zamanı, Burst Süresi, [Öncelik] (Virgülle ayrılmış)
    """
    processes: List[Process] = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # YORUM TEMİZLİĞİ: İlk # işaretinden sonrasını yok say
                if '#' in line:
                    line = line.split('#')[0]
                
                line = line.strip() # Yorum temizlendikten sonra baştaki/sondaki boşlukları temizle
                if not line:
                    continue
                
                parts = line.split(',') # Virgülle ayırma
                
                if len(parts) < 3:
                     print(f"Hata: Geçersiz süreç formatı veya eksik bilgi: '{line.strip()}'", file=sys.stderr)
                     continue

                try:
                    pid = parts[0].strip()
                    arrival_time = int(parts[1].strip())
                    burst_time = int(parts[2].strip())
                    
                    # Öncelik değerini alırken ekstra boşlukları temizle
                    priority = int(parts[3].strip()) if len(parts) > 3 else 0
                    
                    processes.append(Process(pid, arrival_time, burst_time, priority))
                except ValueError as e:
                    print(f"Hata: Sayısal dönüştürme hatası '{line.strip()}' -> {e}", file=sys.stderr)
                    continue

        if not processes:
            print("Hata: Giriş dosyasında geçerli süreç bulunamadı.", file=sys.stderr)
            return []

    except FileNotFoundError:
        print(f"Hata: Giriş dosyası bulunamadı: {file_path}", file=sys.stderr)
        return []
        
    return processes


# ----------------------------------------------------------------------
# Loglama Fonksiyonu (Path sorunlarını çözmek için buraya taşınmıştır)
# ----------------------------------------------------------------------
def log_event(process: Process, current_time: int, event_type: str, details: str = ""):
    """
    Belirli bir süreç için olay kaydı ekler.
    Artık utils.logger yerine utils.parser'dan çağrılacaktır.
    """
    # Süreç nesnesinin execution_log listesine yeni olay kaydını ekler.
    process.execution_log.append({
        'time': current_time,
        'event': event_type,
        'details': details
    })