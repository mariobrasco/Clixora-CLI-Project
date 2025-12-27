import pandas as pd

from utility import autoIncrementNumber, cardTemplate

def formCatalog(state):
    catalog_db = pd.read_csv('storage/catalog.csv')
    print("\n" + "="*44 + " Form Catalog " + "="*44)
    title = input("Masukkan Judul: ")
    description = input("Masukkan Deskripsi: ")
    theme = input("Masukkan Tema: ")
    
    while True:
        tipe_budget = input("Pilih Tipe Budget Lowongan: \n(1. Per Jam, \n2. Per Proyek): ")

        if (tipe_budget == '1'):
            per_jam = input("Masukkan Besaran Budget Per Jam: ")
            budget = per_jam
            break
        elif (tipe_budget == '2'):
            per_proyek = input("Masukkan Besaran Budget Per Proyek: ")
            budget = per_proyek
            break
        else:
            print("Masukkan Tipe Budget yang Valid! (1 atau 2)")

    new_catalog = {
        'catalog_id': autoIncrementNumber(catalog_db),
        'user_id': state['account_session']['user_id'] or "",
        'title': title,
        'description': description,
        'theme': theme,
        'tipe_budget': tipe_budget,
        'budget': budget,
        'status': 'available'
    }

    catalog_df = pd.DataFrame([new_catalog])
    catalog_df.to_csv('storage/catalog.csv', mode='a', header=False, index=False)

    cardTemplate("✅ Catalog berhasil dibuat.")