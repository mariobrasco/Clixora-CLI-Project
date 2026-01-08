import pandas as pd

from utility import autoIncrementNumber, cardTemplate, selectTheme, askInput, headerTemplate, footerTemplate, validasiAngka

def formCatalog(state):
    catalog_db = pd.read_csv('storage/catalog.csv')
    headerTemplate("FORM UNGGAH CATALOG", state, True)
    print("Ketik [batal] untuk membatalkan pembuatan catalog.\n")
    title = askInput("Masukkan Judul: ", True)
    if (title):
        description = askInput("Masukkan Deskripsi: ", True)
        if (description):
            theme = selectTheme()
            if theme is None:
                return
            if (theme):
                while True:
                    print("Tipe Budget:\n[1] Per Jam\n[2] Per Proyek")
                    tipe_budget_pilihan = askInput("Pilih Tipe Budget Katalog: ", True)
                    if (tipe_budget_pilihan):
                        while True:
                            if (tipe_budget_pilihan == '1'):
                                tipe_budget = 'jam'
                                per_jam = askInput("Masukkan Besaran Budget Per Jam: ", True)
                                if (not validasiAngka(per_jam)):
                                    cardTemplate("Peringatan!","Budget harus berupa angka.")
                                    continue
                                if per_jam is None:
                                    return  
                                budget = per_jam
                                break
                            
                            elif (tipe_budget_pilihan == '2'):
                                tipe_budget = 'proyek'
                                per_proyek = askInput("Masukkan Besaran Budget Per Proyek: ", True)
                                if (not validasiAngka(per_proyek)):
                                    cardTemplate("Peringatan!","Budget harus berupa angka.")
                                    continue
                                if per_proyek is None:
                                    return  
                                budget = per_proyek
                                break
                            else:
                                cardTemplate("Peringatan!", "Masukkan Tipe Budget yang Valid! (1 atau 2)")
                                continue
                        
                        footerTemplate()
                               
                        new_catalog = {
                            'catalog_id': autoIncrementNumber(catalog_db),
                            'user_id': state['account_session']['user_id'] or "",
                            'title': title,
                            'description': description,
                            'theme': " ".join(theme) if theme else "",
                            'tipe_budget': tipe_budget,
                            'budget': budget,
                            'status': 'available',
                            'sold_count': 0
                        }

                        catalog_df = pd.DataFrame([new_catalog])
                        catalog_df.to_csv('storage/catalog.csv', mode='a', header=False, index=False)
                        cardTemplate("Berhasil","✅ Catalog berhasil dibuat.")
                        break
                        