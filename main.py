import pandas as pd
from createCatalog import formCatalog
import postAJob as postJob
import findWork as findWork

from profile import profilePage 
from utility import autoIncrementUserId, askInput, cardTemplate, login, menuLogin
from catalog import catalogList

account_db = pd.read_csv('storage/user.csv')
state = {
    "account_session": None, 
    "input_navigasi": None,
    }

#Menu Navigasi
def navBelumLogin():
    global jumlah_nav
    jumlah_nav = 6
    print("\n" + "="*44 + " LANDING PAGE " + "="*44)
    print("Selamat Datang di Clixora!, disini adalah tempat photografer mendapat finder dan finder mendapat photografer.")
    print("1. Login") 
    print("2. Registrasi")
    print("3. Catalog List")
    print("4. Cari Pekerjaan")
    print("5. Unggah Lowongan Pekerjaan")
    print("6. Unggah Catalog Saya")
    print("-----------------")
    print("X. Keluar")
    print("="*103)

def navSudahLogin():
    global jumlah_nav
    jumlah_nav = 4
    print("\n" + "="*44 + " HOME " + "="*32 + f" {state["account_session"]['username']} ({state["account_session"]['role']}) ")
    print("1. Profil Saya") 
    print("2. Catalog List")
    print("3. Cari Pekerjaan")
    if (state["account_session"]['role'] == "finder"):
        print("4. Unggah Lowongan Pekerjaan")
    else:
        print("4. Unggah Catalog")
    print("-----------------")
    print("X. Keluar")
    print("99. Logout")
    print("="*103)
    

#Main Program Loop
while True:
    # print(state)
    
    #Landing Page
    if (state["account_session"] is None ):
        navBelumLogin()
        state["input_navigasi"] = (input(f"Masukkan angka untuk navigasi (1-{jumlah_nav}) atau x untuk keluar: "))
    else:
        navSudahLogin()
        state["input_navigasi"] = (input(f"Masukkan angka untuk navigasi (1-{jumlah_nav}) atau x untuk keluar 99 untuk logout: "))

    #Validasi Input Navigasi
    if (state["account_session"] is None):
        if state["input_navigasi"] not in [str(i) for i in range(1, jumlah_nav + 1)] + ["x"]:
            cardTemplate("Peringatan!", f"Input '{state['input_navigasi']}' tidak valid, silahkan masukan input yang sesuai.")
            continue
    else:
        if state["input_navigasi"] not in [str(i) for i in range(1, jumlah_nav + 1)] + ["x", "99"]:
            cardTemplate("Peringatan!", f"Input '{state['input_navigasi']}' tidak valid, silahkan masukan input yang sesuai.")
            continue
    
    #Keluar Program
    if (state["input_navigasi"] == "x"):
        cardTemplate("Terimakasih", "Terimakasih Telah menggunakan program ini.")
        # exit()
        break
    
    #Logout
    if (state["input_navigasi"] == "99"):
        cardTemplate("Berhasil", f"Anda telah logout dari akun {state['account_session']['username']}.")
        state['account_session'] = None
        state["input_navigasi"] = None

    #Page List Catalog
    if (state["account_session"] is not None and state["input_navigasi"] == "2" or state["account_session"] is None and state["input_navigasi"] == "3"):
        catalogList(state)

    #Post Job / Upload Catalog
    if (state["account_session"] is not None and state["input_navigasi"] == "4"):
        if (state["account_session"]['role'] == "finder"):
            postJob.form_post_job(state)
        elif (state["account_session"]['role'] == "photografer"):
            formCatalog(state)
    elif (state["account_session"] is None and state["input_navigasi"] == "5"):
        cardTemplate("Peringatan!", "Anda harus login terlebih dahulu sebagai finder untuk mengunggah lowongan pekerjaan.")
    elif (state["account_session"] is None and state["input_navigasi"] == "6"):
        cardTemplate("Peringatan!", "Anda harus login terlebih dahulu sebagai photografer untuk mengunggah catalog.")

    #Page List Jobs
    if (state["account_session"] is not None and state["input_navigasi"] == "3" or state["account_session"] is None and state["input_navigasi"] == "4"):
        findWork.find_work(state)

    #Login
    if (state["account_session"] is None and state["input_navigasi"] == "1"):
        menuLogin(state)
        state["input_navigasi"] = None

    #Page Profil  
    if (state["account_session"] is not None and state["input_navigasi"] == "1"):
        profilePage(state)
    
    #Registrasi
    if (state["account_session"] is None and state["input_navigasi"] == "2"):
        while True:
            print("\n" + "="*44 + " MENU REGISTRASI " + "="*44)
            print("Apakah anda Photografer atau Finder?")
            print("1. Photografer")
            print("2. Finder")
            role_picked = (input("Masukan nomor sesuai tipe akun yang diinginkan: "))
            role_id = "null"
            if (role_picked == "1"):
                role_id = "p"
                role_name = "photografer"
                break
            elif(role_picked == "2"):
                role_id = "f"
                role_name = "finder"
                break
            else:
                cardTemplate("Peringatan", f"input '{role_picked}' tidak valid, silahkan masukan nomor yang sesuai (1 dan 2)")
                
        print("\n" + "="*44 + " MENU REGISTRASI " + "="*44)
        print("Jika Ingin membatalkan registrasi, ketik 'batal' saat menginputkan data")
        
        input_username = askInput("Masukkan username: ")
        if (input_username):
            input_password = askInput("Masukkan password: ")
            if (input_password):
                input_email = askInput("Masukkan email: ")
                if (role_id == "p" and input_email):
                    input_location = askInput("Masukkan lokasi: ")
                    if (input_location):
                        input_bio = askInput("Masukkan bio: ")
                        if (input_bio):
                            new_id = autoIncrementUserId(role_id)
                            reg_data = {
                                'user_id': new_id, 
                                'username': input_username, 
                                'password': input_password, 
                                'role': role_name, 
                                'location': input_location, 
                                'email': input_email, 
                                'bio': input_bio
                            }
                            new_account = pd.DataFrame([reg_data])
                            new_account.to_csv('storage/user.csv', mode='a', header=False, index=False)
                            print("="*90)
                            login(input_username, input_password, state)
                            cardTemplate("Berhasil", f"Berhasil registrasi sebagai {role_name}.\nSelamat Datang, {input_username}!")
                            
                elif (role_id == "f" and input_email):
                    new_id = autoIncrementUserId(role_id)
                    reg_data = {
                        'user_id': new_id, 
                        'username': input_username, 
                        'password': input_password,
                        'role': role_name,
                        'location':  "",
                        'email': input_email, 
                        'bio': ""
                    }
                    new_account = pd.DataFrame([reg_data])
                    new_account.to_csv('storage/user.csv', mode='a', header=False, index=False)
                    print("="*90)
                    
                    login(input_username, input_password, state) 
                    cardTemplate("Berhasil", f"Berhasil registrasi sebagai {role_name}.\nSelamat Datang, {input_username}!")
    
    #Registrasi--