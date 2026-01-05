import pandas as pd

# from applyJobs import applyJobs
from negotiateCatalog import negotiateCatalog
from utility import cardTemplate, askInput, login, searchAndFilterByDataFrame, mergeCSV

def catalogList(state):
    merged_db = mergeCSV('storage/catalog.csv', 'storage/user.csv', 'user_id', 'user_id')
    
    searchWord = ""
    filter_theme = ""
    filter_budget = ""
    filter_location = ""
    filter_status = ""
    filters = {}
    tampilan_catalog = merged_db[['catalog_id','title', 'theme', 'budget', 'status', 'username', 'location']]
    
    while True:
        catalog_db = pd.read_csv('storage/catalog.csv')
        account_db = pd.read_csv('storage/user.csv')
        merged_db = mergeCSV('storage/catalog.csv', 'storage/user.csv', 'user_id', 'user_id')
        
        print("\n" + "="*44 + " Catalog List " + "="*44)
        print(f"Cari: ({searchWord}) [H] Hapus Pencarian | Filter: (theme: {filter_theme}) (budget: {filter_budget}) (location: {filter_location}) (status: {filter_status}) [A] Hapus Filter")
        
        if (filters or searchWord):
            tampilan_catalog = searchAndFilterByDataFrame(
                merged_db,
                keyword=searchWord,
                search_columns=['title', 'description', 'theme'],
                filters=filters,
                select_columns=['catalog_id','title', 'theme', 'budget', 'status', 'username', 'location']
            )
        else:
            tampilan_catalog = merged_db[['catalog_id','title', 'theme', 'budget', 'status', 'username', 'location']]
            
        print("="*102)
        if (tampilan_catalog.empty):
            print("⚠️  Tidak ada catalog yang sesuai dengan kriteria pencarian dan/atau filter Anda.")
        else:
            print(tampilan_catalog)    

        print("="*102)

        if (state['account_session'] is not None):
            print("Aksi:")
            print("[K] Kembali  [C] Cari  [F] Filter")
            print("[X] Keluar   [L] Logout")
        else:
            print("Aksi:")
            print("[K] Kembali  [C] Cari  [F] Filter")
            print("[X] Keluar")
            
        input_navigasi = (input("Masukan Catalog id untuk melihat detailnya atau aksi: ")).lower()

        if (input_navigasi == "k"):
            return
        elif (input_navigasi == "x"):
            exit()
        elif (input_navigasi == "l" and state['account_session'] is not None):
            cardTemplate("Berhasil!","Anda Telah Logout dari akun " + state['account_session']['username'] + ".")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif (input_navigasi == "c"):
            searchWord = input("Masukkan kata kunci pencarian: ")
        elif (input_navigasi == "a"):
            filter_theme = ""
            filter_budget = ""
            filter_location = ""
            filter_status = ""
            filters = {}
        elif (input_navigasi == "f"):
            print("Masukkan filter yang diinginkan. Kosongkan jika tidak ingin menambahkan filter pada kolom tersebut.")
            filter_theme = input("Filter Theme: ")
            filter_budget = input("Filter Budget (angka): ")
            filter_location = input("Filter Location: ")
            filter_status = input("Filter Status (available/unavailable): ")

            filters = {}
            if filter_theme:
                filters['theme'] = filter_theme
            if filter_budget:
                try:
                    filters['budget'] = int(filter_budget)
                except ValueError:
                    cardTemplate("Peringatan!", "Filter budget harus berupa angka.")
                    continue
            if filter_location:
                filters['location'] = filter_location
            if filter_status:
                filters['status'] = filter_status

            # tampilan_catalog = searchAndFilterByDataFrame(
            #     merged_db,
            #     keyword=searchWord,
            #     search_columns=['title', 'description', 'theme'],
            #     filters=filters,
            #     select_columns=['catalog_id','title', 'theme', 'budget', 'status', 'username', 'location']
            # )
        elif (input_navigasi == "h"):
            searchWord = ""
            # tampilan_catalog = merged_db[['catalog_id','title', 'theme', 'budget', 'status', 'username', 'location']].to_string(index=True)
        elif (input_navigasi.isdigit() and int(input_navigasi) in catalog_db['catalog_id'].values):
            selected_post = catalog_db[catalog_db['catalog_id'] == int(input_navigasi)].iloc[0]

            user_info = account_db[account_db['user_id'] == selected_post['user_id']].iloc[0]
            
            if user_info.empty:
                cardTemplate("Error", "Data pemilik katalog tidak ditemukan.")
                return

            print("\n" + "="*40 + " DETAIL CATALOG " + "="*40)
            print(f"Title  : {selected_post['title']}")
            print(f"Description: \n{selected_post['description']}")
            print(f"\nTheme: {selected_post['theme']}")
            print(f"Budget : {selected_post['budget']} / {'Per Jam' if selected_post['tipe_budget'] == 1 else 'Proyek'}")
            print(f"\nby @{user_info['username']} in {user_info['location']}")
            print("="*98)
            aksi = input("Jika tertarik ketik '1' untuk melanjutkan proses, atau '0' untuk kembali: ")
            if (aksi == '1' and state['account_session'] is not None):
                negotiateCatalog(state, selected_post)
            elif (aksi == '1' and state['account_session'] is None):
                cardTemplate("Peringatan!", "Anda harus login terlebih dahulu untuk melanjutkan proses .")
                # state["input_navigasi"] = 1
                print("\n" + "="*44 + " MENU LOGIN " + "="*44)
                print("Jika Ingin membatalkan login, ketik 'batal'")
                
                input_username = askInput("Masukkan username: ")
                if (input_username):
                    input_password = askInput("Masukkan password: ")
                    if (input_password):
                        if(login(input_username, input_password, state)):
                            print("="*90)
                            cardTemplate("Berhasil!",f"Berhasil login sebagai {state['account_session']['role']}, Selamat datang, {input_username}!")
                        else:
                            cardTemplate("Peringatan!", "Gagal login, username atau password salah.")
                return
            elif(aksi == '0'):
                continue
            else:
                cardTemplate("Peringatan!",f"Input {aksi} tidak valid, silahkan masukan input yang sesuai.")
        else:
            cardTemplate("Peringatan!",f"Input {input_navigasi} tidak valid, silahkan masukan input yang sesuai.")
            
            
