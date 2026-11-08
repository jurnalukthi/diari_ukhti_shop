# Shopee Affiliate Content Generator Workflow

Workflow otomatisasi pembuatan konten promosi video pendek Shopee Affiliate menggunakan AI dan FFmpeg.

## Panduan Linting & Typecheck
- Script utama: Python 3.x
- Ketergantungan: `requests`, `google-genai`
- Validasi video: `ffmpeg`, `ffprobe`

### Aturan Pembuatan Prompt Gambar
- **Model Manusia**: Wajib model wanita Muslimah Indonesia berhijab rapi (Indonesian Muslim woman wearing a neat hijab).
- **Format**: Potret 9:16 (1080x1920px).
- **Produk Bersih / Unbranded**: Hilangkan semua logo, nama merek, dan teks dari kemasan/pakaian.
- **DILARANG Minta AI Gambar Teks/Strip**: Prompt gambar harus bersih tanpa tulisan, logo, strip, atau watermark. Floating strip etalase ditambahkan otomatis via FFmpeg saat render video agar teks tajam dan konsisten.

## Alur Kerja 3 Tahap

### Tahap 1 — Siapkan Aset & Generate Prompt

1. Simpan detail produk ke `01_detail_produk/{indeks}.txt` (baris 1: link affiliate, baris 3 dst: judul & deskripsi).
2. Simpan aset asli ke `03_aset_produk/{indeks}/`:
   - Gambar: `image_01.webp` (atau jpg/png)
   - Video (opsional jika ada): `video_01.mp4`
3. Generate prompt DALL-E 3 bersih (clean photo only) → simpan ke `05_product_generate/{indeks}/prompts.txt`.

### Tahap 2 — Generate Gambar di ChatGPT (Manual)

1. Buka ChatGPT (DALL-E 3).
2. Upload foto referensi dari `03_aset_produk/{indeks}/`.
3. Paste prompt dari `05_product_generate/{indeks}/prompts.txt`.
4. Simpan gambar hasil generate ke `05_product_generate/{indeks}/image_01.png`.

### Tahap 3 — Generate Video dan Update Web

Jalankan proses render setelah gambar poster tersimpan di `05_product_generate/{indeks}/image_01.png`.

#### 1. Pembuatan Skrip & Caption
- API `plan-combo` membuat skrip & caption JSON (caption IG & TikTok, promo_tag, marketing_title) → simpan ke `02_konten_affiliate/{indeks}/`.
- Voiceover tidak diperlukan jika video aset sudah memiliki audio sendiri.

#### 2. Render Video (FFmpeg)
- **Mode Hybrid (Gambar 3 Detik + Video Produk)**:
  - 3 Detik pertama: Gambar poster hasil generate (`05_product_generate/{indeks}/image_01.png`).
  - Lanjutan: Video produk asli (`03_aset_produk/{indeks}/video_01.mp4`).
  - Audio: Audio asli dari video produk dengan delay 3 detik (`adelay=3000|3000`), sinkron saat video mulai (tanpa voiceover).
  - Floating Strip: Box hitam transparan 60% di bawah (`y=1570, h=120`), teks putih centered:
    * Baris 1: `No. Etalase: {indeks}`
    * Baris 2: `Cek link di bio!`
  - Output: `02_konten_affiliate/{indeks}/{indeks}_IG_final.mp4`.
- **Mode Slideshow (Jika aset hanya gambar)**:
  - Concat gambar poster + variasi gambar produk dengan overlay FFmpeg potret 9:16 background blur adaptif.

#### 3. Update Web Etalase & Push GitHub
- `generate_page.py` membaca rekursif semua produk di `01_detail_produk/**/*.txt`.
- Otomatis `git add docs/`, commit, dan push ke GitHub.
