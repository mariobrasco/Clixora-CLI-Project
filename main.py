import pandas as pd

#Variables
id_nav = 0
jumlah_nav = 0
account_db = pd.read_csv('user.csv')

#Menu Navigasi
def navBelumLogin():
    global jumlah_nav
    jumlah_nav = 2
    print("\n============== MENU NAVIGASI ===============")
    print("1. Login") 
    print("2. Registrasi")
    print("0. Keluar")
    print("============================================")

def navSudahLogin():
    global jumlah_nav
    jumlah_nav = 2
    print("\n============== MENU NAVIGASI ===============")
    print("1. Profil Saya") 
    print("2. For You Page")
    print("0. Keluar")
    print("99. Logout")
    print("============================================")
#Menu Navigasi--

#Utiliy
def autoIncrementUserId(role_id):
    # Filter existing IDs by role prefix (p or f)
    role_users = account_db[account_db['user_id'].str.startswith(role_id)]

    if len(role_users) == 0:
        new_number = 1
    else:
        max_id = role_users['user_id'].str[1:].astype(int).max()
        new_number = max_id + 1

    # Format number into 3 digits (e.g., 001, 002, 015)
    new_user_id = f"{role_id}{new_number:03}"
    return new_user_id


#Utility--

def navHub():
    global input_navigasi
    
    if (id_nav == 0):
        navBelumLogin()
        input_navigasi = int(input(f"Masukkan angka untuk navigasi (1-{jumlah_nav}) atau 0 untuk keluar: "))
    elif (id_nav == 1):
        navSudahLogin()
        input_navigasi = int(input(f"Masukkan angka untuk navigasi (1-{jumlah_nav}) atau 0 untuk keluar: "))

def login(username, password):
    account = account_db[(account_db['username'] == username) & (account_db['password'] == password)]
    
    return not account.empty

while True:
    
    navHub()

    #Login
    if (id_nav == 0 and input_navigasi == 1):
        print("\n============================ MENU LOGIN =================================")
        print("Jika Ingin membatalkan login, ketik 'batal' pada username atau password")
        
        input_username = input("Masukkan username: ")
        if (input_username == "batal"):
            print("Login dibatalkan, kembali ke menu navigasi.")
        elif (input_username != "batal"):
            input_password = input("Masukkan password: ")
            if (input_password == "batal"):
                print("Login dibatalkan, kembali ke menu navigasi.")
                
        print("=========================================================================")
        
        if (input_username == "batal" or input_password == "batal"):
            print("Login dibatalkan, kembali ke menu navigasi.")
            
        elif (login(input_username, input_password)):
            print(f"Berhasil login sebagai {input_username}, Selamat datang!")
            id_nav = 1 
        else:
            print("Gagal login, username atau password salah.")
    #Login--
    
    #Registrasi
    if (id_nav == 0 and input_navigasi == 2):
        
        while True:
            print("\n============================ MENU REGISTRASI =================================")
            print("Apakah anda Photografer atau Finder?")
            print("1. Photografer")
            print("2. Finder")
            role_picked = (input("Masukan nomor sesuai tipe akun yang diinginkan: "))
            role_id = "null"
            if (role_picked == "1"):
                role_id = "p"
                break
            elif(role_picked == "2"):
                role_id = "f"
                break
            else:
                print(f"'{role_picked}' tidak valid, silahkan masukan nomor yang sesuai (1 dan 2)")
                
        print("\n============================ MENU REGISTRASI =================================")
        print("Jika Ingin membatalkan registrasi, ketik 'batal' pada saat menginputkan data")
        
        input_username = input("Masukkan username: ")
        if (input_username == "batal"):
            print("Registrasi dibatalkan, kembali ke menu navigasi.")
        elif (input_username != "batal"):
            input_password = input("Masukkan password: ")
            if (input_password == "batal"):
                print("Registrasi dibatalkan, kembali ke menu navigasi.")
                
        print("=========================================================================")
        
        if (input_username == "batal" or input_password == "batal"):
            print("Registrasi dibatalkan, kembali ke menu navigasi.")
        else:
            new_id = autoIncrementUserId(role_id)
            new_account = pd.DataFrame({'user_id': [new_id], 'username': [input_username], 'password': [input_password]})
            new_account.to_csv('user.csv', mode='a', header=False, index=False)
            print(f"Berhasil registrasi sebagai {input_username}.")
            print(f"Selamat Datang, {input_username}")
            id_nav = 1
    #Registrasi--
    
    
    if (input_navigasi == 99):
        print("Berhasil logout, sampai jumpa!")
        id_nav = 0
    if (input_navigasi == 0):
        print("Terimakasih Telah menggunakan program ini.")
        break