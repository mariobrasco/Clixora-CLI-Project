import pandas as pd

from userPost import myApplications, myCatalog, myJobs, myOrders
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

        if state['account_session']['role'] == "photografer":
            print(f"Lokasi     : {user_info['location']}")
            print(f"Bio        : {user_info['bio']}")

        # ===== menu aksi =====
        print("--------------------------------")
        print(
            f"[P] Pesanan saya     [E] Edit Profil    \n"
            f"[C] Katalog saya     [B] Tambah Bio     \n"
            f"[K] Kembali          [L] Logout\n"
            f"[X] Keluar"
        )
        footerTemplate()
        aksi = input("Masukan aksi: ").lower()

        # ===== aksi user =====
        if aksi == "k":
            return
        elif aksi == "x":
            cardTemplate("Terima Kasih!","Terima kasih telah menggunakan Clixora CLI. Sampai jumpa!")
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

        elif (aksi == "l"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  {state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return