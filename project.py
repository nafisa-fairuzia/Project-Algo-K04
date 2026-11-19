import pandas as pd

harga = [
    ["Plastik", 3000],
    ["Kertas", 2000],
    ["Kardus", 2500],
    ["Kaleng/Logam", 5000],
    ["Botol Kaca", 1000]
]

# Daftar sembako yang bisa ditukar dengan poin
sembako = [
    ["Beras 1 kg", 100],
    ["Minyak Goreng 1 Liter", 200],
    ["Gula Pasir 1 kg", 120],
    ["Mie Instan 1 bungkus", 25],
    ["Telur Ayam 1 kg", 150],
    ["Tepung Terigu 1 kg", 80],
    ["Garam 500 gram", 30]
]

# Login petugas, 2 role: admin dan petugas
# admin: admin / 123456 (semua menu)
# petugas: petugas / 111111 (tanpa ubah dan hapus)
def login():
    kesempatan = 3
    while kesempatan > 0:
        username = input("Username : ")
        password = input("Password : ")
        if password.isdigit() == False:
            print("Password harus angka.")
            kesempatan = kesempatan - 1
            print("Sisa kesempatan:", kesempatan)
        elif username == "admin" and password == "123456":
            print("Login berhasil. Selamat datang, admin.")
            return "admin"
        elif username == "petugas" and password == "111111":
            print("Login berhasil. Selamat datang, petugas.")
            return "petugas"
        else:
            kesempatan = kesempatan - 1
            print("Username atau password salah. Sisa kesempatan:", kesempatan)
    print("Login gagal 3 kali. Program berhenti.")
    exit()

def muat_data():
    try:
        data = pd.read_csv("bank_sampah.csv")
    except FileNotFoundError:
        data = pd.DataFrame([
            ["Budi", "Plastik", 5, 50, 15000],
            ["Siti", "Kertas", 8, 80, 16000],
            ["Andi", "Kardus", 4, 40, 10000],
            ["Dewi", "Kaleng/Logam", 3, 30, 15000],
            ["Rizky", "Botol Kaca", 10, 100, 10000],
            ["Budi", "Kertas", 6, 60, 12000],
            ["Siti", "Plastik", 7, 70, 21000],
            ["Andi", "Kaleng/Logam", 2, 20, 10000],
            ["Dewi", "Kardus", 9, 90, 22500],
            ["Rizky", "Plastik", 12, 120, 36000]
        ], columns=["Nama", "Jenis", "Berat", "Poin", "Rupiah"])
        data.to_csv("bank_sampah.csv", index=False)
    return data

def muat_bayar():
    try:
        data_bayar = pd.read_csv("pembayaran.csv")
    except FileNotFoundError:
        data_bayar = pd.DataFrame([], columns=["Nama", "Jumlah", "Metode"])
    return data_bayar

def muat_tukar():
    try:
        data_tukar = pd.read_csv("penukaran.csv")
    except FileNotFoundError:
        data_tukar = pd.DataFrame([], columns=["Nama", "Sembako", "Poin"])
    return data_tukar

def tampilkan_data(data):
    for i in range(len(data)):
        baris = data.iloc[i]
        print(f"{i + 1}. {baris['Nama']} - {baris['Jenis']} - {baris['Berat']} kg - {baris['Poin']} poin - Rp{baris['Rupiah']}")

def tampil_menu(peran):
    print("===== BANK SAMPAH =====")
    print("1. Tampilkan semua setoran")
    print("2. Tambah setoran")
    if peran == "admin":
        print("3. Ubah setoran")
        print("4. Hapus setoran")
    print("5. Cari setoran")
    print("6. Urutkan setoran")
    print("7. Laporan saldo nasabah")
    print("8. Pembayaran nasabah")
    print("9. Tukar poin")
    print("10. Keluar")

def tampilkan(data):
    print("=== DATA SETORAN ===")
    if len(data) == 0:
        print("Belum ada data setoran.")
    else:
        tampilkan_data(data)

def tambah(data, harga):
    print("=== TAMBAH SETORAN ===")
    nama = input("Nama nasabah : ")
    if nama == "":
        print("Nama tidak boleh kosong.")
        return
    if nama.replace(" ", "").isalpha() == False:
        print("Nama hanya boleh huruf.")
        return
    print("Jenis sampah:")
    for i in range(len(harga)):
        print(f"{i + 1}. {harga[i][0]} - Rp{harga[i][1]}/kg")
    pilih_jenis = input("Pilih jenis (1-5): ")
    if pilih_jenis not in ["1", "2", "3", "4", "5"]:
        print("Pilihan jenis tidak valid.")
        return
    jenis = harga[int(pilih_jenis) - 1][0]
    harga_kg = harga[int(pilih_jenis) - 1][1]
    while True:
        berat_teks = input("Berat (kg) : ")
        try:
            berat = float(berat_teks)
        except:
            print("Berat harus angka.")
            continue
        if berat <= 0:
            print("Berat harus lebih dari 0.")
        elif berat > 50:
            print("Berat maksimal 50 kg per setoran, pecah jadi beberapa setoran.")
        else:
            break
    poin = int(berat * 10)
    rupiah = int(berat * harga_kg)
    data.loc[len(data)] = [nama, jenis, berat, poin, rupiah]
    data.to_csv("bank_sampah.csv", index=False)
    print("=== RINGKASAN SETORAN ===")
    print("Nama   :", nama)
    print("Jenis  :", jenis)
    print("Berat  :", berat, "kg")
    print("Poin   :", poin)
    print("Rupiah : Rp", rupiah)
    print("Data berhasil disimpan.")

def ubah(data, harga, peran):
    print("=== UBAH SETORAN ===")
    if peran != "admin":
        print("Hanya admin yang bisa mengubah data.")
        return
    if len(data) == 0:
        print("Belum ada data setoran.")
    else:
        tampilkan_data(data)
        nomor_teks = input("Nomor setoran yang diubah: ")
        try:
            nomor = int(nomor_teks)
        except:
            nomor = 0
        if nomor < 1 or nomor > len(data):
            print("Nomor tidak ditemukan.")
        else:
            lama = data.iloc[nomor - 1]
            print("Data lama:", lama["Nama"], "-", lama["Jenis"], "-", lama["Berat"], "kg -", lama["Poin"], "poin - Rp", lama["Rupiah"])
            nama_baru = input("Nama baru (kosongkan kalau tidak diubah): ")
            print("Jenis sampah:")
            for i in range(len(harga)):
                print(f"{i + 1}. {harga[i][0]} - Rp{harga[i][1]}/kg")
            jenis_baru = input("Jenis baru (0 kalau tidak diubah): ")
            berat_baru_teks = input("Berat baru (kosongkan kalau tidak diubah): ")
            if nama_baru != "":
                if nama_baru.replace(" ", "").isalpha() == False:
                    print("Nama baru hanya boleh huruf, nama tidak diubah.")
                else:
                    data.loc[nomor - 1, "Nama"] = nama_baru
            if jenis_baru == "" or jenis_baru == "0":
                pass
            elif jenis_baru in ["1", "2", "3", "4", "5"]:
                data.loc[nomor - 1, "Jenis"] = harga[int(jenis_baru) - 1][0]
            else:
                print("Pilihan jenis tidak valid, jenis tidak diubah.")
            if berat_baru_teks != "":
                try:
                    berat_baru = float(berat_baru_teks)
                except:
                    berat_baru = -1
                if berat_baru <= 0 or berat_baru > 50:
                    print("Berat baru tidak valid, berat tidak diubah.")
                else:
                    data.loc[nomor - 1, "Berat"] = berat_baru
            harga_kg = 0
            for i in range(len(harga)):
                if harga[i][0] == data.loc[nomor - 1, "Jenis"]:
                    harga_kg = harga[i][1]
            if harga_kg == 0:
                print("Peringatan: jenis sampah tidak dikenali, poin dan rupiah tidak dihitung ulang.")
            else:
                data.loc[nomor - 1, "Poin"] = int(data.loc[nomor - 1, "Berat"] * 10)
                data.loc[nomor - 1, "Rupiah"] = int(data.loc[nomor - 1, "Berat"] * harga_kg)
            data.to_csv("bank_sampah.csv", index=False)
            print("Data berhasil diubah.")

def hapus(data, peran):
    print("=== HAPUS SETORAN ===")
    if peran != "admin":
        print("Hanya admin yang bisa menghapus data.")
        return data
    if len(data) == 0:
        print("Belum ada data setoran.")
    else:
        tampilkan_data(data)
        nomor_teks = input("Nomor setoran yang dihapus: ")
        try:
            nomor = int(nomor_teks)
        except:
            nomor = 0
        if nomor < 1 or nomor > len(data):
            print("Nomor tidak ditemukan.")
        else:
            hapus_data = data.iloc[nomor - 1]
            print("Data yang dihapus:", hapus_data["Nama"], "-", hapus_data["Jenis"], "-", hapus_data["Berat"], "kg -", hapus_data["Poin"], "poin - Rp", hapus_data["Rupiah"])
            yakin = input("Yakin hapus? (y/n): ")
            if yakin == "y":
                data = data.drop(nomor - 1).reset_index(drop=True)
                data.to_csv("bank_sampah.csv", index=False)
                print("Data berhasil dihapus.")
            else:
                print("Penghapusan dibatalkan.")
    return data

def cari(data):
    print("=== CARI SETORAN ===")
    kata = input("Masukkan nama nasabah atau jenis sampah: ")
    ketemu = False
    for i in range(len(data)):
        if kata.lower() in str(data.iloc[i, 0]).lower() or kata.lower() in str(data.iloc[i, 1]).lower():
            baris = data.iloc[i]
            print(f"{i + 1}. {baris['Nama']} - {baris['Jenis']} - {baris['Berat']} kg - {baris['Poin']} poin - Rp{baris['Rupiah']}")
            ketemu = True
    if ketemu == False:
        print("Data tidak ditemukan.")

def urutkan(data):
    print("=== URUTKAN SETORAN ===")
    print("1. Berat (terbesar ke terkecil)")
    print("2. Rupiah (terbesar ke terkecil)")
    urut = input("Pilih urutan (1-2): ")
    if urut == "1":
        kolom = 2
    elif urut == "2":
        kolom = 4
    else:
        kolom = -1
        print("Pilihan tidak valid.")
    if kolom != -1:
        for i in range(len(data)):
            for j in range(len(data) - 1 - i):
                if data.iloc[j, kolom] < data.iloc[j + 1, kolom]:
                    temp = data.iloc[j].tolist()
                    data.iloc[j] = data.iloc[j + 1].tolist()
                    data.iloc[j + 1] = temp
        print("Data berhasil diurutkan.")
        print("Catatan: urutan ini tidak disimpan ke file dan akan kembali seperti semula saat program dibuka ulang.")
        tampilkan_data(data)

def laporan(data):
    print("=== LAPORAN SALDO NASABAH ===")
    nama = input("Nama nasabah : ")
    total_setoran = 0
    total_berat = 0
    total_poin = 0
    total_rupiah = 0
    for i in range(len(data)):
        if str(data.iloc[i, 0]).lower() == nama.lower():
            total_setoran = total_setoran + 1
            total_berat = total_berat + data.iloc[i, 2]
            total_poin = total_poin + data.iloc[i, 3]
            total_rupiah = total_rupiah + data.iloc[i, 4]
    if total_setoran == 0:
        print("Nasabah tidak ditemukan.")
    else:
        print("Nama nasabah :", nama)
        print("Jumlah setoran:", total_setoran)
        print("Total berat   :", total_berat, "kg")
        print("Total poin    :", total_poin)
        print("Total rupiah  : Rp", total_rupiah)

def bayar(data, data_bayar):
    print("=== PEMBAYARAN NASABAH ===")
    nama = input("Nama nasabah : ")
    total_rupiah = 0
    for i in range(len(data)):
        if str(data.iloc[i, 0]).lower() == nama.lower():
            total_rupiah = total_rupiah + data.iloc[i, 4]
    total_bayar = 0
    for i in range(len(data_bayar)):
        if str(data_bayar.iloc[i, 0]).lower() == nama.lower():
            total_bayar = total_bayar + data_bayar.iloc[i, 1]
    sisa = total_rupiah - total_bayar
    ditemukan = any(str(data.iloc[i, 0]).lower() == nama.lower() for i in range(len(data)))
    if not ditemukan:
        print("Nasabah tidak ditemukan.")
    elif sisa <= 0:
        print("Saldo nasabah sudah lunas.")
    else:
        print("Nama nasabah :", nama)
        print("Total saldo   : Rp", total_rupiah)
        print("Sudah dibayar : Rp", total_bayar)
        print("Sisa saldo    : Rp", sisa)
        jumlah_teks = input("Jumlah dibayar (Rp): ")
        if jumlah_teks.isdigit() == False:
            print("Jumlah harus angka.")
        elif int(jumlah_teks) <= 0:
            print("Jumlah harus lebih dari 0.")
        elif int(jumlah_teks) > sisa:
            print("Jumlah melebihi sisa saldo.")
        else:
            jumlah = int(jumlah_teks)
            print("Metode pembayaran:")
            print("1. Tunai")
            print("2. Transfer")
            metode_pilih = input("Pilih metode (1-2): ")
            if metode_pilih == "1":
                metode = "Tunai"
            elif metode_pilih == "2":
                metode = "Transfer"
            else:
                print("Metode tidak valid, pembayaran dibatalkan.")
                metode = ""
            if metode != "":
                data_bayar.loc[len(data_bayar)] = [nama, jumlah, metode]
                data_bayar.to_csv("pembayaran.csv", index=False)
                print("=== BUKTI PEMBAYARAN ===")
                print("Nama nasabah :", nama)
                print("Jumlah bayar : Rp", jumlah)
                print("Metode       :", metode)
                print("Sisa saldo   : Rp", sisa - jumlah)
                print("Pembayaran berhasil disimpan.")

def tukar_poin(data, data_tukar, sembako):
    print("=== TUKAR POIN ===")
    nama = input("Nama nasabah : ")
    total_poin = 0
    for i in range(len(data)):
        if str(data.iloc[i, 0]).lower() == nama.lower():
            total_poin = total_poin + data.iloc[i, 3]
    total_tukar = 0
    for i in range(len(data_tukar)):
        if str(data_tukar.iloc[i, 0]).lower() == nama.lower():
            total_tukar = total_tukar + data_tukar.iloc[i, 2]
    sisa = total_poin - total_tukar
    ditemukan = any(str(data.iloc[i, 0]).lower() == nama.lower() for i in range(len(data)))
    if not ditemukan:
        print("Nasabah tidak ditemukan.")
    elif sisa <= 0:
        print("Poin nasabah sudah habis.")
    else:
        print("Nama nasabah :", nama)
        print("Total poin    :", total_poin)
        print("Sudah ditukar :", total_tukar, "poin")
        print("Sisa poin     :", sisa, "poin")
        print("Daftar sembako:")
        for i in range(len(sembako)):
            print(f"{i + 1}. {sembako[i][0]} - {sembako[i][1]} poin")
        pilih_teks = input("Pilih sembako (1-7): ")
        if pilih_teks not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("Pilihan tidak valid.")
        else:
            barang = sembako[int(pilih_teks) - 1][0]
            harga_poin = sembako[int(pilih_teks) - 1][1]
            if harga_poin > sisa:
                print("Poin tidak cukup.")
            else:
                data_tukar.loc[len(data_tukar)] = [nama, barang, harga_poin]
                data_tukar.to_csv("penukaran.csv", index=False)
                print("=== BUKTI PENUKARAN ===")
                print("Nama nasabah :", nama)
                print("Sembako      :", barang)
                print("Poin dipakai :", harga_poin)
                print("Sisa poin    :", sisa - harga_poin)
                print("Penukaran berhasil disimpan.")

peran = login()
data = muat_data()
data_bayar = muat_bayar()
data_tukar = muat_tukar()

while True:
    tampil_menu(peran)
    pilih = input("Pilih menu (1-10): ")
    if pilih == "1":
        tampilkan(data)
    elif pilih == "2":
        tambah(data, harga)
    elif pilih == "3":
        ubah(data, harga, peran)
    elif pilih == "4":
        data = hapus(data, peran)
    elif pilih == "5":
        cari(data)
    elif pilih == "6":
        urutkan(data)
    elif pilih == "7":
        laporan(data)
    elif pilih == "8":
        bayar(data, data_bayar)
    elif pilih == "9":
        tukar_poin(data, data_tukar, sembako)
    elif pilih == "10":
        print("Terima kasih, program selesai.")
        break
    else:
        print("Pilihan tidak valid, coba lagi.")
