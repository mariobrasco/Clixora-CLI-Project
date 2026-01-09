import pandas as pd

from jobApplications import FILE_PATH_FINDER
from payment import menuPayment
from utility import askInput, cardTemplate, deleteRowById, updateRowById, validasiAngka, headerTemplate, footerTemplate, mergeCSV

FILE_PATH_PHOTOGRAPHER = 'storage/catalogApplications.csv'


def listCatalogApplications(state, catalog_id):
    while True:
        catalog_db = pd.read_csv('storage/catalog.csv')
        merge_db = mergeCSV(FILE_PATH_PHOTOGRAPHER, 'storage/user.csv', 'user_id', 'user_id')
        application_info = pd.read_csv(FILE_PATH_PHOTOGRAPHER)
        catalog_info = catalog_db[catalog_db['catalog_id'] == catalog_id].iloc[0]
        applications_selected = merge_db[merge_db['catalog_id'] == catalog_id]
        applications_selected = applications_selected.rename(columns={
            'applications_id': 'Id Tawaran',
            'message': 'Pesan',
            'location_left': 'Lokasi',
            'date': 'Tanggal',
            'time': 'Waktu',
            'negotiated_budget': 'Budget Diajukan',
            'tipe_budget': 'Tipe Budget',
            'status': 'Status',
            'username': 'Diajukan Oleh'
        }) 
        
        headerTemplate("List Tawaran", state, profile=True)
        print(f"Lowongan: {catalog_info['title']}  | Tema: {catalog_info['theme']}  |  Budget Asli: {catalog_info['budget']}")
        footerTemplate()
        if (applications_selected.empty):
            print("⚠️  Belum ada tawaran untuk catalog ini.")
        else:
            print(applications_selected[['Id Tawaran', 'Diajukan Oleh', 'Pesan', 'Lokasi', 'Tanggal', 'Waktu', 'Budget Diajukan', 'Tipe Budget', 'Status']].to_string(index=False))
        
        print("-------------------------")
        print("[K] Kembali      [X] Keluar dari program")
        footerTemplate()

        choice = input("Masukan Id Tawaran untuk menindak lanjuti atau Aksi: ").lower()

        if choice == 'k':
            return 
        elif choice == 'x':
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
            exit()
        
        elif choice.isdigit() and int(choice) in applications_selected['Id Tawaran'].values:
            selected =  application_info[application_info['applications_id'] == int(choice)].iloc[0]
            
            while True:
                headerTemplate("Detail Tawaran", state, profile=True)
                print(f"💰 {merge_db[merge_db['user_id'] == selected['user_id']].iloc[0]['username']} mengajukan: {selected['negotiated_budget']} {selected['tipe_budget']}")
                print("-------------------------")
                if (merge_db[merge_db['user_id'] == selected['user_id']].iloc[0]['status'] == 'pending'):
                    print("[S] Pembayaran Diterima")
                print("[A] Terima tawaran")
                print("[B] Ajukan negosiasi balik")
                print("[X] Kembali")
                footerTemplate()

                action = input("Pilih Aksi: ").lower()

                if (action == 's' and merge_db[merge_db['user_id'] == selected['user_id']].iloc[0]['status'] == 'pending'):
                    updateRowById(
                        FILE_PATH_FINDER, 
                        'applications_id', 
                        selected['applications_id'], 
                        {'status': 'paid'}
                    )
                    cardTemplate("Berhasil!",f"✅ Pembayaran diterima sebesar {selected['negotiated_budget']}.")
            
                if action == 'b':
                    headerTemplate("Pengajuan Negosiasi Balik", state, profile=True)
                    
                    while True:
                        print("Tipe Budget:\n[1] Per Jam\n[2] Per Proyek")
                        tipe_budget_pilihan = askInput("Pilih Tipe Budget Katalog: ", True)
                        
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
                    if (new_budget <= '0'):
                        print("\nBudget harus lebih dari 0.")
                        continue

                    if (not validasiAngka(new_budget)):
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
                    cardTemplate("Berhasil!",f"✅ Tawaran {merge_db[merge_db['user_id'] == selected['user_id']].iloc[0]['username']} diterima dengan Harga {selected['negotiated_budget']}.\n Silahkan menunggu konfirmasi pembayaran dari Finder.")
                    break

                elif action == 'x':
                    break

                else:
                    cardTemplate("Peringatan!", f"Input '{action}' tidak valid.")
        else:
            cardTemplate("Peringatan!", f"Input '{choice}' tidak valid.")

def listOrderApplications(state, applications_id):
    while True:
        catalog_db = pd.read_csv('storage/catalog.csv')
        list_catalog_photographer_db = pd.read_csv(FILE_PATH_PHOTOGRAPHER)
        
        applications_selected = list_catalog_photographer_db[list_catalog_photographer_db['applications_id'] == applications_id].iloc[0] 
        catalog_info = catalog_db[catalog_db['catalog_id'] == applications_selected['catalog_id']].iloc[0]
        
        user_db = pd.read_csv('storage/user.csv')
        photographer_info = user_db[user_db['user_id'] == catalog_info['user_id']].iloc[0]
        
        headerTemplate("Detail Pesanan", state, profile=True)

        if (applications_selected.empty):
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
        print("-----------------------------------")
        
        if (applications_selected['status'] == 'waiting for finder'):
            print(f"[A] Ajukan Negosiasi")
        if (applications_selected['status'] == 'waiting for finder'):
            print(f"[T] Tolak Negosiasi")
        if (applications_selected['status'] == 'waiting for finder'):
            print(f"[J] Terima Negosiasi dan Bayar")
        elif (applications_selected['status'] == 'accepted'):
            print(f"[B] Bayar Pesanan")
        if (applications_selected['status'] == 'paid'):
            print("[L] Lihat Struk Pembayaran")
        if (applications_selected['status'] not in ['accepted', 'rejected', 'pending', 'paid']):
            print("[C] Batalkan Pesanan")
            
        print("[K] Kembali    [X] Keluar dari program")
        footerTemplate()
        
        pilihan_aksi = input("Masukan Aksi: ").lower()
        if (pilihan_aksi) == 'k':
            return  
        if (pilihan_aksi) == 'x':
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
            exit()
        
        if (pilihan_aksi == 'l' and applications_selected['status'] == 'paid'):
            payment_db = pd.read_csv('storage/payments.csv')
            payment_info = payment_db[payment_db['application_id'] == applications_id].iloc[0]
            headerTemplate("Struk Pembayaran", state, profile=True)
            print(f"Payment ID              : {payment_info['payment_id']}")
            print(f"Metode Pembayaran       : {payment_info['payment_method']}")
            print(f"Tipe Pembayaran         : {payment_info['payment_type']}")
            print(f"Refs                    : {payment_info['payment_refs']}")
            print(f"Jumlah dibayar          : {payment_info['amount']}")
            print(f"Status                  : {payment_info['status']}")
            print(f"Dibayar Pada            : {payment_info['paid_at']}")
            footerTemplate()
            input("Tekan Enter untuk kembali...")
            continue
        
        if pilihan_aksi == 'a' and applications_selected['status'] == 'waiting for finder':
            headerTemplate("Pengajuan Negosiasi Balik ke Photographer", state, profile=True)
            while True:
                print("Tipe Budget:\n[1] Per Jam\n[2] Per Proyek")
                tipe_budget_pilihan = askInput("Pilih Tipe Budget Katalog: ")
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
                FILE_PATH_PHOTOGRAPHER, 
                'applications_id', 
                applications_id, 
                {'status': 'waiting for photographer',
                'tipe_budget': tipe_budget,
                'negotiated_budget': new_budget
            })
            cardTemplate("Berhasil!","💰 Negosiasi berhasil dikirim , Silahkan tunggu respon dari Photographer.")
            return
        
        if (pilihan_aksi == 'c') and (applications_selected['status'] in ['accepted', 'rejected', 'pending', 'paid']):
            deleteRowById(
                FILE_PATH_PHOTOGRAPHER, 
                'applications_id', 
                applications_id,
                "Pesanan akan dihapus permanen"
            )
            return
        
        if pilihan_aksi == 'j' and applications_selected['status'] == 'waiting for finder':
            updateRowById(
                FILE_PATH_PHOTOGRAPHER, 
                'applications_id', 
                applications_id, 
                {"status": 'accepted',
                'tipe_budget': applications_selected['tipe_budget'],
                'negotiated_budget': applications_selected['negotiated_budget']
            })
            cardTemplate("Berhasil!","✅ Negosiasi berhasil diterima. Silahkan lanjut ke pembayaran.")
            menuPayment(state, applications_selected, catalog_info, photographer_info)
            return
        
        if pilihan_aksi == 'b' and applications_selected['status'] == 'accepted':
            menuPayment(state, applications_selected, catalog_info, photographer_info)
        
        if pilihan_aksi == 't' and applications_selected['status'] == 'waiting for finder':
            updateRowById(
                FILE_PATH_PHOTOGRAPHER, 
                'applications_id', 
                applications_id, 
                {"status": 'rejected'}
            )
            cardTemplate("Berhasil!","❌ Negosiasi berhasil ditolak.")
            return
        
        elif pilihan_aksi not in ['a', 'j', 'b', 't', 'k', 'x', 'c', 'l']:
            cardTemplate("Peringatan!", f"Input '{pilihan_aksi}' tidak valid.")
        