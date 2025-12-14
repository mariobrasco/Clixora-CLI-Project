import pandas as pd

def validasi_angka(teks):
    for char in teks:
        if char < '0' or char > '9':
            return False
    return True

def validasi_tanggal(tanggal):
    if len(tanggal) != 8:
        return False
    if tanggal[2] != "-" or tanggal[5] != "-":
        return False

    hari_str = tanggal[0:2]
    bulan_str = tanggal[3:5]
    tahun_str = tanggal[6:8]

    if not (validasi_angka(hari_str) and 
            validasi_angka(bulan_str) and 
            validasi_angka(tahun_str)):
        return False

    hari = int(hari_str)
    bulan = int(bulan_str)
    tahun = int(tahun_str)

    if hari < 1 or hari > 31:
        return False
    if bulan < 1 or bulan > 12:
        return False
    if tahun < 0 or tahun > 99:
        return False

    return True

def validasi_waktu(waktu):
    if len(waktu) != 5:
        return False
    if waktu[2] != ":":
        return False

    jam = waktu[0:2]
    menit = waktu[3:5]

    if not (validasi_angka(jam) and validasi_angka(menit)):
        return False

    jam = int(jam)
    menit = int(menit)

    if jam < 0 or jam > 23:
        return False
    if menit < 0 or menit > 59:
        return False

    return True

def form_post_job():
    print("\n" + "="*44 + " Form Postingan Lowongan " + "="*44)
    judul = input("Masukkan Judul Lowongan: ")
    deskripsi = input("Masukkan Deskripsi Lowongan: ")
    tema = input("Masukkan Tema Lowongan: ")
    lokasi = input("Masukkan Lokasi Lowongan: ")

    while True:
        tanggal = input("Masukkan Tanggal Lowongan (DD-MM-YY): ")
        if validasi_tanggal(tanggal):
            break
        print("Format tanggal salah! Gunakan DD-MM-YY")

    while True:
        waktu = input("Masukkan Waktu Lowongan (HH:MM): ")
        if validasi_waktu(waktu):
            break
        print("Format waktu salah! Gunakan HH:MM")

    budget = input("Pilih Tipe Budget Lowongan (1. Per Jam, 2. Per Proyek): ")

    post_job = {
        "judul": judul,
        "deskripsi": deskripsi,
        "tema": tema,
        "lokasi": lokasi,
        "tanggal": tanggal,
        "waktu": waktu,
        "budget": budget
    }

    post_job_df = pd.DataFrame([post_job])
    post_job_df.to_csv('Clixora-CLI-Project/storage/postAJob.csv',mode='a', header=False, index=False)

    print("Lowongan berhasil diposting!")