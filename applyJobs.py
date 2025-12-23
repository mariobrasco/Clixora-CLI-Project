import pandas as pd
from postAJob import validasi_angka, validasi_tanggal, validasi_waktu
from utility import autoIncrementNumber, cardTemplate

jobs_applications_db = pd.read_csv('storage/jobsApplications.csv')

def applyJobs(state, job_data):
    print("\n" + "="*44 + " Proses Pelamaran " + "="*44)
    # judul = input("Masukkan Judul Pesanan: ")
    print("Apakah anda setuju dengan harga yang sudah ditentukan (Rp" + str(job_data['budget']) + ")?")
    print("1. Setuju")
    print("2. Negosiasi Harga")
    
    while True:
        aksi = input("Masukkan pilihan Anda (1/2): ")
        if (aksi == '1'):
            tipe_budget = job_data['tipe_budget']
            negotiated_budget = job_data['budget']
            break
        elif (aksi == '2'):
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
                    break
        else:
            cardTemplate("Peringatan!",f"Input {aksi} tidak valid. Silahkan input 1 atau 2.")
            continue
        
    print("Pesan bersifat opsional, jika tidak ada, tekan enter.")
    message = input("Masukkan pesan tambahan untuk Finder: ")
    
    # tema = input("Masukkan Tema Pesanan: ")
    # lokasi = input("Masukkan Lokasi Pesanan: ")

    # while True:
    #     tanggal = input("Masukkan Tanggal Lowongan (DD-MM-YY): ")
    #     if validasi_tanggal(tanggal):
    #         break
    #     print("Format tanggal salah! Gunakan DD-MM-YY")

    # while True:
    #     waktu = input("Masukkan Waktu Lowongan (HH:MM): ")
    #     if validasi_waktu(waktu):
    #         break
    #     print("Format waktu salah! Gunakan HH:MM")

    

    messages_data = {
        'applications_id': autoIncrementNumber(jobs_applications_db),
        'job_id': job_data['job_id'],
        "user_id": state['account_session']['user_id'] or "",
        # 'judul': [judul],
        'deskripsi': message,
        # 'tema': [tema],
        # 'lokasi': [lokasi],
        # 'tanggal': [tanggal],
        # 'waktu': [waktu],
        'tipe_budget': tipe_budget,
        'negotiated_budget': negotiated_budget,
        'status': 'pending'
    }

    apply_job_df = pd.DataFrame([messages_data])
    apply_job_df.to_csv('storage/jobsApplications.csv', mode='a', header=False, index=False)
    # apply_job_df.to_csv('storage/listJobsFinder.csv', mode='a', header=False, index=False)

    cardTemplate("Berhasil", "✅ Berhasil mengirim permintaan pekerjaan!")

# applyJobs()