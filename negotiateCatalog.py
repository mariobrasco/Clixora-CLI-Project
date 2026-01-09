import pandas as pd

from utility import autoIncrementNumber, cardTemplate, validasiTanggal, validasiWaktu, askInput, headerTemplate, footerTemplate

def negotiateCatalog(state, catalog_data):
    if (state['account_session'] is not None):
        if (state['account_session']['role'] != 'finder'):
            cardTemplate("Peringatan!", "⚠️  Hanya akun finder yang dapat melakukan negosiasi catalog.")
            return
    catalogApplications_db = pd.read_csv('storage/catalogApplications.csv')
    headerTemplate("NEGOSIASI CATALOG", state, profile=True)
    print("Anda akan melakukan negosiasi pada catalog berikut:")
    print(f"Catalog ID       : {catalog_data['catalog_id']}")
    print(f"Judul Catalog    : {catalog_data['title']}")
    print(f"Deskripsi        : {catalog_data['description']}")
    print(f"Tipe Budget      : {catalog_data['tipe_budget']}")
    footerTemplate()
    print("Apakah anda setuju dengan harga yang sudah ditentukan (Rp" + str(catalog_data['budget']) + ")?")
    print("[1] Setuju")
    print("[2] Negosiasi Harga")
    print("[B] Batal Negosiasi")
    footerTemplate()
    
    while True:
        aksi = input("Masukkan pilihan Anda: ")
        if (aksi.lower() == 'b'):
            return
        if (aksi == '1'):
            negotiated_budget = catalog_data['budget']
        elif (aksi == '2'):
            negotiated_budget = input("Masukkan harga negosiasi Anda: ")
        else:
            cardTemplate("Peringatan!",f"Input {aksi} tidak valid. Silahkan input 1 atau 2.")
            continue
        
        print("Pesan bersifat opsional, jika tidak ada, tekan enter.")
        message = input("Masukkan pesan tambahan untuk photografer : ")
        location = input("Masukkan lokasi tempat dilaksanakan: ")
        
        while True:
            tanggal = input("Masukkan Tanggal Lowongan (DD-MM-YYYY): ")
            if validasiTanggal(tanggal):
                break
            print("Format tanggal salah! Gunakan DD-MM-YYYY")
        while True:
            waktu = input("Masukkan Waktu Lowongan (HH:MM): ")
            if validasiWaktu(waktu):
                break
            print("Format waktu salah! Gunakan HH:MM")
        
        footerTemplate()
        new_application = {
            "applications_id": autoIncrementNumber(catalogApplications_db),
            "catalog_id": catalog_data['catalog_id'],
            "user_id": state['account_session']['user_id'],
            "message": message,
            "location": location,
            "date": tanggal,
            "time": waktu,
            "tipe_budget": catalog_data['tipe_budget'],
            "negotiated_budget": negotiated_budget,
            "status": "waiting for photographer"
        }
        new_application_df = pd.DataFrame([new_application])
        new_application_df.to_csv('storage/catalogApplications.csv', mode='a', header=False, index=False)
        cardTemplate("Berhasil", "Tawaran berhasil dikirimkan ke photografer, silahkan tunggu jawaban photografer.")
        break
         
        