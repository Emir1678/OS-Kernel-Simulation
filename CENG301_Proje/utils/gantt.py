# utils/gantt.py

def generate_ascii_gantt(gantt_data):
    """
    Ham Gantt verisinden ASCII Gantt şeması oluşturur.
    """
    if not gantt_data:
        return "Gantt şeması verisi yok."

    # Sadece geçerli, pozitif uzunluklu blokları al
    filtered_data = [d for d in gantt_data if d['end'] > d['start']]
    if not filtered_data:
        return "Gantt şeması verisi yok (Filtrelenmiş)."

    time_str = "0"
    process_str = ""
    
    last_end = 0

    # Her bir blok için çizim yap
    for segment in filtered_data:
        pid = segment['pid']
        start_t = segment['start']
        end_t = segment['end']
        length = end_t - start_t
        
        # Eğer arada boşluk varsa, Gantt verisi eksik demektir, ama biz var sayıyoruz ki sıralı.

        # Blok içeriği
        if pid == 'IDLE':
            block = " " * length
        else:
            # PID'yi bloğun içine yerleştirme (en az 1 karakter)
            if length >= 3:
                # Blok uzunluğu 3 veya daha fazlaysa PID'yi ortala
                padding_left = max(0, length - len(pid)) // 2
                padding_right = length - len(pid) - padding_left
                block = "-" * padding_left + pid + "-" * padding_right
            elif length == 2:
                # Uzunluk 2 ise: P1 -> -P1
                 block = "-" + pid
            else: # length == 1
                # Uzunluk 1 ise: Sadece PID'nin ilk harfi veya PID
                block = pid 
        
        # Süreç çizimi
        process_str += "|" + block

        # Zaman çizimi
        time_point_label = str(end_t)
        time_str += f"{'':>{len(block)}}{time_point_label}"
        
        last_end = end_t
    
    process_str += "|"
    
    # ASCII çizimini döndür
    gantt_output = (
        f"\n--- 📈 ASCII Gantt Chart ---\n" 
        f"Time: {time_str.strip()}\n"
        f"      {process_str.strip()}"
    )
    return gantt_output