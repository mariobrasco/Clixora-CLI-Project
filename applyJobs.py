import pandas as pd
from postAJob import validasi_angka, validasi_tanggal, validasi_waktu
from utility import autoIncrementNumber

messages_db = pd.read_csv('storage/listJobsPhotographer.csv')

def applyJobs():
    print("\n" + "="*44 + " Proses Pemesanan " + "="*44)
    judul = input("Masukkan Judul Pesanan: ")
    deskripsi = input("Masukkan Deskripsi Pesanan: ")
    tema = input("Masukkan Tema Pesanan: ")
    lokasi = input("Masukkan Lokasi Pesanan: ")

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
            if not validasi_angka(per_jam):
                print("\nBudget harus berupa angka.\n")
                continue 
            budget = per_jam
            break
        elif (tipe_budget == '2'):
            per_proyek = input("Masukkan Besaran Budget Per Proyek: ")
            if not validasi_angka(per_proyek):
                print("\nBudget harus berupa angka.\n")
                continue 
            budget = per_proyek
            break
        else:
            print("Masukkan Tipe Budget yang Valid! (1 atau 2)")

    messages_data = {
        'message_id': [autoIncrementNumber(messages_db)],
        # "finder_id": state['account_session']['user_id'] or "",
        'judul': [judul],
        'deskripsi': [deskripsi],
        'tema': [tema],
        'lokasi': [lokasi],
        'tanggal': [tanggal],
        'waktu': [waktu],
        'tipe_budget': [tipe_budget],
        'budget': [budget],
        'status': ['pending'],
        'negotiated_budget': ['-']
    }

    apply_job_df = pd.DataFrame(messages_data)
    apply_job_df.to_csv('storage/listJobsPhotographer.csv', mode='a', header=False, index=False)
    apply_job_df.to_csv('storage/listJobsFinder.csv', mode='a', header=False, index=False)

    print("\n✅ Berhasil mengirim permintaan pekerjaan!")

# applyJobs()