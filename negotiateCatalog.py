import pandas as pd

# from postAJob import validasi_tanggal, validasi_waktu
from utility import autoIncrementNumber, cardTemplate, validasiTanggal, validasiWaktu, askInput


def negotiateCatalog(state, catalog_data):
    # print(state)
    # print(catalog_data)
    # print(user_info)
    catalogApplications_db = pd.read_csv('storage/catalogApplications.csv')
    print("\n" + "="*44 + " Proses Negosiasi " + "="*44)
    print("Apakah anda setuju dengan harga yang sudah ditentukan (Rp" + str(catalog_data['budget']) + ")?")
    print("1. Setuju")
    print("2. Negosiasi Harga")
    print("="*102)
    
    while True:
        aksi = input("Masukkan pilihan Anda (1/2): ")
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
            tanggal = input("Masukkan Tanggal Lowongan (DD-MM-YY): ")
            if validasiTanggal(tanggal):
                break
            print("Format tanggal salah! Gunakan DD-MM-YY")
        while True:
            waktu = input("Masukkan Waktu Lowongan (HH:MM): ")
            if validasiWaktu(waktu):
                break
            print("Format waktu salah! Gunakan HH:MM")
            
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
         
        