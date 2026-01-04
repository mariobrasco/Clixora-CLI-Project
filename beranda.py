import pandas as pd

DB_FILE = 'storage/contact.csv'

def validasiEmail(email):
    if "@" not in email or "." not in email:
        return False

    parts = email.split("@")

    if len(parts) != 2:
        return False

    if "." not in parts[1]:
        return False

    return True

def simpanPesan(nama, email, pesan):
    data_baru = {
        'nama': [nama],
        'email': [email],
        'pesan': [pesan],
        'timestamp': [pd.Timestamp.now()]
    }

    df_baru = pd.DataFrame(data_baru)
    
    try:
        pd.read_csv(DB_FILE)
        df_baru.to_csv(DB_FILE, mode='a', header=False, index=False)
    except FileNotFoundError:
        df_baru.to_csv(DB_FILE, mode='w', header=True, index=False)

def separator():
    print("\n" + "="*50)

def main():
    berjalan = True
    
    while berjalan:
        # --- HEADER MENU ---
        separator()
        print("        📷  CLIXORA TERMINAL APP  📷")
        print("Temukan Fotografer Sempurna untuk Momen Spesial Anda.")
        separator()
        print("1. Tentang Clixora")
        print("2. Cara Penggunaan (How to use Clixora)")
        print("3. Hubungi Kami")
        print("4. Keluar")
        separator()
        
        pilihan = input("Pilih Menu (1-4): ")

        # --- LOGIKA MENU ---
        if pilihan == '1':
            separator()
            print(">> TENTANG KAMI")
            print("Clixora adalah sebuah platform berbasis website yang berfungsi \nsebagai finder untuk mempertemukan pencari jasa (Finder) dengan \npenyedia jasa fotografer. Platform ini memungkinkan pengguna untuk \nmencari fotografer, melakukan negosiasi harga, serta membuat lowongan \njasa fotografi yang lebih spesifik sesuai kebutuhan.")
            
        elif pilihan == '2':
            separator()
            print(">> CARA PENGGUNAAN")
            print("[A] Finder: Register/Login -> Cari Jasa -> Deal")
            print("[B] Photographer: Upload Katalog -> Kerja -> Kelola dan Negosiasi")
            
        elif pilihan == '3':
            separator()
            print(">> HUBUNGI KAMI")
            print("Silakan isi data di bawah. (Disimpan ke contact.csv)\n")
            
            nama = input("Nama Lengkap : ")
            email = input("Alamat Email : ")
            pesan = input("Isi Pesan    : ")
            
            if nama and email and pesan:
                if validasiEmail(email) == False:
                    print("\n❌ Gagal. Alamat email tidak valid.")
                    print("Kembali ke menu utama...")
                else:
                    simpanPesan(nama, email, pesan)
                    print("✅ Sukses! Pesan Anda telah tersimpan di contact.csv")
            else:
                print("\n❌ Gagal. Semua data wajib diisi.")
                
        elif pilihan == '4':
            print("\nTerima kasih telah menggunakan Clixora. Sampai jumpa!")
            berjalan = False
            
        else:
            print("\n❌ Pilihan tidak valid, silakan coba lagi.")

main()