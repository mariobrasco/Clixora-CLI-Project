import pandas as pd

from payment import menuPayment
from postAJob import validasi_angka
from utility import cardTemplate, updateRowById

FILE_PATH_FINDER = 'storage/jobsApplications.csv'

list_jobs_finder_db = pd.read_csv(FILE_PATH_FINDER)

def listJobsFinder(job_id):
    while True:
        global list_jobs_finder_db
        jobs_db = pd.read_csv('storage/jobs.csv')
        
        print("\n" + "="*63 + " List Tawaran " + "="*63)
        applications_selected = list_jobs_finder_db[list_jobs_finder_db['job_id'] == job_id] 

        if list_jobs_finder_db.empty:
            cardTemplate("Info!","Belum ada yang melamar lowongan anda.")
            return
        
        user_db = pd.read_csv('storage/user.csv')
        job_info = jobs_db[jobs_db['job_id'] == job_id].iloc[0]
        
        print(f"Lowongan: {job_info['title']} | Budget Asli: {job_info['budget']}\n")
        for index, row in applications_selected.iterrows():
            print(
                f"Id Tawaran: {row['applications_id']}. "
                f"Budget Diajukan: {row['negotiated_budget']}  | "
                f"oleh @{user_db[user_db['user_id'] == row['user_id']].iloc[0]['username']}  |"
                f"Status: {row['status']}"
            )
        print("="*135)

        print(f"Aksi:")
        print("[x] Kembali")

        choice = input("Masukan Id Tawaran untuk menindak lanjuti atau Aksi: ").lower()

        if choice == 'x':
            return 
        
        selected =  applications_selected[applications_selected['applications_id'] == int(choice)].iloc[0]
        
        if (selected['status'] == 'waiting for photographer'):
            cardTemplate("Info!","Menunggu Photographer merespon tawaran Anda.")
            continue
        
        if (selected['status'] == 'accepted'):
            cardTemplate("Info!","Tawaran sudah diterima sebelumnya.")
            continue
        
        while True:
            print("\n💬 Photographer mengajukan negosiasi")
            print(f"💰 Budget diajukan: {selected['negotiated_budget']}")
            print("\n[a] Terima tawaran")
            print("(b) Ajukan negosiasi balik")
            print("(x) Kembali")

            action = input("Aksi: ").lower()

            if action == 'b':
                print("\n💬 Ajukan negosiasi balik ke Photographer")
                
                while True:
                    tipe_budget = input("Pilih Tipe Budget Lowongan: \n(1. Per Jam, \n2. Per Proyek): ")

                    if (tipe_budget != '1' and tipe_budget != '2'):
                        print("Masukkan Tipe Budget yang Valid! (1 atau 2)")
                        continue
                    else:
                        break
                    
                new_budget = input("Masukkan budget baru: ")
                if new_budget <= '0':
                    print("\nBudget harus lebih dari 0.")
                    continue

                if not validasi_angka(new_budget):
                    print("\nBudget harus berupa angka.")
                    continue

                updateRowById(
                    FILE_PATH_FINDER, 
                    'applications_id', 
                    selected['applications_id'], 
                    {'status': 'waiting for photographer',
                    'tipe_budget': tipe_budget,
                    'negotiated_budget': new_budget
                })
                cardTemplate("Berhasil!","💰 Negosiasi balasan dikirim ke Photographer, Silahkan tunggu respon dari Photographer.")
                break
            
            elif action == 'a':
                updateRowById(
                    FILE_PATH_FINDER, 
                    'applications_id', 
                    selected['applications_id'], 
                    {'status': 'accepted',
                    'tipe_budget': selected['tipe_budget'],
                    'negotiated_budget': selected['negotiated_budget']
                })
                cardTemplate("Berhasil!",f"✅ Tawaran @{user_db[user_db['user_id'] == selected['user_id']].iloc[0]['username']} diterima dengan Harga {selected['negotiated_budget']}.")
                break

            elif action == 'x':
                break

            else:
                cardTemplate("Peringatan!", f"Input '{action}' tidak valid.")

def listJobsApplications(applications_id):
    while True:
        job_db = pd.read_csv('storage/jobs.csv')
        applications_selected = list_jobs_finder_db[list_jobs_finder_db['applications_id'] == applications_id].iloc[0] 
        job_info = job_db[job_db['job_id'] == applications_selected['job_id']].iloc[0]
        
        
        user_db = pd.read_csv('storage/user.csv')
        finder_info = user_db[user_db['user_id'] == job_info['user_id']].iloc[0]
        
        print("\n" + "="*63 + " Detail Pesanan " + "="*63)

        if applications_selected.empty:
            cardTemplate("Info!","Pesanan tidak ditemukan.")
            return
        
        print(f"Finder          : {finder_info['username']}")
        print(f"Judul Lamaran   : {job_info['title']}")
        print(f"Tema            : {job_info['theme']}")
        print(f"Deskripsi       : {job_info['description']}")
        print(f"Pesan           : {applications_selected['message']}")
        print(f"Lokasi          : {job_info['location']}")
        print(f"Tanggal         : {job_info['date_needed']}")
        print(f"Waktu           : {job_info['time']}")
        print(f"Budget          : {applications_selected['negotiated_budget']}")
        print(f"Status          : {applications_selected['status']}")
        print("="*135)
        
        print(f"Aksi:")
        print(f"{'[A] Ajukan Negosiasi' if applications_selected['status'] == 'waiting for photographer' else ''}")
        print(f"{'[T] Tolak Negosiasi' if applications_selected['status'] == 'waiting for photographer' else ''}")
        print(f"{'[B] Bayar Pesanan' if applications_selected['status'] == 'accepted' else ''}")
        print("[K] Kembali")
        
        choice = input("Masukan Aksi: ").lower()
        if choice == 'k':
            return  
        
        if choice == 'a' and applications_selected['status'] == 'waiting for photographer':
            print("\n💬 Ajukan negosiasi balik ke Finder")
            while True:
                tipe_budget = input("Pilih Tipe Budget Katalog: \n(1. Per Jam, \n2. Per Proyek): ")

                if (tipe_budget != '1' and tipe_budget != '2'):
                    print("Masukkan Tipe Budget yang Valid! (1 atau 2)")
                    continue
                else:
                    break
                
            new_budget = input("Masukkan budget baru: ")
            if new_budget <= '0':
                print("\nBudget harus lebih dari 0.")
                continue

            if not validasi_angka(new_budget):
                print("\nBudget harus berupa angka.")
                continue

            updateRowById(
                FILE_PATH_FINDER, 
                'applications_id', 
                applications_id, 
                {'status': 'waiting for finder',
                'tipe_budget': tipe_budget,
                'negotiated_budget': new_budget
            })
            cardTemplate("Berhasil!","💰 Negosiasi berhasil dikirim , Silahkan tunggu respon dari Finder.")
            return
        
        if choice == 'b' and applications_selected['status'] == 'accepted':
            menuPayment(applications_selected, job_info, finder_info)