import pandas as pd

# from applyJobs import applyJobs
from negotiateCatalog import negotiateCatalog
from utility import cardTemplate, askInput, login

def catalogList(state):
    catalog_db = pd.read_csv('storage/catalog.csv')
    account_db = pd.read_csv('storage/user.csv')
    while True: 
        print("\n" + "="*44 + " Catalog List " + "="*44)
        
        # merged_db = catalog_db.merge(account_db, on='user_id', how='left', suffixes=('_post', '_user'))
        # print(merged_db[['content', 'type', 'username', 'location']])

        # no_width = len(str(len(catalog_db))) + 2
        # content_width = max(catalog_db['content'].astype(str).apply(len).max(), len("Content")) + 2
        # type_width = max(catalog_db['type'].astype(str).apply(len).max(), len("Type")) + 2

        # # Header
        # print(
            
        #     f"{'No'.ljust(no_width)}| "
        #     f"{'Content'.ljust(content_width)}| "
        #     f"{'Type'.ljust(type_width)}"
        # )

        # print("-" * (no_width + content_width + type_width + 4))

        # # Isi
        # for i, row in catalog_db.iterrows():
        #     user_id = row['user_id']
        #     user_info = account_db[account_db['user_id'] == user_id].iloc[0]
        #     print(
        #         f"{str(i+1).ljust(no_width)}| "
        #         f"{row['content'].ljust(content_width)}| "
        #         f"{row['type'].ljust(type_width)}"
        #         f" (made by {user_info['username']} in {user_info['location']})"
        #     )

        print(catalog_db[['catalog_id','title', 'theme', 'budget', 'status']].to_string(index=False))    

        print("="*102)

        if (state['account_session'] is not None):
            print("Aksi: \n[k] Kembali \n[x] Keluar dari program \n[s] logout.")
        else:
            print("Aksi: \n[k] Kembali \n[x] Keluar dari program")
        input_navigasi = (input("Masukan nomor id untuk melihat detailnya atau aksi: "))

        if (input_navigasi == "k"):
            return
        elif (input_navigasi == "x"):
            exit()
        elif (input_navigasi == "s" and state['account_session'] is not None):
            cardTemplate("Berhasil!","Anda Telah Logout dari akun " + state['account_session']['username'] + ".")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif (1 <= int(input_navigasi) <= len(catalog_db)):
            selected_index = int(input_navigasi) - 1
            selected_post = catalog_db.iloc[selected_index]

            user_info = account_db[account_db['user_id'] == selected_post['user_id']].iloc[0]

            print("\n" + "="*40 + " DETAIL CATALOG " + "="*40)
            print(f"Title  : {selected_post['title']}")
            print(f"Description: \n{selected_post['description']}")
            print(f"\nTheme: {selected_post['theme']}")
            print(f"Budget : {selected_post['budget']}")
            print(f"\nby @{user_info['username']} in {user_info['location']}")
            print("="*98)
            aksi = input("Jika tertarik ketik '1' untuk melanjutkan proses, atau '0' untuk kembali: ")
            if (aksi == '1' and state['account_session'] is not None):
                negotiateCatalog(state, selected_post, user_info)
            elif (aksi == '1' and state['account_session'] is None):
                cardTemplate("Peringatan!", "Anda harus login terlebih dahulu untuk melanjutkan proses .")
                state["input_navigasi"] = 1
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
            
            
