import pandas as pd

from utility import autoIncrementNumber, cardTemplate, validasiAngka, headerTemplate, footerTemplate

jobs_applications_db = pd.read_csv('storage/jobsApplications.csv')

def applyJobs(state, job_data):
    headerTemplate("PROSES PELAMARAN", state, True)
    print("Anda akan melamar pada pekerjaan berikut:")
    print(f"Job ID          : {job_data['job_id']}")
    print(f"Judul Pekerjaan : {job_data['title']}")
    print(f"Deskripsi       : {job_data['description']}")
    print(f"Tipe Budget     : {job_data['tipe_budget']}")
    footerTemplate()
    print("Apakah anda setuju dengan harga yang sudah ditentukan (Rp" + str(job_data['budget']) + ")?")
    print("[1] Setuju")
    print("[2] Negosiasi Harga")
    print("[B] Batal Pelamaran")
    aksi = input("Masukkan pilihan Anda: ")
    if (aksi.lower() == 'b'):
        cardTemplate("Info!", "Proses pelamaran dibatalkan, kembali ke menu sebelumnya.")
        return
    
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
    footerTemplate()

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

    cardTemplate("Berhasil", "✅ Berhasil mengirimkan Lamaran pekerjaan!")
