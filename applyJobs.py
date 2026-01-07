import pandas as pd
# from postAJob import validasi_angka
from utility import autoIncrementNumber, cardTemplate, validasiAngka

jobs_applications_db = pd.read_csv('storage/jobsApplications.csv')

def applyJobs(state, job_data):
    print("\n" + "="*44 + " Proses Pelamaran " + "="*44)
    # judul = input("Masukkan Judul Pesanan: ")
    print("Apakah anda setuju dengan harga yang sudah ditentukan (Rp" + str(job_data['budget']) + ")?")
    print("1. Setuju")
    print("2. Negosiasi Harga")
    aksi = input("Masukkan pilihan Anda (1/2): ")
    
    while True:
        if (aksi == '1'):
            tipe_budget = job_data['tipe_budget']
            negotiated_budget = job_data['budget']
            break
        elif (aksi == '2'):
            tipe_budget = input("Pilih Tipe Budget Lowongan: \n1. Per Jam, \n2. Per Proyek \nMasukan Nomor 1 atau 2: ")

            if (tipe_budget == '1'):
                negotiated_budget = input("Masukkan Besaran Budget Per Jam: ")
                if not validasiAngka(negotiated_budget):
                    print("\nBudget harus berupa angka.\n")
                    continue
                break
            elif (tipe_budget == '2'):
                negotiated_budget = input("Masukkan Besaran Budget Per Proyek: ")
                if not validasiAngka(negotiated_budget):
                    print("\nBudget harus berupa angka.\n")
                    continue
                break
            else:
                print("Masukkan Tipe Budget yang Valid! (1 atau 2)")
                continue
        else:
            cardTemplate("Peringatan!",f"Input {aksi} tidak valid. Silahkan input 1 atau 2.")
            continue
        
    print("Pesan bersifat opsional, jika tidak ada, tekan enter.")
    message = input("Masukkan pesan tambahan untuk Finder: ")

    messages_data = {
        'applications_id': autoIncrementNumber(jobs_applications_db),
        'job_id': job_data['job_id'],
        "user_id": state['account_session']['user_id'] or "",
        'deskripsi': message,
        'tipe_budget': tipe_budget,
        'negotiated_budget': negotiated_budget,
        'status': 'waiting for finder'
    }

    apply_job_df = pd.DataFrame([messages_data])
    apply_job_df.to_csv('storage/jobsApplications.csv', mode='a', header=False, index=False)
    # apply_job_df.to_csv('storage/listJobsFinder.csv', mode='a', header=False, index=False)

    cardTemplate("Berhasil", "✅ Berhasil mengirimkan Lamaran pekerjaan!")

# applyJobs()