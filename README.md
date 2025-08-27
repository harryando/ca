# Streamlit App: Backdoor Listing and Corporate Actions Scanner
 ---------------------------------------------------------------
# Fitur utama:
# - Mengumpulkan berita dari Google News (RSS) berbasis kata kunci Indonesia
# - Menyaring berdasarkan rentang tanggal & kategori aksi korporasi
# - Ekstraksi kandidat ticker emiten (3–4 huruf, contoh: BBCA, TLKM, CUAN)
# - Skor kecurigaan per emiten + daftar bukti (tautan berita)
# - Tampilan ringkas (tabel) + detail per emiten
# - Ekspor hasil ke CSV
#
# Catatan:
# - Ini *detektor rumor* (bukan konfirmasi resmi). Selalu verifikasi ke sumber resmi (IDX/OJK/Emiten).
# - Akses internet diperlukan ketika aplikasi berjalan (untuk mengambil RSS Google News dan artikel).
# - Instal dependensi di environment Anda: pip install streamlit feedparser pandas requests beautifulsoup4 python-dateutil tldextract
#
# Menjalankan:
#   streamlit run scanner.py

Cara jalan lokal: pip3 install -r requirements.txt → streamlit run scanner.py
