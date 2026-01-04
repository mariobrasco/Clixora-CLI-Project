import pandas as pd

from userPost import myApplications, myCatalog, myJobs, myOrders
from utility import cardTemplate


def profilePage(state):
    while True:
        # ===== ambil data user =====
        account_db = pd.read_csv('storage/user.csv')
        user_idx = account_db.index[
            account_db['user_id'] == state['account_session']['user_id']
        ][0]
        user_info = account_db.loc[user_idx]

        # ===== sinkronkan role dari login =====
        account_db.at[user_idx, 'role'] = state['account_session']['role']

        # ===== tampilkan profil =====
        print("\n" + "=" * 44 + " Profil Saya " + "=" * 44)
        print(f"Username   : {user_info['username']}")
        print(f"Email      : {user_info['email']}")
        print(f"Role       : {state['account_session']['role']}")

          # ===== bio (jika ada) =====
        if 'bio' in user_info and pd.notna(user_info['bio']) and user_info['bio']:
            print(f"Bio        : {user_info['bio']}")

        # ===== sosial media (tampil sesuai yang diisi user) =====
        sosmed = {
            "Instagram": "instagram",
            "Twitter": "twitter",
            "Facebook": "facebook"
        }

        for label, field in sosmed.items():
            if field in user_info and pd.notna(user_info[field]) and user_info[field]:
                print(f"{label:<11}: {user_info[field]}")

        print("=" * 101)

        # ===== menu aksi =====
        print(
            f"Aksi:\n"
            f"[e] Edit data profil\n"
            f"[b] Tambahkan bio\n"
            f"[s] Link sosial media\n"
            f"[k] Kembali\n"
            f"[x] Keluar\n"
            f"{'[c] Katalog saya' if state['account_session']['role'] == 'photografer' else '[j] Lowongan saya'}"
        )

        aksi = input("Masukan aksi: ").lower()

        # ===== aksi user =====
        if aksi == "k":
            return

        elif aksi == "x":
            exit()

        # ===== edit data profil (TANPA ROLE) =====
        elif aksi == "e":
            print("\nEdit data profil (kosongkan jika tidak diubah)")
            username = input("Username : ")
            email = input("Email    : ")

            if username:
                account_db.at[user_idx, 'username'] = username
                state['account_session']['username'] = username

            if email:
                account_db.at[user_idx, 'email'] = email

            account_db.to_csv('storage/user.csv', index=False)
            cardTemplate("Berhasil!", "Data profil berhasil diperbaharui")

        # ===== tambah bio =====
        elif aksi == "b" and state['account_session']['role'] == "photografer":
            bio = input("Masukan bio: ")
            account_db.at[user_idx, 'bio'] = bio 
            account_db.to_csv('storage/user.csv', index=False)
            cardTemplate("Berhasil!", "Bio berhasil ditambahkan")
            
        # ===== tambah link sosial media =====
        elif aksi == "s":
            print("\nKetik '-' jika ingin mengosongkan")
            
            instagram = input("Instagram : ")
            twitter = input("Twitter : ")
            facebook = input("Facebook : ")
            if instagram:
                account_db.at[user_idx, 'instagram'] = instagram
            if twitter:
                account_db.at[user_idx, 'twitter'] = twitter
            if facebook:
                account_db.at[user_idx, 'facebook'] = facebook  
                
            account_db.to_csv('storage/user.csv', index=False)
            cardTemplate("Berhasil", "Ssosial media berhasil disimpan")

        # ===== katalog fotografer =====
        elif aksi == "c" and state['account_session']['role'] == "photografer":
            myCatalog(state)
            # listJobsFinder(state)    
        elif (aksi == "j" and state["account_session"]["role"] == "finder"):
            myJobs(state)
            # listJobsFinder(state)
        elif (aksi == "x"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  @{state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return