#!/usr/bin/env python3
"""
caesar_cipher.py

Hybrid mode:
 - Jika dijalankan dengan argumen: tetap berfungsi sebagai CLI (encrypt/decrypt/analyze)
 - Jika dijalankan tanpa argumen: masuk mode interaktif (menu) supaya mudah dipakai tanpa CLI

Usage (CLI):
    python caesar_cipher.py encrypt "Halo Dunia!" 3
    python caesar_cipher.py decrypt "Kdor Gxqld!" 3
    python caesar_cipher.py analyze "Kdor Gxqld!"

If you run:
    python caesar_cipher.py
you'll get an interactive menu.
"""

import sys
import argparse
import string
from collections import Counter

ENGLISH_FREQ = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}

ETAOIN = "ETAOINSHRDLU"  # common letters heuristic


def caesar_shift(text: str, shift: int) -> str:
    shift = shift % 26
    result_chars = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            new_ord = (ord(ch) - base + shift) % 26 + base
            result_chars.append(chr(new_ord))
        else:
            result_chars.append(ch)
    return ''.join(result_chars)


def encrypt(plaintext: str, key: int) -> str:
    if not (1 <= key <= 25):
        raise ValueError("Key harus integer antara 1 dan 25.")
    return caesar_shift(plaintext, key)


def decrypt(ciphertext: str, key: int) -> str:
    if not (1 <= key <= 25):
        raise ValueError("Key harus integer antara 1 dan 25.")
    return caesar_shift(ciphertext, -key)


def letter_counts_only(text: str) -> Counter:
    filtered = [ch.upper() for ch in text if ch.isalpha()]
    return Counter(filtered)


def chi_squared_score(text: str) -> float:
    counts = letter_counts_only(text)
    n = sum(counts.values())
    if n == 0:
        return float('-inf')
    chi2 = 0.0
    for letter, exp_pct in ENGLISH_FREQ.items():
        observed = counts.get(letter, 0)
        expected = exp_pct / 100.0 * n
        chi2 += (observed - expected) ** 2 / expected
    return -chi2


def etaoin_score(text: str) -> float:
    counts = letter_counts_only(text)
    n = sum(counts.values())
    if n == 0:
        return 0.0
    score = sum(counts.get(ch, 0) for ch in ETAOIN)
    return score / n


def combined_score(text: str, weight_etaoin: float = 5.0) -> float:
    chi = chi_squared_score(text)
    eta = etaoin_score(text)
    return chi + weight_etaoin * eta


def analyze(ciphertext: str, top_n: int = 10, show_all: bool = False):
    results = []
    for key in range(0, 26):
        candidate = caesar_shift(ciphertext, -key)
        score = combined_score(candidate)
        results.append((key, candidate, score))

    results.sort(key=lambda t: t[2], reverse=True)

    if show_all:
        for key, cand, sc in results:
            print(f"[key={key:2d}] score={sc:9.3f}  -> {cand}")
    else:
        limit = min(top_n, len(results))
        for i in range(limit):
            key, cand, sc = results[i]
            print(f"[rank {i+1:2d}] key={key:2d}  score={sc:9.3f}  -> {cand}")

    best_key, best_plain, best_score = results[0]
    print("\n=== Best guess ===")
    print(f"Key (encryption shift) = {best_key}")
    print(f"Plaintext candidate      = {best_plain}")
    return results


def build_arg_parser():
    parser = argparse.ArgumentParser(
        prog="caesar_cipher.py",
        description="Caesar Cipher tool: encrypt | decrypt | analyze (brute-force + freq analysis)"
    )
    parser.add_argument("mode", choices=["encrypt", "decrypt", "analyze"],
                        help="Mode operasi")
    parser.add_argument("text", help="Teks (wrap dengan quotes jika mengandung spasi)")
    parser.add_argument("key", nargs='?', type=int,
                        help="Kunci (integer 1-25). Diperlukan untuk encrypt/decrypt.")
    parser.add_argument("--top", type=int, default=10,
                        help="Untuk analyze: tampilkan top N kandidat (default 10)")
    parser.add_argument("--all", action="store_true",
                        help="Untuk analyze: tampilkan semua 26 kandidat")
    return parser


def interactive_menu():
    print("=== Caesar Cipher (Interactive Mode) ===")
    while True:
        print("\nPilih mode:")
        print("1) Encrypt")
        print("2) Decrypt")
        print("3) Analyze (brute-force)")
        print("4) Keluar")
        choice = input("Masukkan pilihan (1-4): ").strip()
        if choice == '1':
            text = input("Masukkan plaintext: ")
            key = input("Masukkan kunci (1-25): ").strip()
            try:
                k = int(key)
                result = encrypt(text, k)
                print("\nHasil (encrypt):")
                print(result)
            except Exception as e:
                print("Error:", e)
        elif choice == '2':
            text = input("Masukkan ciphertext: ")
            key = input("Masukkan kunci (1-25): ").strip()
            try:
                k = int(key)
                result = decrypt(text, k)
                print("\nHasil (decrypt):")
                print(result)
            except Exception as e:
                print("Error:", e)
        elif choice == '3':
            text = input("Masukkan ciphertext untuk dianalisis: ")
            top = input("Tampilkan top N kandidat (enter = 10): ").strip()
            all_flag = input("Tampilkan semua kandidat? (y/N): ").strip().lower()
            try:
                top_n = int(top) if top else 10
            except ValueError:
                top_n = 10
            show_all = (all_flag == 'y')
            analyze(text, top_n=top_n, show_all=show_all)
        elif choice == '4':
            print("Keluar. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid. Coba lagi.")


def main(argv=None):
    # Jika dipanggil tanpa argumen di command line, masuk mode interaktif
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) == 0:
        interactive_menu()
        return

    parser = build_arg_parser()
    args = parser.parse_args(argv)

    mode = args.mode
    text = args.text

    if mode in ("encrypt", "decrypt"):
        if args.key is None:
            parser.error("Mode encrypt/decrypt memerlukan argumen key (1-25).")
        key = args.key
        try:
            if mode == "encrypt":
                result = encrypt(text, key)
            else:
                result = decrypt(text, key)
        except ValueError as e:
            print("Error:", e)
            sys.exit(1)
        print(result)
    else:  # analyze
        analyze(text, top_n=args.top, show_all=args.all)


if __name__ == "__main__":
    main()
