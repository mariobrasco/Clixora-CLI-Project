import pandas as pd

from applyJobs import applyJobs
from utility import cardTemplate, mergeCSV, searchAndFilterByDataFrame, headerTemplate, footerTemplate
from loginRegister import menuLogin
from profile import viewUserProfile

def findJobs(state):
    merged_db = mergeCSV('storage/jobs.csv', 'storage/user.csv', 'user_id', 'user_id')
    searchWord = ""
    filter_theme = ""
    filter_budget = ""
    filter_location = ""
    filters = {}
    current_page = 1
    total_pages = 1
    tampilan_job = merged_db[['job_id','title', 'theme', 'budget', 'status', 'username', 'location_left']]
    
    while True:
        postAJob_csv = pd.read_csv('storage/jobs.csv')
        account_db = pd.read_csv('storage/user.csv')
        merged_db = mergeCSV('storage/jobs.csv', 'storage/user.csv', 'user_id', 'user_id')
        merged_db = merged_db.rename(columns={
            'job_id': 'Job Id',
            'title': 'Judul Lowongan',
            'theme': 'Tema',
            'budget': 'Budget',
            'status': 'Status',
            'username': 'Diupload Oleh',
            'location_left': 'Lokasi'
        })
        if (state['account_session'] is None):
            headerTemplate("FIND JOBS")
        else:
            headerTemplate("FIND JOBS", state, profile=True)
        print(f"Cari    : ( {searchWord} ) [H] Hapus Pencarian ")
        print(f"Filter  : ({'(theme: ' + filter_theme + ')' if filter_theme else ''} {'(budget: ' + filter_budget + ')' if filter_budget else ''} {'(location: ' + filter_location + ')' if filter_location else ''}) [A] Hapus Filter")
        
        tampilan_job, total_pages = searchAndFilterByDataFrame(
            merged_db,
            keyword=searchWord,
            search_columns=['Judul Lowongan'],
            filters=filters,
            select_columns=['Job Id','Judul Lowongan', 'Tema', 'Budget', 'Status', 'Diupload Oleh', 'Lokasi'],
            page=current_page,
            per_page=10
        )
        
        footerTemplate()
        
        if (tampilan_job.empty and not (searchWord or filters)):
            print("⚠️  Belum ada lowongan pekerjaan yang tersedia.")
        elif (tampilan_job.empty and (searchWord or filters)):
            print("⚠️  Tidak ada lowongan pekerjaan yang sesuai dengan kriteria pencarian dan/atau filter Anda.")
        else:
            print(tampilan_job.to_string(index=False))
        
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
        
        pilih = (input("Masukan Job id untuk melihat detailnya atau Aksi: ")).lower()

        if (pilih == 'k'):
            break
        elif (pilih == "x"):
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
            exit()
        elif (pilih == "l" and state['account_session'] is not None):
            cardTemplate("Berhasil!","Anda Telah Logout dari akun " + state['account_session']['username'] + ".")
            state['account_session'] = None
        elif (pilih == "c"):
            searchWord = input("Masukkan kata kunci pencarian: ")
        elif (pilih == "p" and current_page > 1):
            current_page -= 1
        elif (pilih == "n" and current_page < total_pages):
            current_page += 1
        elif (pilih == "a"):
            filters = {}
            filter_theme = ""
            filter_budget = ""
            filter_location = ""
        elif (pilih == "f"):
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
        elif (pilih == "h"):
            searchWord = ""      
        elif (pilih.isdigit() and int(pilih) in tampilan_job['Job Id'].values):
            selected_post = postAJob_csv[postAJob_csv['job_id'] == int(pilih)].iloc[0]
            user_info = account_db[account_db['user_id'] == selected_post['user_id']].iloc[0]
            
            if (user_info.empty):
                cardTemplate("Peringatan!","⚠️  Pengguna yang memposting pekerjaan ini tidak ditemukan.")
                return

            headerTemplate("DETAIL LOWONGAN PEKERJAAN", state, profile=True)

            print(f"Job ID        : {selected_post['job_id']}")
            print(f"Posted by     : {user_info['username']}")
            print(f"Judul         : {selected_post['title']}")
            print(f"Deskripsi     : {selected_post['description']}")
            print(f"Tema          : {selected_post['theme']}")
            print(f"Tipe Budget   : {selected_post['tipe_budget']}")
            print(f"Budget        : {selected_post['budget']}")
            print(f"Lokasi        : {selected_post['location']}")
            print(f"Tanggal       : {selected_post['date_needed']}")
            print(f"Waktu         : {selected_post['time']}")
            print(f"Status        : {selected_post['status']}")
            print("--------------------------------")

            if (state['account_session']['role'] == 'photographer'):
                print("[1] Lamar Pekerjaan ini      [2] Lihat Profil      [0] Kembali ")
                footerTemplate()
                aksi = input("Pilih aksi: ")
                
                if (aksi == '1' and state['account_session'] is not None):
                    applyJobs(state, selected_post)
                elif (aksi == '1' and state['account_session'] is None):
                    cardTemplate("Peringatan!","⚠️  Anda harus login terlebih dahulu untuk melamar pekerjaan.")
                    menuLogin(state)
                elif (aksi == '2'):
                    viewUserProfile(state, user_info['user_id'])
                elif (aksi == '0'):
                    continue
            elif (state['account_session']['role'] == 'finder'):
                print("[1] Lihat Profil     [0] Kembali")
                footerTemplate()
                aksi = input("Pilih aksi: ")
                if (aksi == '0'):
                    continue
                elif (aksi == '1'):
                    viewUserProfile(state, user_info['user_id'])
            
            else:
                cardTemplate("Peringatan!","⚠️  Job Id tidak ditemukan.")
        else:
            cardTemplate("Peringatan!","⚠️  Mohon masukkan input sesuai.")
