import pandas as pd

from applyJobs import applyJobs
from loginRegister import menuLogin
from negotiateCatalog import negotiateCatalog
from utility import cardTemplate, headerTemplate, footerTemplate

def profilePage(state):
    while True:
        # ===== ambil data user =====
        account_db = pd.read_csv('storage/user.csv')
        user_idx = account_db.index[ account_db['user_id'] == state['account_session']['user_id']][0]
        user_info = account_db.loc[user_idx]

        # ===== sinkronkan role dari login =====
        account_db.at[user_idx, 'role'] = state['account_session']['role']

        # ===== tampilkan profil =====
        headerTemplate("PROFIL SAYA", state, profile=False)
        print(f"Username   : {user_info['username']}")
        print(f"Email      : {user_info['email']}")
        print(f"Role       : {state['account_session']['role']}")

        if state['account_session']['role'] == "photographer":
            print(f"Lokasi     : {user_info['location']}")
            print(f"Bio        : {user_info['bio']}")

        # ===== menu aksi =====
        print("--------------------------------")
        print(
            f"[P] Pesanan saya     [E] Edit Akun    \n"
            f"[C] Katalog saya     {'[B] Tambah Bio' if state['account_session']['role'] == 'photographer' else ''}     \n"
            f"[K] Kembali          [X] Keluar           [L] Logout"
        )
        footerTemplate()
        aksi = input("Masukan aksi: ").lower()

        # ===== aksi user =====
        if aksi == "k":
            break
        elif aksi == "x":
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
            exit()

        # ===== edit data =====
        elif aksi == "e":
            headerTemplate("EDIT PROFIL SAYA", state, profile=False)
            print("\nSilahkan kosongkan kolom jika tidak diubah")
            username = input("Username : ")
            email =    input("Email    : ")
            password = input("Password : ")

            if (username):
                account_db.at[user_idx, 'username'] = username
                state['account_session']['username'] = username
                
            if (password):
                account_db.at[user_idx, 'password'] = password

            if (email):
                account_db.at[user_idx, 'email'] = email

            account_db.to_csv('storage/user.csv', index=False)
            cardTemplate("Berhasil!", "Data Akun berhasil diperbaharui")

        # ===== tambah bio =====
        elif aksi == "b" and state['account_session']['role'] == "photographer":
            bio = input("Masukan bio: ")
            account_db.at[user_idx, 'bio'] = bio
            account_db.to_csv('storage/user.csv', index=False)
            cardTemplate("Berhasil!", "Bio berhasil ditambahkan")

        elif (aksi == "l"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  {state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            break

def viewUserProfile(state, user_id):
    while True:
        account_db = pd.read_csv('storage/user.csv')
        catalog_db = pd.read_csv('storage/catalog.csv')
        jobs_db = pd.read_csv('storage/jobs.csv')
        user_info = account_db[ account_db['user_id'] == user_id].iloc[0]
        tampilan_pemilik = {}
        kolom_tampilan = []
        
        if (user_info.empty):
            cardTemplate("Peringatan!", f"User dengan ID {user_id} tidak ditemukan.")
            break
        elif (user_info['role'] == 'photographer'):
            tampilan_pemilik = catalog_db[catalog_db['user_id'] == user_id]
            tampilan_pemilik = tampilan_pemilik.rename(columns={
                'catalog_id': 'Catalog Id',
                'title': 'Judul',
                'theme': 'Tema',
                'budget': 'Budget',
                'tipe_budget': 'Tipe Budget',
                'sold_count': 'Terjual'
            })
            kolom_tampilan = ['Catalog Id', 'Judul', 'Tema', 'Budget', 'Tipe Budget']
        elif (user_info['role'] == 'finder'):
            tampilan_pemilik = jobs_db[jobs_db['user_id'] == user_id]
            tampilan_pemilik = tampilan_pemilik.rename(columns={
                'job_id': 'Job Id',
                'title': 'Judul',
                'theme': 'Tema',
                'budget': 'Budget',
                'tipe_budget': 'Tipe Budget'
            })
            kolom_tampilan = ['Job Id', 'Judul', 'Tema', 'Budget', 'Tipe Budget']
        
        headerTemplate(f"PROFIL {user_info['username']}", state, profile=True)
        print(f"Username   : {user_info['username']}")
        print(f"Email      : {user_info['email']}")
        print(f"Role       : {user_info['role']}")
        if (user_info['role'] == "photographer"):
            print(f"Lokasi     : {user_info['location']}")
            print(f"Bio        : {user_info['bio']}")
        headerTemplate("DAFTAR " + ("CATALOG" if (user_info['role'] == 'photographer') else "LOWONGAN PEKERJAAN") + " YANG DIUNGGAH", state, profile=False)
        if user_info['role'] == 'photographer':
            print("Jumlah Catalog yang diunggah: ", len(tampilan_pemilik), "|", "Jumlah Catalog Terjual: ", tampilan_pemilik['Terjual'].sum())
        if (tampilan_pemilik.empty):
            print(f"{user_info['role']} belum mengunggah apapun.")
        else:
            print(tampilan_pemilik[kolom_tampilan].to_string(index=False))
        print("--------------------------------")
       
        print("[K] Kembali      [X] Keluar")
        footerTemplate()
        
        aksi = input(f"Masukan {'Catalog Id' if (user_info['role'] == 'photographer') else 'Job Id'} atau aksi: ").lower()

        if aksi == "k":
            break
        elif aksi == "x":
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
            exit()
        elif (aksi.isdigit() and int(aksi) in catalog_db['catalog_id'].values and user_info['role'] == 'photographer'):
            selected_post = catalog_db[catalog_db['catalog_id'] == int(aksi)].iloc[0]
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
                
        elif (aksi.isdigit() and int(aksi) in jobs_db['job_id'].values and user_info['role'] == 'finder'):
            selected_post = jobs_db[jobs_db['job_id'] == int(aksi)].iloc[0]
            user_info = account_db[account_db['user_id'] == selected_post['user_id']].iloc[0]
            
            if (user_info.empty):
                cardTemplate("Info!","⚠️  Pengguna yang memposting pekerjaan ini tidak ditemukan.")
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
                print("[1] Lamar Pekerjaan ini      [0] Kembali ")
                footerTemplate()
                aksi = input("Pilih aksi: ")
                
                if (aksi == '1' and state['account_session'] is not None):
                    applyJobs(state, selected_post)
                elif (aksi == '1' and state['account_session'] is None):
                    cardTemplate("Peringatan!","⚠️  Anda harus login terlebih dahulu untuk melamar pekerjaan.")
                elif (aksi == '0'):
                    continue
            elif (state['account_session']['role'] == 'finder'):
                print("[0] Kembali")
                footerTemplate()
                aksi = input("Pilih aksi: ")
                if (aksi == '0'):
                    continue
            
        else:
            cardTemplate("Peringatan!","⚠️  Job Id tidak ditemukan.")