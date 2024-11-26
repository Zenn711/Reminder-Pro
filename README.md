**Reminder Pro**

**Reminder Pro** adalah aplikasi berbasis GUI yang membantu kamu mengatur dan mengingat jadwal harian dengan mudah. Dibangun menggunakan Python, SQLite, dan **ttkbootstrap** untuk desain modern.

---

**Fitur**
- **Tambah Pengingat Baru:** Masukkan judul, deskripsi, tanggal, dan waktu untuk mencatat pengingat.
- **Tandai Pengingat Selesai:** Pengingat yang telah selesai dapat ditandai untuk manajemen yang lebih baik.
- **Hapus Pengingat:** Hapus pengingat yang sudah tidak diperlukan.
- **Pengingat Mendatang:** Daftar pengingat dalam 24 jam ke depan.
- **Notifikasi Otomatis:** Pemberitahuan muncul tepat waktu melalui desktop notification.
- **Desain Modern:** Menggunakan library `ttkbootstrap` untuk tampilan yang bersih dan profesional.

---

**Teknologi yang Digunakan**
- **Bahasa Pemrograman:** Python
- **GUI Framework:** Tkinter + ttkbootstrap
- **Database:** SQLite
- **Library Tambahan:**
  - `plyer` untuk notifikasi desktop
  - `schedule` untuk penjadwalan tugas

---

## Instalasi
### Prasyarat
Pastikan Python sudah terinstal di sistem kamu. Program ini membutuhkan Python versi 3.7 atau lebih baru.

### Langkah Instalasi
1. Clone repositori ini:
   ```bash
   git clone https://github.com/Zenn711/Reminder-Pro.git
   
2. Buat dan aktifkan virtual environment (opsional)
   ```bash
   python -m venv env
   source env/bin/activate # Untuk Linux/Mac
   env\Scripts\activate    # Untuk Windows

3. Install dependensi yang digunakan
   ```bash
   pip install -r requirements.txt

4. Run Aplikasi
   ```bash
   python main.py

