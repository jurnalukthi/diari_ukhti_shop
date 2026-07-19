# Shopee Affiliate Content Generator Workflow

Workflow otomatisasi pembuatan konten promosi video pendek Shopee Affiliate menggunakan AI dan FFmpeg.

## Panduan Linting & Typecheck
- Script utama: Python 3.x
- Ketergantungan: `requests`, `google-genai`
- Validasi video: `ffmpeg`, `ffprobe`

## Alur Kerja 3 Tahap

### Tahap 1 — Download Poster Asli & Generate Prompt (via opencode)

Minta opencode dengan format:
```
download poster untuk indeks 001: https://url1.jpg https://url2.jpg https://url3.jpg
```

opencode akan otomatis:
1. Download setiap URL → simpan ke `03_aset_produk/001/image1.jpg`, `image2.jpg`, dst.
2. Baca `01_detail_produk/001.txt`
3. Generate 5 prompt DALL-E 3 → simpan ke `05_product_generate/001/prompts.txt`

Syarat: file `01_detail_produk/001.txt` harus sudah ada sebelum request ke opencode.

### Tahap 2 — Generate Poster di ChatGPT (Manual)

1. Buka `05_product_generate/001/prompts.txt`
2. Upload foto referensi yang disebutkan di bagian atas file ke ChatGPT
3. Paste prompt V1–V5 satu per satu
4. Simpan hasil gambar ke folder `05_product_generate/001/` (format: jpg/png/webp)

### Tahap 3 — Generate Video dengan Voiceover

Jalankan `main.py` setelah poster hasil ChatGPT tersimpan di `05_product_generate/001/`.
```bash
python main.py "01_detail_produk/001.txt"
```

Proses otomatis:
1. Membaca deskripsi produk dan mengekstrak meta-data.
2. Menggunakan API `plan-combo` untuk membuat skrip promosi JSON (hook x3, isi, CTA, caption IG & TikTok).
3. Menggunakan API Gemini TTS (`gemini-3.1-flash-tts-preview`) dengan rotasi API Key untuk voiceover (`04_voice_over/001.wav`).
4. Menggabungkan poster dari `05_product_generate/001/` + voiceover menggunakan FFmpeg → video potret 9:16 dengan background blur adaptif, teks marketing di atas, label etalase di bawah.
5. Update halaman web etalase dan push ke GitHub.

*Video siap diunggah tersimpan di `02_konten_affiliate/001/001_<jenis_produk>_<merk_produk>.mp4`.*
