import pandas as pd

from payment import menuPayment
from postAJob import validasi_angka
from utility import cardTemplate, updateRowById

FILE_PATH_PHOTOGRAPHER = 'storage/catalogApplications.csv'

list_catalog_photographer_db = pd.read_csv(FILE_PATH_PHOTOGRAPHER)

def listCatalogApplications(catalog_id):
    while True:
        global list_catalog_photographer_db
        catalog_db = pd.read_csv('storage/catalog.csv')
        
        print("\n" + "="*63 + " List Tawaran " + "="*63)
        applications_selected = list_catalog_photographer_db[list_catalog_photographer_db['catalog_id'] == catalog_id] 

        if list_catalog_photographer_db.empty:
            cardTemplate("Info!","Belum ada yang menawar Catalog anda.")
            return
        
        user_db = pd.read_csv('storage/user.csv')
        catalog_info = catalog_db[catalog_db['catalog_id'] == catalog_id].iloc[0]
        
        print(f"Lowongan: {catalog_info['title']} | Budget Asli: {catalog_info['budget']}")
        for index, row in applications_selected.iterrows():
            print(
                f"Id Tawaran: {row['applications_id']}. "
                f"Budget Diajukan: {row['negotiated_budget']}  | "
                f"Lokasi: {row['location']}  | "
                f"Tanggal: {row['date']} Jam: {row['time']}  | "
                f"Oleh {user_db[user_db['user_id'] == row['user_id']].iloc[0]['username']} | "
                f"Status: {row['status']}"
            )
        print("="*135)

        print(f"Aksi:")
        print("[x] Kembali")

        choice = input("Masukan Id Tawaran untuk menindak lanjuti atau Aksi: ").lower()

        if choice == 'x':
            return 
        
        selected =  applications_selected[applications_selected['applications_id'] == int(choice)].iloc[0]
        
        if (selected['status'] == 'waiting for finder'):
            cardTemplate("Info!","Menunggu Finder merespon tawaran Anda.")
            continue
        
        if (selected['status'] == 'accepted'):
            cardTemplate("Info!","Tawaran sudah diterima sebelumnya.")
            continue
        
        while True:
            print("\n💬 Finder mengajukan negosiasi")
            print(f"💰 Budget diajukan: {selected['negotiated_budget']}")
            print("\n[a] Terima tawaran")
            print("(b) Ajukan negosiasi balik")
            print("(x) Kembali")

            action = input("Aksi: ").lower()

            if action == 'b':
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
                    FILE_PATH_PHOTOGRAPHER, 
                    'applications_id', 
                    selected['applications_id'], 
                    {'status': 'waiting for finder',
                    'tipe_budget': tipe_budget,
                    'negotiated_budget': new_budget
                })
                cardTemplate("Berhasil!","💰 Negosiasi berhasil dikirim , Silahkan tunggu respon dari Finder.")
                break
            
            elif action == 'a':
                updateRowById(
                    FILE_PATH_PHOTOGRAPHER, 
                    'applications_id', 
                    selected['applications_id'], 
                    {'status': 'accepted',
                    'tipe_budget': selected['tipe_budget'],
                    'negotiated_budget': selected['negotiated_budget']
                })
                cardTemplate("Berhasil!",f"✅ Tawaran @{user_db[user_db['user_id'] == selected['user_id']].iloc[0]['username']} diterima dengan Harga {selected['negotiated_budget']}.\n Silahkan menunggu konfirmasi pembayaran dari Finder.")
                break

            elif action == 'x':
                break

            else:
                cardTemplate("Peringatan!", f"Input '{action}' tidak valid.")

def listOrderApplications(applications_id):
    while True:
        catalog_db = pd.read_csv('storage/catalog.csv')
        catalog_info = catalog_db[catalog_db['catalog_id'] == applications_id].iloc[0]
        
        applications_selected = list_catalog_photographer_db[list_catalog_photographer_db['applications_id'] == applications_id].iloc[0] 
        
        user_db = pd.read_csv('storage/user.csv')
        photographer_info = user_db[user_db['user_id'] == catalog_info['user_id']].iloc[0]
        
        print("\n" + "="*63 + " Detail Pesanan " + "="*63)

        if applications_selected.empty:
            cardTemplate("Info!","Pesanan tidak ditemukan.")
            return
        
        print(f"Photographer    : {photographer_info['username']}")
        print(f"Judul Catalog   : {catalog_info['title']}")
        print(f"Tema            : {catalog_info['theme']}")
        print(f"Deskripsi       : {catalog_info['description']}")
        print(f"Pesan           : {applications_selected['message']}")
        print(f"Lokasi          : {applications_selected['location']}")
        print(f"Tanggal         : {applications_selected['date']}")
        print(f"Waktu           : {applications_selected['time']}")
        print(f"Budget          : {applications_selected['negotiated_budget']}")
        print(f"Status          : {applications_selected['status']}")
        print("="*135)
        
        print(f"Aksi:")
        print(f"{'[A] Ajukan Negosiasi' if applications_selected['status'] == 'waiting for finder' else ''}")
        print(f"{'[T] Tolak Negosiasi' if applications_selected['status'] == 'waiting for finder' else ''}")
        print(f"{'[B] Bayar Pesanan' if applications_selected['status'] == 'accepted' else ''}")
        print("[K] Kembali")
        
        choice = input("Masukan Aksi: ").lower()
        if choice == 'k':
            return  
        
        if choice == 'a' and applications_selected['status'] == 'waiting for finder':
            print("\n💬 Ajukan negosiasi balik ke Photographer")
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
                FILE_PATH_PHOTOGRAPHER, 
                'applications_id', 
                applications_id, 
                {'status': 'waiting for photographer',
                'tipe_budget': tipe_budget,
                'negotiated_budget': new_budget
            })
            cardTemplate("Berhasil!","💰 Negosiasi berhasil dikirim , Silahkan tunggu respon dari Photographer.")
            return
        
        if choice == 'b' and applications_selected['status'] == 'accepted':
            menuPayment(applications_selected, catalog_info, photographer_info)
            
        
        

# listJobsFinder()