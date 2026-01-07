import pandas as pd

from negotiateCatalog import negotiateCatalog
from utility import cardTemplate, askInput, login, searchAndFilterByDataFrame, mergeCSV, headerTemplate, footerTemplate
from loginRegister import menuLogin

def catalogList(state):
    merged_db = mergeCSV('storage/catalog.csv', 'storage/user.csv', 'user_id', 'user_id')
    searchWord = ""
    filter_theme = ""
    filter_budget = ""
    filter_location = ""
    filters = {}
    current_page = 1
    total_pages = 1
    tampilan_catalog = merged_db[['catalog_id','title', 'theme', 'budget', 'status', 'username', 'location']]
    
    while True:
        catalog_db = pd.read_csv('storage/catalog.csv')
        account_db = pd.read_csv('storage/user.csv')
        merged_db = mergeCSV('storage/catalog.csv', 'storage/user.csv', 'user_id', 'user_id')
        merged_db = merged_db.rename(columns={
            'catalog_id': 'Catalog Id',
            'title': 'Judul Lowongan',
            'theme': 'Tema',
            'budget': 'Budget',
            'status': 'Status',
            'username': 'Diupload Oleh',
            'location': 'Lokasi'
        })
        headerTemplate("CATALOG", state, profile=True)
        print(f"Cari    : ( {searchWord} ) [H] Hapus Pencarian ")
        print(f"Filter  : ({'(theme: ' + filter_theme + ')' if filter_theme else ''} {'(budget: ' + filter_budget + ')' if filter_budget else ''} {'(location: ' + filter_location + ')' if filter_location else ''}) [A] Hapus Filter")
        
        tampilan_catalog, total_pages = searchAndFilterByDataFrame(
            merged_db,
            keyword=searchWord,
            search_columns=['Judul Lowongan'],
            filters=filters,
            select_columns=['Catalog Id','Judul Lowongan', 'Tema', 'Budget', 'Status', 'Diupload Oleh', 'Lokasi'],
            page=current_page,
            per_page=10
        )
            
        footerTemplate()
        if (tampilan_catalog.empty and not (searchWord or filters)):
            print("⚠️  Belum ada catalog yang tersedia.")
        elif (tampilan_catalog.empty and (searchWord or filters)):
            print("⚠️  Tidak ada catalog yang sesuai dengan kriteria pencarian dan/atau filter Anda.")
        else:
            print(tampilan_catalog.to_string(index=False))    

        footerTemplate()

        if (state['account_session'] is not None):
            print(f"Halaman: [ {str(current_page)} ] dari [ {str(total_pages)} ]")
            if (current_page > 1 and current_page < total_pages):
                print("[P] Halaman Sebelumnya   [N] Halaman Berikutnya")
            elif (current_page == 1 and total_pages > 1):
                print("[N] Halaman Berikutnya")
            elif (current_page == total_pages and total_pages > 1):
                print("[P] Halaman Sebelumnya")
            print("-----------------------------------")
            print("[K] Kembali  [C] Cari  [F] Filter")
            print("[X] Keluar   [L] Logout")
        else:
            print(f"Halaman: [ {str(current_page)} ] dari [ {str(total_pages)} ]")
            if (current_page > 1 and current_page < total_pages):
                print("[P] Halaman Sebelumnya   [N] Halaman Berikutnya")
            elif (current_page == 1 and total_pages > 1):
                print("[N] Halaman Berikutnya")
            elif (current_page == total_pages and total_pages > 1):
                print("[P] Halaman Sebelumnya")
            print("-----------------------------------")
            print("[K] Kembali  [C] Cari  [F] Filter")
            print("[X] Keluar")
        footerTemplate()
        input_navigasi = (input("Masukan Catalog id untuk melihat detailnya atau Aksi: ")).lower()

        if (input_navigasi == "k"):
            return
        elif (input_navigasi == "x"):
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
            exit()
        elif (input_navigasi == "l" and state['account_session'] is not None):
            cardTemplate("Berhasil!","Anda Telah Logout dari akun " + state['account_session']['username'] + ".")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif (input_navigasi == "c"):
            searchWord = input("Masukkan kata kunci pencarian: ")
        elif (input_navigasi == "p" and current_page > 1):
            current_page -= 1
        elif (input_navigasi == "n" and current_page < total_pages):
            current_page += 1
        elif (input_navigasi == "a"):
            filter_theme = ""
            filter_budget = ""
            filter_location = ""
            filters = {}
        elif (input_navigasi == "f"):
            print("Masukkan filter yang diinginkan. Kosongkan jika tidak ingin menambahkan filter pada kolom tersebut.")
            filter_theme = input("Filter Theme: ")
            filter_budget = input("Filter Budget (angka): ")
            filter_location = input("Filter Location: ")

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
        elif (input_navigasi == "h"):
            searchWord = ""
        elif (input_navigasi.isdigit() and int(input_navigasi) in catalog_db['catalog_id'].values):
            selected_post = catalog_db[catalog_db['catalog_id'] == int(input_navigasi)].iloc[0]
            user_info = account_db[account_db['user_id'] == selected_post['user_id']].iloc[0]
            
            if user_info.empty:
                cardTemplate("Error", "Data pemilik katalog tidak ditemukan.")
                return

            headerTemplate("DETAIL CATALOG", state, profile=False)
            print(f"Title  : {selected_post['title']}")
            print(f"Description: \n{selected_post['description']}")
            print(f"\nTheme: {selected_post['theme']}")
            print(f"Budget : {selected_post['budget']} / {selected_post['tipe_budget']}")
            print(f"\nby @{user_info['username']} in {user_info['location']}")
            footerTemplate()
            
            if (state['account_session']['role'] == 'finder'):
                print("[1] Pesan Catalog    [0] Kembali")
                aksi = input("Masukan aksi: ").lower()
                if (aksi == '1' and state['account_session'] is not None):
                    negotiateCatalog(state, selected_post)
                elif (aksi == '1' and state['account_session'] is None):
                    cardTemplate("Peringatan!", "Anda harus login terlebih dahulu untuk melanjutkan proses .")
                    menuLogin(state)
                elif(aksi == '0'):
                    continue
                else:
                    cardTemplate("Peringatan!",f"Input {aksi} tidak valid, silahkan masukan input yang sesuai.")
            else:
                print("[0] Kembali")
                aksi = input("Masukan aksi: ").lower()
                if(aksi == '0'):
                    continue
        else:
            cardTemplate("Peringatan!",f"Input {input_navigasi} tidak valid, silahkan masukan input yang sesuai.")
            
            
