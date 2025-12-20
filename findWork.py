import pandas as pd

postAJob_csv = pd.read_csv('storage/postAJob.csv')

def validasi_angka(teks):
    for char in teks:
        if char < '0' or char > '9':
            return False
    return True

def find_work():
    while True:
        print("\n" + "="*50 + " Find Work " + "="*50)
        
        print(postAJob_csv)
        print("="*125)

        print("\nKetik nomor index (angka paling kiri) untuk melihat detail.")
        print("Ketik 'x' untuk kembali.")
        
        pilih = input("Pilih lowongan: ")

        if pilih == 'x':
            print("Keluar dari Find Work.")
            break

        if pilih != "" and validasi_angka(pilih):
            
            index = int(pilih)

            if index >= 0 and index < len(postAJob_csv):
                
                job = postAJob_csv.iloc[index]

                keterangan_tipe = "Hourly Price"
                if job['tipe_budget'] == 2:
                    keterangan_tipe = "Project Price"

                print("\n" + "="*60)
                print(f" DETAIL PEKERJAAN (ID: {index}) ")
                print("=" * 60)

                for i, (key, value) in enumerate(job.items(), start=1):
                    if key == "tipe_budget":
                        print(f"{i}. {key:<12}: {value} ({keterangan_tipe})")
                    elif key == "budget":
                        print(f"{i}. {key:<12}: Rp {value}")
                    else:
                        print(f"{i}. {key:<12}: {value}")

                print("#" * 60)

                print("\n[1] Lamar Pekerjaan ini")
                print("[0] Kembali ke menu awal")
                
                aksi = input("Pilih aksi: ")
                
                if aksi == '1':
                    print(f"\n✅ Berhasil melamar ke: {job['judul']}")
                
            else:
                print("⚠️  Nomor index tidak ditemukan.")
        else:
            print("⚠️  Mohon masukkan input berupa angka.")

# find_work()