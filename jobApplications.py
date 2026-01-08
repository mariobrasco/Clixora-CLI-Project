import pandas as pd

from payment import menuPayment
from utility import askInput, cardTemplate, deleteRowById, updateRowById, validasiAngka, headerTemplate, footerTemplate, mergeCSV

FILE_PATH_FINDER = 'storage/jobsApplications.csv'

def listJobsFinder(state, job_id):
    while True:
        jobs_db = pd.read_csv('storage/jobs.csv')
        merge_db = mergeCSV(FILE_PATH_FINDER, 'storage/user.csv', 'user_id', 'user_id')
        job_info = jobs_db[jobs_db['job_id'] == job_id].iloc[0]
        application_info = pd.read_csv(FILE_PATH_FINDER)
        applications_selected = merge_db[merge_db['job_id'] == job_id] 
        applications_selected = applications_selected.rename(columns={
            'applications_id': 'Id Tawaran',
            'username': 'Nama Photographer',
            'tipe_budget': 'Tipe Budget',
            'negotiated_budget': 'Budget Negosiasi',
            'status': 'Status'
        })
        
        headerTemplate("Daftar Tawaran Lowongan", state, profile=True)
        print(f"Lowongan: {job_info['title']} | Budget Asli: {job_info['budget']}\n")
        footerTemplate()
        if (applications_selected.empty):
            print("⚠️  Belum ada tawaran untuk lowongan pekerjaan ini.")
        else:
            print(applications_selected[['Id Tawaran','Nama Photographer', 'Tipe Budget', 'Budget Negosiasi', 'Status']].to_string(index=False))    
        print("--------------------------------")
        print("[K] Kembali  [X] Keluar dari program")
        footerTemplate()
        
        choice = input("Masukan Id Tawaran untuk menindak lanjuti atau Aksi: ").lower()

        if choice == 'k':
            return 
        elif choice == 'x':
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
            exit()
            
        elif choice.isdigit() and int(choice) in applications_selected['Id Tawaran'].values:
            selected =  application_info[application_info['applications_id'] == int(choice)].iloc[0]
            
            if (selected['status'] == 'waiting for photographer'):
                cardTemplate("Info!","Menunggu Photographer merespon tawaran Anda.")
                continue
            
            if (selected['status'] == 'accepted'):
                cardTemplate("Info!","Tawaran sudah diterima sebelumnya.")
                continue
            
            while True:
                headerTemplate("Detail Tawaran", state, profile=True)
                print(f"💰 {merge_db[merge_db['user_id'] == selected['user_id']].iloc[0]['username']} mengajukan: {selected['negotiated_budget']}\n")
                print("[A] Terima tawaran dan Bayar   [T] Tolak tawaran")
                print(f"[B] Ajukan negosiasi balik     {'[C] Bayar Photographer' if selected['status'] == 'accepted' else ''}")
                print("[K] Kembali")
                footerTemplate()

                action = input("Aksi: ").lower()
                
                if (action == 'c' and selected['status'] == 'accepted'):
                    photographer_info = merge_db[merge_db['user_id'] == selected['user_id']].iloc[0]
                    menuPayment(state, selected, job_info, photographer_info)
                    break
                if (action == 't'):
                    updateRowById(
                        FILE_PATH_FINDER, 
                        'applications_id', 
                        selected['applications_id'], 
                        {'status': 'rejected'}
                    )
                    cardTemplate("Berhasil!","❌ Tawaran berhasil ditolak.")
                    break

                if action == 'b':
                    headerTemplate("Pengajuan Negosiasi Balik", state, profile=True)
                    print("\n💬 Ajukan negosiasi balik ke Photographer")
                    
                    while True:
                        print("Tipe Budget:\n[1] Per Jam\n[2] Per Proyek")
                        tipe_budget_pilihan = askInput("Pilih Tipe Budget Katalog*: ", True)
                        
                        if (tipe_budget_pilihan is None):
                            return
                        if (tipe_budget_pilihan == '1'):
                            tipe_budget = 'jam'
                            break
                        elif (tipe_budget_pilihan == '2'):
                            tipe_budget = 'proyek'
                            break
                        if (tipe_budget_pilihan != '1' and tipe_budget_pilihan != '2'):
                            print("Masukkan Tipe Budget yang Valid! (1 atau 2)")
                            continue
                        else:
                            break
                        
                    new_budget = input("Masukkan budget baru: ")
                    if new_budget <= '0':
                        print("\nBudget harus lebih dari 0.")
                        continue

                    if not validasiAngka(new_budget):
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
                    cardTemplate("Berhasil!",f"✅ Tawaran {merge_db[merge_db['user_id'] == selected['user_id']].iloc[0]['username']} diterima dengan Harga {selected['negotiated_budget']}.")
                    menuPayment(state, selected, job_info, merge_db[merge_db['user_id'] == selected['user_id']].iloc[0])
                    break

                elif action == 'k':
                    break

                else:
                    cardTemplate("Peringatan!", f"Input '{action}' tidak valid.")
        else:
            cardTemplate("Peringatan!", f"Input '{choice}' tidak valid.")
            
def listJobsApplications(state, applications_id):
    while True:
        list_jobs_finder_db = pd.read_csv(FILE_PATH_FINDER)
        job_db = pd.read_csv('storage/jobs.csv')
        applications_selected = list_jobs_finder_db[list_jobs_finder_db['applications_id'] == applications_id].iloc[0]
        job_info = job_db[job_db['job_id'] == applications_selected['job_id']].iloc[0]
        
        user_db = pd.read_csv('storage/user.csv')
        finder_info = user_db[user_db['user_id'] == job_info['user_id']].iloc[0]
        
        headerTemplate("Detail Lamaran Lowongan", state, profile=True)

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
        print("-----------------------------------")
        
        if (applications_selected['status'] == 'waiting for photographer'):
            print(f"[A] Ajukan Negosiasi")
        if (applications_selected['status'] == 'waiting for photographer'):
            print(f"[T] Tolak Negosiasi")
        if (applications_selected['status'] == 'waiting for photographer'):
            print(f"[J] Terima Negosiasi")
        if (applications_selected['status'] not in ['rejected', 'accepted']):
            print("[B] Batalkan Lamaran")
            
        print("[K] Kembali      [X] Keluar dari program")
        footerTemplate()
        
        choice = input("Masukan Aksi: ").lower()
        if (choice == 'k'):
            return  
        if (choice == 'x'):
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
            exit()
        
        if (choice == 'a' and applications_selected['status'] == 'waiting for photographer'):
            headerTemplate("Pengajuan Negosiasi Balik ke Finder", state, profile=True)
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

            if not validasiAngka(new_budget):
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
        
        if (choice == 'b' and applications_selected['status'] not in ['waiting for finder', 'waiting for photographer', 'rejected', 'accepted']):
            deleteRowById(
                FILE_PATH_FINDER, 
                'applications_id', 
                applications_id, 
                "Lamaran akan dihapus permanen"
            )
            return
        
        if (choice == 't' and applications_selected['status'] == 'waiting for photographer'):
            updateRowById(
                FILE_PATH_FINDER, 
                'applications_id', 
                applications_id, 
                {'status': 'rejected'}
            )
            cardTemplate("Berhasil!","❌ Negosiasi berhasil ditolak.")
            return
        
        if (choice == 'j' and applications_selected['status'] == 'waiting for photographer'):
            updateRowById(
                FILE_PATH_FINDER, 
                'applications_id', 
                applications_id, 
                {'status': 'accepted',
                'tipe_budget': applications_selected['tipe_budget'],
                'negotiated_budget': applications_selected['negotiated_budget']
            })
            cardTemplate("Berhasil!",f"✅ Negosiasi diterima dengan Harga {applications_selected['negotiated_budget']}.")
            return
        
        if (choice not in ['a', 't', 'j', 'k', 'x', 'b']):
            cardTemplate("Peringatan!", f"Input '{choice}' tidak valid.")