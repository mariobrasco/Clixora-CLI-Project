import pandas as pd

from utility import autoIncrementNumber, cardTemplate

jobs_db = pd.read_csv('storage/jobs.csv')

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

    if not (validasi_angka(hari_str) and validasi_angka(bulan_str) and validasi_angka(tahun_str)):
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

def form_post_job(state):
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

    while True:
        tipe_budget = input("Pilih Tipe Budget Lowongan: \n(1. Per Jam, \n2. Per Proyek): ")

        if (tipe_budget == '1'):
            per_jam = input("Masukkan Besaran Budget Per Jam: ")
            budget = per_jam
            break
        elif (tipe_budget == '2'):
            per_proyek = input("Masukkan Besaran Budget Per Proyek: ")
            budget = per_proyek
            break
        else:
            print("Masukkan Tipe Budget yang Valid! (1 atau 2)")

    jobs_data = {
        "job_id": autoIncrementNumber(jobs_db),
        "finder_id": state['account_session']['user_id'] or "",
        "judul": judul,
        "deskripsi": deskripsi,
        "tema": tema,
        "lokasi": lokasi,
        "tanggal": tanggal,
        "waktu": waktu,
        "budget": budget,
        "status": "available",
        "negotiated_budget": "-"
    }
        
    post_job_df = pd.DataFrame([jobs_data])
    post_job_df.to_csv('storage/jobs.csv', mode='a', header=False, index=False)

    cardTemplate("Berhasil", "Lowongan berhasil diunggah!")

# form_post_job()