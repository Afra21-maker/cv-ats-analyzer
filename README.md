AI-Powered Career Intelligence, ATS & Interview Platform

Bu platform, BT (Bilişim Teknolojileri) sektöründe kariyer hedefleyen adayların özgeçmişlerini (CV) kurumsal standartlarda analiz eden, yapay zeka destekli ve veritabanı entegrasyonlu bir **ATS (Applicant Tracking System) Uyumluluk ve Kariyer Yol Haritası** uygulamasıdır.

Proje; katmanlı mimari prensiplerine uygun olarak, dinamik LLM servislerini ilişkisel bir veritabanı mimarisiyle harmanlayarak adayın yetenek haritasını çıkarır ve mülakat simülasyonları sunar.

---

 Kullanılan Teknolojiler ve Tercih Sebepleri

Projenin mimarisi, yüksek performans, veri tutarlılığı ve modülerlik (Separation of Concerns) hedeflenerek tasarlanmıştır.

### 1. Backend & Veritabanı Katmanı
* **FastAPI (Python):** Asenkron (async/await) yapısı, yüksek performansı ve veri doğrulamadaki (Pydantic) kararlılığı nedeniyle backend çekirdeği olarak tercih edilmiştir.
* **SQLite (`sql_app.db`):** Uygulamanın verilerini yerelde güvenli, hafif ve ilişkisel bir modelde saklamak için entegre edilmiş dosya tabanlı SQL veritabanıdır.
* **SQLAlchemy ORM:** Veritabanı işlemlerini ham SQL sorguları yazmak yerine, nesne yönelimli (Object-Relational Mapping) olarak yönetmek amacıyla kullanılmıştır. 
    * `SessionLocal` ile her istek için temiz veritabanı oturumları (sessions) üretilir.
    * `get_db()` fonksiyonu ile FastAPI'nin **Dependency Injection (Bağımlılık Enjeksiyonu)** mekanizması kullanılarak, veritabanı bağlantıları işlem bittiğinde otomatik kapatılır (Memory Leak önlenir).

### 2. Yapay Zeka Katmanı (AI Layer)
* **Google Gemini API (`gemini-2.5-flash`):** Yüksek hızı ve bağlamsal analiz yeteneği nedeniyle tercih edilmiştir. 
* **Structured JSON Outputs:** Gemini API çağrılarında `response_mime_type="application/json"` formatı zorunlu kılınarak, modelin frontend katmanını kıracak düz metinler yerine doğrudan işlenebilir JSON Array mimarisi dönmesi garantilenmiştir.

### 3. Presentation Katmanı (Ön Yüz)
* **HTML5 & Modern JavaScript (ES6+):** Harici kütüphane yükü olmadan, `fetch` API aracılığıyla backend ile tamamen asenkron (anlık) haberleşen saf JavaScript mimarisi kurulmuştur.
* **Tailwind CSS:** Modern, responsive ve cyberpunk temalı (`glassmorphism` efektli) görsel arayüz tasarımı için kullanılmıştır.

---

## Proje Klasör Mimarisi (Architectural Directory Structure)

Proje, kod karmaşasını önlemek ve modülerliği sağlamak adına kurumsal standartlarda katmanlandırılmıştır:

```text
backend/
│
├── database.py             ➔ Veritabanı Bağlantı ve Oturum Yönetimi (SQLAlchemy / SQLite)
│
├── services/               ➔ İş Mantığı ve Yapay Zeka Katmanı (Business Logic Layer)
│   └── interview.py        ➔ Gemini prompt yönetimi, mülakat soru ve cevap motoru.
│
├── templates/              ➔ Sunum ve Ön Yüz Katmanı (Presentation Layer)
│   └── index.html          ➔ UI bileşenleri, Tailwind CSS ve Asenkron JS köprüleri.
│
└── app.py                  ➔ Uygulama Giriş Kapısı (Application Router & Entry Point)
                            ➔ API endpoint'lerini yönetir, veritabanı oturumlarını bağlar.

SQLAlchemy & Veritabanı Yönetimi
Uygulama, gücünü sadece anlık API çağrılarından almaz; kalıcı bir veri katmanına sahiptir. database.py altındaki Base = declarative_base() iskeleti sayesinde veriler ilişkisel tablolarda modellenir. get_db bileşeni sayesinde veri tabanı kapıları güvenli bir yaşam döngüsüyle (context manager mantığıyla) açılıp kapanır.

2. AI Recruiter Mülakat Bankası & Accordion Modeli
Seçilen domaine özel olarak Gemini tarafından kurumsal elenme oranı yüksek (%85) 3 adet teknik senaryo sorusu üretilir. Eğitim odaklı mimari gereği, her sorunun altına entegre edilen 💡 İdeal Cevabı Gör butonu (Accordion Yapısı) sayesinde aday, yapay zekanın o soru için ürettiği 100 puanlık ideal kıdemli mühendis yanıtını anında görerek kendini eğitebilir.

3. AI ATS Analyzer & Yol Haritası
Yüklenen CV verilerini analiz eden ATS motoru, adayın eksik kelimelerini (keywords) çıkarır, genel bir uyumluluk skoru hesaplar ve bunu dinamik grafik arayüzüyle kullanıcıya sunar.

 Hata Toleransı ve Dayanıklılık (Fault Tolerance)
Sistem mimarisinde kesintisiz kullanıcı deneyimi esastır. Bu doğrultuda uygulamaya Fallback (Yedek Veri) Mekanizması entegre edilmiştir. API kotalarının dolması, internet kesintileri veya modelin yanıt geciktirmesi durumunda try-except blokları devreye girer. Sistem jüri önünde veya canlıda çökmek (500 Internal Server Error) yerine, veritabanı/kod seviyesindeki hazır kurumsal yedek senaryoları anında ekrana basarak sunum sürekliliğini korur.

Sistemi Yerelde Ayağa Kaldırma (Installation)
Projeyi bilgisayarınıza indirin ve backend klasörüne girin:

Bash
cd backend
Gerekli tüm bağımlılıkları ve veritabanı sürücülerini yükleyin:

Bash
pip install fastapi uvicorn google-genai jinja2 python-multipart sqlalchemy
FastAPI sunucusunu hot-reload (canlı izleme) moduyla başlatın:

Bash
python -m uvicorn app:app --reload
Tarayıcınızdan uygulamaya erişin:

Plaintext
[http://127.0.0.1:8000](http://127.0.0.1:8000)
