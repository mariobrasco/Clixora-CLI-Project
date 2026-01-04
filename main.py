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
    # jumlah_nav = 6
    print("\n" + "="*44 + " BERANDA " + "="*44)
    print("📷  CLIXORA  📷")
    print("Temukan Fotografer Sempurna untuk Momen Spesial Anda.")
    print("[T] Tentang Clixora")
    print("[C] Cara Penggunaan (How To Use)")
    print("[A] About Us")
    print("-----------------")
    print("[1] Login            [4] List Pekerjaan") 
    print("[2] Registrasi       [5] Unggah Lowongan Pekerjaan")
    print("[3] List Catalog     [6] Unggah Catalog")
    print("[X] Keluar")
    print("="*103)

def navSudahLogin():
    global jumlah_nav
    # jumlah_nav = 4
    print("\n" + "="*44 + " BERANDA " + "="*32 + f" {state["account_session"]['username']} ({state["account_session"]['role']}) ")
    print("        📷  CLIXORA  📷")
    print("Temukan Fotografer Sempurna untuk Momen Spesial Anda.")
    print("[T] Tentang Clixora")
    print("[C] Cara Penggunaan (How To Use)")
    print("[A] About Us")
    print("-----------------")
    print("[1] Profil Saya") 
    print("[2] List Catalog")
    print("[3] List Pekerjaan")
    if (state["account_session"]['role'] == "finder"):
        print("[4] Unggah Lowongan Pekerjaan")
    else:
        print("[4] Unggah Catalog")
    print("[X] Keluar")
    print("[L] Logout")
    print("="*103)
    

#Main Program Loop
while True:
    # print(state)
    
    #Landing Page
    if (state["account_session"] is None ):
        navBelumLogin()
        state["input_navigasi"] = (input(f"Masukkan aksi yang diinginkan: ").lower())
    else:
        navSudahLogin()
        state["input_navigasi"] = (input(f"Masukkan aksi yang diinginkan: ").lower())

    #Validasi Input Navigasi
    if (state["account_session"] is None):
        if state["input_navigasi"] not in ["x", "t", "c", "a", "1", "2", "3", "4", "5", "6"]:
            cardTemplate("Peringatan!", f"Input '{state['input_navigasi']}' tidak valid, silahkan masukan input yang sesuai.")
            continue
    else:
        if state["input_navigasi"] not in ["x", "l", "t", "c", "a", "1", "2", "3", "4"]:
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
    
    if (state["input_navigasi"] == "t"):
        cardTemplate("Tentang Kami","Clixora adalah sebuah platform berbasis website yang berfungsi \nsebagai finder untuk mempertemukan pencari jasa (Finder) dengan \npenyedia jasa fotografer. Platform ini memungkinkan pengguna untuk \nmencari fotografer, melakukan negosiasi harga, serta membuat lowongan \njasa fotografi yang lebih spesifik sesuai kebutuhan.")
    elif (state["input_navigasi"] == "c"):
        cardTemplate("Cara Penggunaan","1. Registrasi akun sebagai 'photografer' atau 'finder'.\n2. Login ke akun yang telah dibuat.\n3. Jika Anda seorang 'finder', Anda dapat mencari fotografer \ndan mengunggah lowongan pekerjaan.\n4. Jika Anda seorang 'photografer', Anda dapat mencari pekerjaan \ndan mengunggah katalog fotografi Anda.\n5. Gunakan menu navigasi untuk mengakses fitur-fitur yang tersedia.")    
    elif (state["input_navigasi"] == "a"):
        cardTemplate("About Us","Contact Info: \nMuhammad Arkan Athaya  : athayaarkan8@student.upi.edu \nMario Brasco Putra Hamdani : mariobrasco@student.upi.edu \nZahra Amelia Ramadhani  : zahraamelia@student.upi.edu")
        
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