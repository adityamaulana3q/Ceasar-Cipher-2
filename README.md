# Ceasar-Cipher-2
# 🔐 Caesar Cipher — encrypt / decrypt / analyze (hybrid CLI + interaktif)

Program Python sederhana untuk:

* **encrypt** → enkripsi teks (kunci 1–25)
* **decrypt** → dekripsi teks (kunci 1–25)
* **analyze** → brute-force (26 kemungkinan) + analisis frekuensi untuk menebak plaintext terbaik

Program ini bersifat **hybrid**:

* Bila dijalankan dengan argumen → berfungsi sebagai CLI.
* Bila dijalankan tanpa argumen → masuk ke **mode interaktif** (menu).

---

## Fitur

* Menjaga huruf besar/kecil (case-preserving).
* Mengabaikan karakter non-alfabet (angka, spasi, simbol tidak diubah).
* Mode `analyze` menampilkan semua kandidat (atau top N) dan menebak plaintext terbaik dengan:

  * **Chi-squared** terhadap frekuensi huruf bahasa Inggris.
  * Heuristik **ETAOIN SHRDLU** (huruf-huruf umum dalam bahasa Inggris).
  * Gabungan skor untuk menentukan kandidat terbaik.

---

## Persyaratan

* Python 3.6+ (direkomendasikan Python 3.8 atau lebih baru)

---

## Instalasi / Persiapan

1. Clone repository:

```bash
git clone https://github.com/username/caesar-cipher.git
cd caesar-cipher
```

2. Pastikan file `caesar_cipher.py` executable (opsional):

```bash
chmod +x caesar_cipher.py
```

3. Jalankan dengan Python:

```bash
python caesar_cipher.py
```

atau (jika executable):

```bash
./caesar_cipher.py
```

---

## Cara Penggunaan

### A. Mode Interaktif (direkomendasikan untuk pemula)

Jalankan tanpa argumen:

```bash
python caesar_cipher.py
```

Menu interaktif akan muncul:

1. Pilih `1` → **Encrypt**

   * Masukkan plaintext
   * Masukkan kunci (
