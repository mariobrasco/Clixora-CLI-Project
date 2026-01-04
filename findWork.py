import pandas as pd

from applyJobs import applyJobs
from utility import cardTemplate

def validasi_angka(teks):
    for char in teks:
        if char < '0' or char > '9':
            return False
    return True

def find_work(state):
    
    while True:
        postAJob_csv = pd.read_csv('storage/jobs.csv')

        print("\n" + "="*50 + " Find Work " + "="*50)
        if (postAJob_csv.empty):
            print("⚠️  Belum ada lowongan pekerjaan yang tersedia.")
        else:
            print(postAJob_csv[["title","description","theme","location","date_needed","time","tipe_budget","budget","status"]].to_string(index=True))
        print("="*125)

        print("\nKetik nomor index (angka paling kiri) untuk melihat detail.")
        print("Ketik 'x' untuk kembali.")
        
        pilih = input("Pilih lowongan: ")

        if pilih == 'x':
            print("Keluar dari Find Work.")
            break

        if pilih != "" and validasi_angka(pilih):
            
            index = int(pilih)

            if index >= 0 and index < len(postAJob_csv):
                
                job = postAJob_csv.iloc[index]

                keterangan_tipe = "Budget Per Jam"
                if job['tipe_budget'] == 2:
                    keterangan_tipe = "Budget Proyek"

                print("\n" + "="*60)
                print(f" DETAIL PEKERJAAN (ID: {index}) ")
                print("=" * 60)

                for i, (key, value) in enumerate(job.items(), start=1):
                    if key == "tipe_budget":
                        print(f"{i}. {key:<12}: {value} ({keterangan_tipe})")
                    elif key == "budget":
                        print(f"{i}. {key:<12}: Rp {value}")
                    else:
                        print(f"{i}. {key:<12}: {value}")

                print("=" * 60)

                print("[1] Lamar Pekerjaan ini")
                print("[0] Kembali ke menu awal")
                
                aksi = input("Pilih aksi: ")
                
                if (aksi == '1' and state['account_session'] is not None):
                    applyJobs(state, job)
                elif (aksi == '1' and state['account_session'] is None):
                    cardTemplate("Peringatan!","⚠️  Anda harus login terlebih dahulu untuk melamar pekerjaan.")
                
            else:
                print("⚠️  Nomor index tidak ditemukan.")
        else:
            print("⚠️  Mohon masukkan input berupa angka.")

# find_work()