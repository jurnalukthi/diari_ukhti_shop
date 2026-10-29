#!/usr/bin/env python3
import os
import sys
import glob
import json
import subprocess
import main

def main_run():
    indeks = "024"
    gen_dir = f"05_product_generate/{indeks}"
    aset_dir = f"03_aset_produk/{indeks}"
    out_dir = f"02_konten_affiliate/{indeks}"
    vo_dir = "04_voice_over"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(vo_dir, exist_ok=True)

    # 1. Cari gambar hasil generate
    gen_images = sorted(glob.glob(f"{gen_dir}/*.png") + glob.glob(f"{gen_dir}/*.jpg") + glob.glob(f"{gen_dir}/*.webp"))
    if not gen_images:
        print(f"Error: Tidak ada gambar di {gen_dir}. Simpan hasil generate gambar GPT ke folder ini dulu.")
        sys.exit(1)
    
    img_path = gen_images[0]
    vid_path = f"{aset_dir}/video_01.mp4"
    out_path = f"{out_dir}/{indeks}_IG_final.mp4"
    audio_path = f"{vo_dir}/{indeks}.wav"

    if not os.path.exists(vid_path):
        print(f"Error: Video {vid_path} tidak ditemukan.")
        sys.exit(1)

    # 2. Pastikan file voiceover ada, jika belum buat via Gemini TTS
    if not os.path.exists(audio_path):
        skrip_path = f"{out_dir}/{indeks}_jas_hujan_monarki_rainex.txt"
        with open(skrip_path, "r", encoding="utf-8") as f:
            skrip = json.load(f)
        hook = skrip.get("hook_2") or skrip.get("hook_1", "")
        teks_suara = f"{hook} {skrip['isi_suara']} {skrip['cta']}"
        print(f"Membuat Voiceover TTS: {teks_suara[:60]}...")
        main.generate_voiceover(teks_suara, audio_path)

    font_path = "/usr/share/fonts/truetype/lato/Lato-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

    filter_complex = (
        "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v0];"
        "[1:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v1];"
        "[v0][v1]concat=n=2:v=1:a=0[vcat];"
        f"[vcat]drawbox=x=0:y=1570:w=1080:h=120:color=black@0.6:t=fill,"
        f"drawtext=fontfile='{font_path}':text='No. Etalase\\: {indeks}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=1585,"
        f"drawtext=fontfile='{font_path}':text='Cek link di bio!':fontcolor=white:fontsize=42:x=(w-text_w)/2:y=1640[vout];"
        "[1:a]adelay=3000|3000,volume=0.2[bgm];"
        "[2:a]volume=1.2[vo];"
        "[bgm][vo]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", "3", "-i", img_path,
        "-i", vid_path,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-t", "40",
        out_path
    ]

    print(f"Menggabungkan {img_path} (3s) + {vid_path} + Voiceover ({audio_path})...")
    subprocess.run(cmd, check=True)
    print(f"Video selesai: {out_path}")

    # Update web
    print("Memperbarui daftar barang di web...")
    subprocess.run(["python3", "generate_page.py"], check=True)
    print("Selesai!")

if __name__ == "__main__":
    main_run()
