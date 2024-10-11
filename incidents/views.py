from django.shortcuts import render
import pandas as pd
import random

# Excel'den veri çekme fonksiyonu (sadece ay ve yıl bazında rastgele seçim)
def get_random_incident_by_month(month):
    # Excel dosyasını yükle (dosya yolunu ayarla)
    df = pd.read_excel('cyber_events.xlsx')

    # Yıl bilgilerini çekelim
    df['Year'] = pd.to_datetime(df['Date'], errors='coerce').dt.year
    df['Month'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%B')

    # Seçilen aya göre veriyi filtrele
    incidents = df[df['Month'] == month]
    
    # Eğer o ayda bir olay varsa rastgele birini seç, yoksa boş döndür
    if not incidents.empty:
        selected_incident = incidents.sample().iloc[0]  # Rastgele bir satır seç
        # Olay bilgisi: Yıl Excel'den, ay kullanıcıdan alınacak
        incident_text = f"{selected_incident['Year']}, the incident was: {selected_incident['Event']}"
        return incident_text
    return "No incidents found for this month."

# HTML formunu ve sonucu işleyen görünüm fonksiyonu
def show_incident(request):
    incident = None
    if request.method == 'POST':
        day = request.POST.get('day')  # Kullanıcının seçtiği gün
        month = request.POST.get('month')  # Kullanıcının seçtiği ay
        
        if month and day:
            # Excel'den olay bilgisi alınır, sadece yıl alınır ve metinde gösterilir
            incident = get_random_incident_by_month(month)
            # Kullanıcıdan alınan gün ve ay bilgisiyle olay metni
            incident = f"On {day} {month} {incident}"
    
    return render(request, 'incident.html', {'incident': incident})
