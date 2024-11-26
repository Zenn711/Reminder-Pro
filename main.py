import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import ttkbootstrap as ttk
import threading
import time
from plyer import notification
import schedule

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder Pro")
        self.root.geometry("600x700")
        self.root.configure(bg='#f0f0f0')

        # Tema Modern dengan ttkbootstrap
        style = ttk.Style(theme='flatly')

        # Koneksi Database
        self.conn = sqlite3.connect('reminders.db', check_same_thread=False)
        self.create_table()

        # Variabel Input
        self.judul_var = tk.StringVar()
        self.deskripsi_var = tk.StringVar()
        self.tanggal_var = tk.StringVar()
        self.waktu_var = tk.StringVar()

        # Judul Aplikasi
        self.create_title()
        
        # Tampilan Input
        self.create_input_section()
        
        # Tampilan Daftar Pengingat
        self.create_list_section()

        # Tampilan Pengingat Mendatang
        self.create_upcoming_section()

        # Mulai thread untuk pengecekan pengingat
        self.start_reminder_thread()

    def create_title(self):
        # Frame Judul dengan desain modern
        title_frame = ttk.Frame(self.root, style='primary.TFrame')
        title_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = ttk.Label(
            title_frame, 
            text="Reminder Pro", 
            font=('Arial', 20, 'bold'),
            style='primary.TLabel'
        )
        title_label.pack(pady=10)

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY,
                judul TEXT,
                deskripsi TEXT,
                tanggal TEXT,
                waktu TEXT,
                status TEXT DEFAULT 'Aktif'
            )
        ''')
        self.conn.commit()

    def create_input_section(self):
        # Frame Input dengan desain modern
        input_frame = ttk.LabelFrame(self.root, text="Tambah Pengingat Baru", style='primary.TLabelframe')
        input_frame.pack(fill=tk.X, padx=20, pady=10)

        # Input Judul
        judul_label = ttk.Label(input_frame, text="Judul Pengingat", style='primary.TLabel')    
        judul_label.pack(anchor='w', padx=10, pady=(10,0))
        judul_entry = ttk.Entry(
            input_frame, 
            textvariable=self.judul_var, 
            width=50, 
            font=('Arial', 10)
        )
        judul_entry.pack(padx=10, pady=5)

        # Input Deskripsi
        deskripsi_label = ttk.Label(input_frame, text="Deskripsi", style='primary.TLabel')
        deskripsi_label.pack(anchor='w', padx=10)
        deskripsi_entry = ttk.Entry(
            input_frame, 
            textvariable=self.deskripsi_var, 
            width=50, 
            font=('Arial', 10)
        )
        deskripsi_entry.pack(padx=10, pady=5)

        # Frame Tanggal & Waktu
        datetime_frame = ttk.Frame(input_frame)
        datetime_frame.pack(fill=tk.X, padx=10, pady=5)

        # Input Tanggal
        tanggal_label = ttk.Label(datetime_frame, text="Tanggal (YYYY-MM-DD)", style='primary.TLabel')
        tanggal_label.pack(side=tk.LEFT, padx=(0,5))
        tanggal_entry = ttk.Entry(
            datetime_frame, 
            textvariable=self.tanggal_var, 
            width=15, 
            font=('Arial', 10)
        )
        tanggal_entry.pack(side=tk.LEFT, padx=5)

        # Input Waktu
        waktu_label = ttk.Label(datetime_frame, text="Waktu (HH:MM)", style='primary.TLabel')
        waktu_label.pack(side=tk.LEFT, padx=(10,5))
        waktu_entry = ttk.Entry(
            datetime_frame, 
            textvariable=self.waktu_var, 
            width=10, 
            font=('Arial', 10)
        )
        waktu_entry.pack(side=tk.LEFT, padx=5)

        # Tombol Tambah Pengingat
        tambah_button = ttk.Button(
            input_frame, 
            text="Tambah Pengingat", 
            command=self.tambah_pengingat,
            style='success.TButton'
        )
        tambah_button.pack(pady=10)

    def create_list_section(self):
        # Frame Daftar Pengingat
        list_frame = ttk.LabelFrame(self.root, text="Daftar Pengingat Aktif", style='primary.TLabelframe')
        list_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox Pengingat dengan desain modern
        self.pengingat_listbox = tk.Listbox(
            list_frame, 
            width=50, 
            yscrollcommand=scrollbar.set,
            font=('Arial', 10),
            bg='#ffffff',
            selectbackground='#3498db',
            selectmode=tk.SINGLE
        )
        self.pengingat_listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        scrollbar.config(command=self.pengingat_listbox.yview)

        # Frame Tombol Aksi
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        # Tombol Hapus
        hapus_button = ttk.Button(
            button_frame, 
            text="Hapus Pengingat", 
            command=self.hapus_pengingat,
            style='danger.TButton'
        )
        hapus_button.pack(side=tk.LEFT, padx=5)

        # Tombol Selesai
        selesai_button = ttk.Button(
            button_frame, 
            text="Tandai Selesai", 
            command=self.selesaikan_pengingat,
            style='success.TButton'
        )
        selesai_button.pack(side=tk.LEFT, padx=5)

        # Muat Pengingat Awal
        self.muat_pengingat()

    def create_upcoming_section(self):
        # Frame Pengingat Mendatang
        upcoming_frame = ttk.LabelFrame(self.root, text="Pengingat Mendatang", style='primary.TLabelframe')
        upcoming_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(upcoming_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox Pengingat Mendatang
        self.upcoming_listbox = tk.Listbox(
            upcoming_frame, 
            width=50, 
            yscrollcommand=scrollbar.set,
            font=('Arial', 10),
            bg='#ffffff',
            selectbackground='#3498db',
            selectmode=tk.SINGLE
        )
        self.upcoming_listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        scrollbar.config(command=self.upcoming_listbox.yview)

    def tambah_pengingat(self):
        judul = self.judul_var.get()
        deskripsi = self.deskripsi_var.get()
        tanggal = self.tanggal_var.get()
        waktu = self.waktu_var.get()

        if not judul or not tanggal or not waktu:
            messagebox.showerror("Error", "Judul, Tanggal, dan Waktu harus diisi!")
            return

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO reminders (judul, deskripsi, tanggal, waktu) 
            VALUES (?, ?, ?, ?)
        ''', (judul, deskripsi, tanggal, waktu))
        self.conn.commit()

        # Reset input
        self.judul_var.set('')
        self.deskripsi_var.set('')
        self.tanggal_var.set('')
        self.waktu_var.set('')

        # Muat ulang daftar
        self.muat_pengingat()
        self.muat_pengingat_mendatang()
        
        # Tampilkan notifikasi berhasil
        messagebox.showinfo("Sukses", "Pengingat berhasil ditambahkan!")

    def muat_pengingat(self):
        # Bersihkan listbox
        self.pengingat_listbox.delete(0, tk.END)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE status="Aktif"')
        pengingat = cursor.fetchall()

        for p in pengingat:
            self.pengingat_listbox.insert(tk.END, f"{p[1]} - {p[3]} {p[4]}")

    def muat_pengingat_mendatang(self):
        # Bersihkan listbox pengingat mendatang
        self.upcoming_listbox.delete(0, tk.END)

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE status="Aktif"')
        pengingat = cursor.fetchall()

        # Waktu sekarang
        now = datetime.now()

        # Filter dan tampilkan pengingat dalam 24 jam ke depan
        for p in pengingat:
            try:
                # Parsing tanggal dan waktu
                reminder_datetime = datetime.strptime(f"{p[3]} {p[4]}", "%Y-%m-%d %H:%M")
                
                # Hitung selisih waktu
                time_diff = reminder_datetime - now
                
                # Tampilkan jika kurang dari 24 jam
                if 0 <= time_diff.total_seconds() <= 86400:  # 86400 detik = 24 jam
                    self.upcoming_listbox.insert(tk.END, f"{p[1]} - {p[3]} {p[4]} (dalam {self.format_timedelta(time_diff)})")
            except ValueError:
                # Abaikan jika format tanggal/waktu salah
                pass

    def format_timedelta(self, td):
        # Format selisih waktu dengan cara yang lebih ramah baca
        hours, remainder = divmod(td.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        parts = []
        if td.days > 0:
            parts.append(f"{td.days} hari")
        if hours > 0:
            parts.append(f"{hours} jam")
        if minutes > 0:
            parts.append(f"{minutes} menit")
        
        return " ".join(parts)

    def start_reminder_thread(self):
        # Thread untuk memeriksa dan menampilkan pengingat
        def check_reminders():
            while True:
                # Periksa pengingat setiap menit
                self.check_and_show_reminders()
                time.sleep(60)  # Tunggu 1 menit

        # Jalankan thread sebagai daemon
        reminder_thread = threading.Thread(target=check_reminders, daemon=True)
        reminder_thread.start()

    def check_and_show_reminders(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE status="Aktif"')
        pengingat = cursor.fetchall()

        # Waktu sekarang
        now = datetime.now()

        for p in pengingat:
            try:
                # Parsing tanggal dan waktu
                reminder_datetime = datetime.strptime(f"{p[3]} {p[4]}", "%Y-%m-%d %H:%M")
                
                # Cek jika waktunya sudah tiba (toleransi 1 menit)
                time_diff = reminder_datetime - now
                
                # Tampilkan notifikasi jika waktunya sudah tiba
                if -60 <= time_diff.total_seconds() <= 60:
                    self.tampilkan_notifikasi(p[1], p[2])
            except ValueError:
                # Abaikan jika format tanggal/waktu salah
                pass

    def tampilkan_notifikasi(self, judul, deskripsi):
        # Menampilkan notifikasi sistem
        notification.notify(
            title=judul,
            message=deskripsi,
            app_name="Reminder Pro",
            timeout=10  # Notifikasi akan hilang dalam 10 detik
        )

    def hapus_pengingat(self):
        # Dapatkan indeks yang dipilih
        selected = self.pengingat_listbox.curselection()
        
        if not selected:
            messagebox.showerror("Error", "Pilih pengingat yang ingin dihapus!")
            return

        # Konfirmasi penghapusan
        konfirmasi = messagebox.askyesno("Konfirmasi", "Anda yakin ingin menghapus pengingat ini?")
        if not konfirmasi:
            return

        # Dapatkan data pengingat yang dipilih
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE status="Aktif"')
        pengingat = cursor.fetchall()
        selected_reminder = pengingat[selected[0]]

        # Hapus dari database
        cursor.execute('DELETE FROM reminders WHERE id=?', (selected_reminder[0],))
        self.conn.commit()

        # Muat ulang daftar
        self.muat_pengingat()
        self.muat_pengingat_mendatang()

    def selesaikan_pengingat(self):
        # Dapatkan indeks yang dipilih
        selected = self.pengingat_listbox.curselection()
        
        if not selected:
            messagebox.showerror("Error", "Pilih pengingat yang ingin diselesaikan!")
            return

        # Dapatkan data pengingat yang dipilih
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE status="Aktif"')
        pengingat = cursor.fetchall()
        selected_reminder = pengingat[selected[0]]

# Update status
        cursor.execute('UPDATE reminders SET status="Selesai" WHERE id=?', (selected_reminder[0],))
        self.conn.commit()

        # Muat ulang daftar
        self.muat_pengingat()
        self.muat_pengingat_mendatang()
    
    def create_log_section(self):
        # Frame Log Pengingat
        log_frame = ttk.LabelFrame(self.root, text="Log Pengingat", style='primary.TLabelframe')
        log_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget untuk log
        self.log_text = tk.Text(
            log_frame, 
            width=50, 
            height=10,
            yscrollcommand=scrollbar.set,
            font=('Arial', 10),
            bg='#ffffff',
            wrap=tk.WORD
        )
        self.log_text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        scrollbar.config(command=self.log_text.yview)

        # Tombol Bersihkan Log
        clear_log_button = ttk.Button(
            log_frame, 
            text="Bersihkan Log", 
            command=self.clear_log,
            style='warning.TButton'
        )
        clear_log_button.pack(pady=5)

    def log_reminder(self, pesan):
        # Tambahkan timestamp pada log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {pesan}\n"
        
        # Tambahkan ke text widget log
        self.log_text.insert(tk.END, log_entry)
        
        # Gulir ke bawah secara otomatis
        self.log_text.see(tk.END)

    def clear_log(self):
        # Bersihkan isi log
        self.log_text.delete('1.0', tk.END)

    def check_and_show_reminders(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM reminders WHERE status="Aktif"')
        pengingat = cursor.fetchall()

        # Waktu sekarang
        now = datetime.now()

        for p in pengingat:
            try:
                # Parsing tanggal dan waktu
                reminder_datetime = datetime.strptime(f"{p[3]} {p[4]}", "%Y-%m-%d %H:%M")
                
                # Cek jika waktunya sudah tiba (toleransi 1 menit)
                time_diff = reminder_datetime - now
                
                # Tampilkan notifikasi dan log jika waktunya sudah tiba
                if -60 <= time_diff.total_seconds() <= 60:
                    self.tampilkan_notifikasi(p[1], p[2])
                    
                    # Log pengingat yang sudah waktunya
                    log_message = f"Pengingat: {p[1]} - {p[2]} telah tiba"
                    self.log_reminder(log_message)
            except ValueError:
                # Abaikan jika format tanggal/waktu salah
                pass

def main():
    try:
        root = ttk.Window(themename="flatly")
        app = ReminderApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()