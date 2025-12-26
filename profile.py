import pandas as pd

from userPost import myApplications, myCatalog, myJobs, myOrders
from utility import cardTemplate

def profilePage(state):
    account_db = pd.read_csv('storage/user.csv')
    user_info = account_db[account_db['user_id'] == state['account_session']['user_id']].iloc[0]
    while True:
        print("\n" + "="*44 + " Profil Saya " + "="*44)
        # print(account_db[account_db['user_id'] == state['account_session']['user_id']].to_string(index=False))
        print(f"Username   : {user_info['username']}")
        print(f"Email      : {user_info['email']}")
        print(f"Role       : {user_info['role']}")
        if (user_info['role'] == "photografer"):
            print(f"Lokasi     : {user_info['location']}")
            print(f"Bio        : {user_info['bio']}")
        print("="*101)

        print(f"Aksi: \n[k] Kembali \n[x] Keluar dari program \n[s] logout \n{'[c] Catalog saya' if (state["account_session"]["role"] == "photografer") else '[j] Lowongan Saya'} \n{'[a] Lamaran saya' if (state["account_session"]["role"] == "photografer") else '[p] Pesanan Saya'} .")
        aksi = (input("Masukan aksi: "))

        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "c" and state["account_session"]["role"] == "photografer"):
            myCatalog(state)
        elif (aksi == "j" and state["account_session"]["role"] == "finder"):
            myJobs(state)
        elif (aksi == "a" and state["account_session"]["role"] == "photografer"):
            myApplications(state)
        elif (aksi == "p" and state["account_session"]["role"] == "finder"):
            myOrders(state)
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  @{state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return