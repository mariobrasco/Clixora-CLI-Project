import pandas as pd

from utility import autoIncrementNumber, cardTemplate


def negotiateCatalog(state, catalog_data, user_info):
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
        new_application = {
            "applications_id": autoIncrementNumber(catalogApplications_db),
            "catalog_id": catalog_data['catalog_id'],
            "user_id": state['account_session']['user_id'],
            "message": message,
            "location": location,
            "negotiated_budget": negotiated_budget,
            "status": "pending"
        }
        new_application_df = pd.DataFrame([new_application])
        new_application_df.to_csv('storage/catalogApplications.csv', mode='a', header=False, index=False)
        cardTemplate("Berhasil", "Tawaran berhasil dikirimkan ke photografer, silahkan tunggu jawaban photografer.")
        break
         
        
