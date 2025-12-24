import os
print("WORKING DIRECTORY:", os.getcwd())

import pandas as pd

# BACA DATA CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'storage', 'jobs.csv')

postAJob_csv = pd.read_csv(CSV_PATH)

# MENU FILTER (OPSIONAL)
def menu_filter():
    global postAJob_csv

    data_asli = postAJob_csv.copy()

    print("\n" + "="*40)
    print(" MENU FILTER LOWONGAN ")
    print("="*40)

    print("[1] Filter berdasarkan Judul")
    print("[2] Filter berdasarkan Tipe Budget")
    print("[3] Filter berdasarkan Minimal Budget")
    print("[4] Filter berdasarkan Rentang Budget")
    print("[0] Tanpa Filter")

    pilihan = input("Pilih filter (opsional): ")

    if pilihan == '1':
        kata = input("Masukkan kata kunci judul: ")
        postAJob_csv = postAJob_csv[
            postAJob_csv['judul'].str.contains(kata, case=False, na=False)
        ]

    elif pilihan == '2':
        print("1 = Budget Per Jam")
        print("2 = Budget Proyek")
        tipe = input("Pilih tipe budget: ")

        if tipe in ['1', '2']:
            postAJob_csv = postAJob_csv[
                postAJob_csv['tipe_budget'] == int(tipe)
            ]

    elif pilihan == '3':
        min_budget = input("Masukkan minimal budget: ")
        if min_budget.isdigit():
            postAJob_csv = postAJob_csv[
                postAJob_csv['budget'] >= int(min_budget)
            ]

    elif pilihan == '4':
        min_budget = input("Budget minimum: ")
        max_budget = input("Budget maksimum: ")

        if min_budget.isdigit() and max_budget.isdigit():
            postAJob_csv = postAJob_csv[
                (postAJob_csv['budget'] >= int(min_budget)) &
                (postAJob_csv['budget'] <= int(max_budget))
            ]

    elif pilihan == '0':
        postAJob_csv = data_asli

    postAJob_csv = postAJob_csv.reset_index(drop=True)

# KODE ASLI KAMU
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

                keterangan_tipe = "Budget Per Jam"
                if job['tipe_budget'] == 2:
                    keterangan_tipe = "Budget Proyek"

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

# JALANKAN PROGRAM
menu_filter()
find_work()
