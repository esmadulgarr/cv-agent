import streamlit as st
import os
from pypdf import PdfReader
from groq import Groq

# Sayfa Genişliği ve Estetik Başlık Ayarları
st.set_page_config(page_title="AI CV Analiz Sistemi", page_icon="💼", layout="wide")

st.title("💼 Çift Perspektifli Yapay Zeka CV Analiz Sistemi")
st.markdown("Yapay zeka ajanları özgeçmişinizi hem **İnsan Kaynakları** hem de **Teknik Ekip** gözüyle değerlendirir.")
st.markdown("---")

# API Anahtarı Kontrolü (Colab ortamından veya arayüzden alınabilir)
# Eğer Colab Secrets kullandıysanız buraya otomatik yansır
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    st.sidebar.warning("Lütfen sol menüye Groq API Anahtarınızı girin.")
    GROQ_API_KEY = st.sidebar.text_input("Groq API Key:", type="password")

if GROQ_API_KEY:
    client = Groq(api_key=GROQ_API_KEY)
    GUNCEL_MODEL = "llama-3.3-70b-versatile"

    # Dosya Yükleme Alanı
    uploaded_file = st.file_uploader("Lütfen analiz etmek istediğiniz CV (.pdf) dosyasını sürükleyin veya seçin", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("PDF okunuyor ve metne dönüştürülüyor..."):
            reader = PdfReader(uploaded_file)
            cv_metni = ""
            for page in reader.pages:
                cv_metni += page.extract_text() + "\n"
        
        st.success(f"'{uploaded_file.name}' başarıyla okundu! Analiz başlatılıyor...")

        # Analiz Butonu
        if st.button("Ajanları Çalıştır ve CV'yi Analiz Et"):
            
            # Kolon Tasarımı ile İki Ajanı Yan Yana Gösterme
            col1, col2 = st.columns(2)

            # --- AJAN 1: İK UZMANI ---
            with col1:
                st.subheader("🏢 1. İK ve ATS Uzmanı Değerlendirmesi")
                with st.spinner("İK Ajanı rapor hazırlıyor..."):
                    ik_rolu = (
                        "Sen, dijital yetenek kazanımı ve modern İnsan Kaynakları (ATS - Aday Takip Sistemleri) "
                        "konusunda uzmanlaşmış kıdemli bir İK yöneticisisin. Sana verilen CV metnini sadece bir İK "
                        "gözüyle incelemelisin. Raporda şu 3 başlık kesinlikle olmalı:\n"
                        "1) ATS Uyumluluk Durumu\n"
                        "2) Güçlü ve Geliştirilmesi Gereken Yönler\n"
                        "3) Genel Kurumsal Uyum Değerlendirmesi."
                    )
                    ik_yaniti = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": ik_rolu},
                            {"role": "user", "content": f"Lütfen şu CV metnini analiz et ve Türkçe rapor hazırla:\n\n{cv_metni}"}
                        ],
                        model=GUNCEL_MODEL,
                        temperature=0.2,
                    )
                    st.markdown(ik_yaniti.choices[0].message.content)

            # --- AJAN 2: TECH LEAD ---
            with col2:
                st.subheader("💻 2. Teknik Sorumlu (Tech Lead) Değerlendirmesi")
                with st.spinner("Tech Lead teknik derinliği inceliyor..."):
                    teknik_rol = (
                        "Sen, büyük ölçekli projeleri ve yapay zeka sistemlerini yöneten kıdemli bir Yazılım Takım Liderisin (Tech Lead). "
                        "Sana verilen CV'yi tamamen teknik derinlik, mimari bilgi ve teknoloji kullanımı açısından incelemelisin. "
                        "Raporda şu 3 başlık kesinlikle olmalı:\n"
                        "1) Teknik Yetkinlik Seviyesi Analizi\n"
                        "2) Proje Analizi (Projeleri gerçekçi ve güçlü mü?)\n"
                        "3) Adaya Özel 3 Teknik Mülakat Sorusu ve Kısa Cevap Anahtarı."
                    )
                    teknik_yanit = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": teknik_rol},
                            {"role": "user", "content": f"Lütfen şu CV metnini teknik açıdan analiz et ve Türkçe rapor hazırla:\n\n{cv_metni}"}
                        ],
                        model=GUNCEL_MODEL,
                        temperature=0.3,
                    )
                    st.markdown(teknik_yanit.choices[0].message.content)
            
            st.balloons() # Başarı animasyonu
else:
    st.info("Sistemi kullanabilmek için geçerli bir GROQ_API_KEY tanımlanmış olmalıdır.")
