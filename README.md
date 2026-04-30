# 📊 E-Commerce Apparel Sales & Profitability Analysis

**Link Interaktif Dashboard:** [Masukkan Link Power BI kamu di sini]

## 📌 Latar Belakang Bisnis
Perusahaan ritel *apparel* menghadapi tantangan dalam melacak efisiensi operasional dan profitabilitas dari berbagai kategori produk dan metode pengiriman. Proyek ini bertujuan untuk menganalisis data transaksi selama 2023-2025 guna menemukan pola penjualan dan potensi kebocoran pendapatan.

## 🛠️ Tools & Proses (Data Preparation)
- **Python (Pandas):** Digunakan untuk manipulasi data awal.
- **Data Cleaning:** Menangani *missing values* pada metode pembayaran dan diskon.
- **Fuzzy Matching (thefuzz):** Mengotomatisasi standardisasi ratusan data nama kota (Shipping_City) yang *typo* dengan akurasi kemiripan >80%.
- **Microsoft Power BI:** Membangun visualisasi interaktif dan metrik bisnis.

## 💡 Key Insights (Temuan Utama)
1. **Metode Pembayaran & Retur:** Pembayaran melalui opsi *[Sebutkan Metodenya]* menyumbang tingkat pembatalan tertinggi sebesar *[X]%*.
2. **Produk Bintang:** Kategori *[Sebutkan Produk]* menghasilkan *Net Sales* tertinggi meskipun volume transaksinya bukan yang terbanyak.
3. **Puncak Transaksi:** Terdapat lonjakan signifikan pada pesanan di jam *[Sebutkan Jam]* dan bulan *[Sebutkan Bulan]*, menunjukkan perilaku musiman konsumen.

## 🎯 Rekomendasi AksiBisnis
- **Evaluasi Metode COD:** Mempertimbangkan untuk membatasi opsi COD pada wilayah dengan tingkat retur historis tertinggi untuk menekan *shipping cost* yang terbuang.
- **Optimalisasi Stok:** Meningkatkan produksi dan kampanye pemasaran untuk kategori *[Sebutkan Produk]* menjelang bulan *[Sebutkan Bulan]* untuk memaksimalkan margin keuntungan.