# A* Algorithm to Solve Color Mind Puzzle

# Color Mind Puzzle Solver - A* Search Algorithm

Proyek ini adalah implementasi algoritma pencarian **A-Star (A*)** untuk menyelesaikan teka-teki logika dari permainan indie bernama **Color Mind**. [cite_start]Program ini mensimulasikan mekanisme permainan, termasuk pencampuran warna primer menjadi warna sekunder, dan mencari solusi langkah demi langkah secara otomatis[cite: 1, 2].

## 🎮 Tentang Color Mind
[cite_start]Color Mind adalah permainan puzzle berbasis logika di mana pemain harus menyusun balok-balok berwarna untuk mencapai target matriks tertentu[cite: 3, 4]. Fitur unik permainan ini meliputi:
- [cite_start]**Pencampuran Warna**: Warna dapat digabungkan untuk menghasilkan warna baru (contoh: Kuning + Biru = Hijau)[cite: 5, 27].
- [cite_start]**Rotasi Balok**: Balok dapat diputar untuk menyesuaikan dengan slot yang tersedia[cite: 6].
- [cite_start]**Keterbatasan**: Tempat dan jumlah balok yang terbatas menuntut pemikiran sistematis[cite: 7].

## 🧠 Algoritma Penyelesaian
[cite_start]Program ini menggunakan pendekatan **Shortest Path Problem** dengan algoritma **A***[cite: 14, 15]. 

### Fungsi Heuristik
Untuk mempercepat pencarian, digunakan estimasi biaya ($H_n$) dengan perhitungan poin sebagai berikut[cite: 23, 42]:
- **2 Poin**: Jika warna sel sudah tepat sesuai target.
- **1 Poin**: Jika warna sel merupakan komponen warna dasar dari target (membantu akurasi estimasi)[cite: 42, 43].
- **0 Poin**: Jika sel kosong atau salah.

Algoritma akan memprioritaskan *state* dengan nilai heuristik yang paling mendekati solusi[cite: 51].

## 📋 Prasyarat
- **Python 3.12.1** atau versi terbaru[cite: 32].
- Library **NumPy** untuk komputasi matriks[cite: 33, 124].

Instalasi library:
```bash
pip install numpy
