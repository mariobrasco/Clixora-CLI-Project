import pandas as pd
from createCatalog import formCatalog
import postAJob as postJob
import findJobs as findjobs

from profile import profilePage 
from userPost import myApplications, myCatalog, myJobs, myOrders
from utility import cardTemplate, headerTemplate, footerTemplate
from catalog import catalogList
from loginRegister import menuLogin, menuRegistrasi

account_db = pd.read_csv('storage/user.csv')
state = {
    "account_session": None, 
    "input_navigasi": None,
    }

#Menu Navigasi
def navBelumLogin():
    headerTemplate("BERANDA")
    print("📷  CLIXORA  📷")
    print("Dalam Aplikasi ini semua yang dikurungi oleh '[]' adalah aksi yang dapat dipilih.")
    print("Temukan Fotografer Sempurna untuk Momen Spesial Anda.")
    print("[T] Tentang Clixora")
    print("[C] Cara Penggunaan (How To Use)")
    print("[A] Tentang Kami")
    print("-----------------")
    print("[1] Login            [3] List Catalog") 
    print("[2] Registrasi       [4] List Pekerjaan")
    print("[X] Keluar")
    footerTemplate()

def navSudahLogin():
    headerTemplate("BERANDA", state, profile=True)
    print("📷  CLIXORA  📷")
    print("Dalam Aplikasi ini semua yang dikurungi oleh '[]' adalah aksi yang dapat dipilih.")
    print("Temukan Fotografer Sempurna untuk Momen Spesial Anda.")
    print("[T] Tentang Clixora")
    print("[C] Cara Penggunaan (How To Use)")
    print("[A] Tentang Kami")
    print("-----------------")
    print(f"[1] Profil Saya      [3] List Pekerjaan      {'  [5] Lowongan Saya' if state['account_session']['role'] == 'finder' else '  [5] Catalog Saya'}" ) 
    print(f"[2] List Catalog    {' [4] Unggah Lowongan' if state['account_session']['role'] == 'finder' else ' [4] Unggah Catalog'}       {'[6] Pesanan Saya' if state['account_session']['role'] == 'finder' else ' [6] Lamaran Saya'}")
    print("[X] Keluar           [L] Logout")
    footerTemplate()
    

#Main Program Loop
while True:
    #Landing Page
    if (state["account_session"] is None ):
        navBelumLogin()
        state["input_navigasi"] = (input(f"Masukkan aksi yang diinginkan: ").lower())
    else:
        navSudahLogin()
        state["input_navigasi"] = (input(f"Masukkan aksi yang diinginkan: ").lower())

    #Validasi Input Navigasi
    if (state["account_session"] is None):
        if state["input_navigasi"] not in ["x", "t", "c", "a", "1", "2", "3", "4"]:
            cardTemplate("Peringatan!", f"Input '{state['input_navigasi']}' tidak valid, silahkan masukan input yang sesuai.")
            continue
    else:
        if state["input_navigasi"] not in ["x", "l", "t", "c", "a", "1", "2", "3", "4", "5", "6"]:
            cardTemplate("Peringatan!", f"Input '{state['input_navigasi']}' tidak valid, silahkan masukan input yang sesuai.")
            continue
    
    #Keluar Program
    if (state["input_navigasi"] == "x"):
        cardTemplate("Terimakasih", "Terimakasih Telah menggunakan program CLIXORA CLI, Sampai Jumpa!")
        break
    
    #Logout
    if (state["input_navigasi"] == "l"):
        cardTemplate("Berhasil", f"Anda telah logout dari akun {state['account_session']['username']}.")
        state['account_session'] = None
        state["input_navigasi"] = None
    
    #Informasi Tentang Clixora, Cara Penggunaan, About Us
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

    #Page List Jobs
    if (state["account_session"] is not None and state["input_navigasi"] == "3" or state["account_session"] is None and state["input_navigasi"] == "4"):
        findjobs.findJobs(state)
    
    #Page User Posts
    if (state["input_navigasi"] == "6" and state["account_session"]["role"] == "finder"):
        myOrders(state)
    if (state["input_navigasi"] == "6" and state["account_session"]["role"] == "photographer"):
        myApplications(state)
    if (state["input_navigasi"] == "5" and state['account_session']['role'] == "photographer"):
        myCatalog(state) 
    if (state["input_navigasi"] == "5" and state["account_session"]["role"] == "finder"):
        myJobs(state)

    #Login
    if (state["account_session"] is None and state["input_navigasi"] == "1"):
        menuLogin(state)
        state["input_navigasi"] = None

    #Page Profil  
    if (state["account_session"] is not None and state["input_navigasi"] == "1"):
        profilePage(state)
    
    #Registrasi
    if (state["account_session"] is None and state["input_navigasi"] == "2"):
        menuRegistrasi(state)
    