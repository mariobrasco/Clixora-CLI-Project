import pandas as pd
from utility import login, askInput, cardTemplate, validasiEmail, autoIncrementUserId

def menuLogin(state):
    print("\n" + "="*44 + " MENU LOGIN " + "="*44)
    print("Jika Ingin membatalkan login, ketik 'batal'\n")
    
    input_username = askInput("*Masukkan username: ", True)
    if (input_username):
        input_password = askInput("*Masukkan password: ", True)
        if (input_password):
            if(login(input_username, input_password, state)):
                print("="*90)
                cardTemplate("Berhasil!",f"Berhasil login sebagai {state['account_session']['role']}, Selamat datang, {input_username}!")
            else:
                cardTemplate("Peringatan!", "Gagal login, username atau password salah.")

def menuRegistrasi(state):
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
    
    input_username = askInput("*Masukkan username: ", True)
    if (input_username):
        input_password = askInput("*Masukkan password: ", True)
        if (input_password):
            while True:
                input_email = askInput("*Masukkan email: ", True)
                if (not validasiEmail(input_email)):
                    cardTemplate("Peringatan!", f"Email '{input_email}' tidak valid, silahkan masukan email yang sesuai.")
                    continue
                if (role_id == "p" and input_email):
                    input_location = askInput("*Masukkan lokasi: ", True)
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
                            break    
                elif (role_id == "f" and input_email and validasiEmail(input_email)):
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
                    break
