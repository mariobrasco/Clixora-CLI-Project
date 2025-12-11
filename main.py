import pandas as pd

id_nav = 0
jumlah_nav = 0

#Menu Navigasi
def nav_belum_login():
    global jumlah_nav
    # global id_nav
    # id_nav = 0
    jumlah_nav = 2
    print("\n============== MENU NAVIGASI ===============")
    print("1. Login") 
    print("2. Registrasi")
    print("0. Keluar")
    print("============================================")

def nav_sudah_login():
    global jumlah_nav
    # global id_nav
    # id_nav = 1
    jumlah_nav = 2
    print("\n============== MENU NAVIGASI ===============")
    print("1. Profil Saya") 
    print("2. For You Page")
    # print("3. K")
    print("0. Keluar")
    print("99. Logout")
    print("============================================")
#Menu Navigasi--

def nav_hub():
    global input_navigasi
    
    if (id_nav == 0):
        nav_belum_login()
        input_navigasi = int(input(f"Masukkan angka untuk navigasi (1-{jumlah_nav}) atau 0 untuk keluar: "))
    elif (id_nav == 1):
        nav_sudah_login()
        input_navigasi = int(input(f"Masukkan angka untuk navigasi (1-{jumlah_nav}) atau 0 untuk keluar: "))

def login(username, password):
    account_db = pd.read_csv('user.csv')
    account = account_db[(account_db['username'] == username) & (account_db['password'] == password)]
    
    return not account.empty

while True:
    
    nav_hub()

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
        #Fetch ke .txt
            
        elif (login(input_username, input_password)):
            print(f"Berhasil login sebagai {input_username}, Selamat datang!")
            id_nav = 1 
        else:
            print("Gagal login, username atau password salah.")
    #Login--
    
    if (id_nav == 0 and input_navigasi == 2):
        print("\n============================ MENU REGISTRASI =================================")
        print("Jika Ingin membatalkan registrasi, ketik 'batal' pada username atau password")
        
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
            new_account = pd.DataFrame({'username': [input_username], 'password': [input_password]})
            new_account.to_csv('user.csv', mode='a', header=False, index=False)
            print(f"Berhasil registrasi sebagai {input_username}, silahkan login.")
            
    if (input_navigasi == 99):
        print("Berhasil logout, sampai jumpa!")
        id_nav = 0
    if (input_navigasi == 0):
        print("Terimakasih Telah menggunakan program ini.")
        break