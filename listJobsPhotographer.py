import pandas as pd

from postAJob import validasi_angka

FILE_PATH_PHOTOGRAPHER = 'storage/listJobsPhotographer.csv'
FILE_PATH_FINDER = 'storage/listJobsFinder.csv'
list_jobs_photographer_db = pd.read_csv(FILE_PATH_PHOTOGRAPHER)
list_jobs_finder_db = pd.read_csv(FILE_PATH_FINDER)

def negotiateJob(message_no, new_budget):
    global list_jobs_photographer_db, list_jobs_finder_db

    index = message_no - 1
    if index < 0 or index >= len(list_jobs_photographer_db):
        print("Nomor tawaran tidak valid.")
        return False
 
    message_id = list_jobs_photographer_db.iloc[index]['message_id']

    list_jobs_photographer_db.at[index, 'negotiated_budget'] = new_budget
    list_jobs_photographer_db.at[index, 'status'] = 'negotiation'

    list_jobs_finder_db.loc[
        list_jobs_finder_db['message_id'] == message_id,
        'negotiated_budget'
    ] = new_budget

    list_jobs_finder_db.loc[
        list_jobs_finder_db['message_id'] == message_id,
        'status'
    ] = 'negotiation'

    list_jobs_photographer_db.to_csv(FILE_PATH_PHOTOGRAPHER, index=False)
    list_jobs_finder_db.to_csv(FILE_PATH_FINDER, index=False)

    print(f"\n💰 Negosiasi dikirim ke Finder: {new_budget}")
    return True


def updateJobStatus(message_no, new_status):
    global list_jobs_photographer_db
    global list_jobs_finder_db

    index = message_no - 1

    if index < 0 or index >= len(list_jobs_photographer_db):
        print("Nomor tawaran tidak valid.")
        return False

    list_jobs_photographer_db.at[index, 'status'] = new_status
    list_jobs_photographer_db.to_csv(FILE_PATH_PHOTOGRAPHER, index=False)

    return True


def removeJob(message_no):
    global list_jobs_photographer_db

    index = message_no - 1

    if index < 0 or index >= len(list_jobs_photographer_db):
        print("Nomor tawaran tidak valid.")
        return False

    list_jobs_photographer_db = list_jobs_photographer_db.drop(index).reset_index(drop=True)
    list_jobs_photographer_db.to_csv(FILE_PATH_PHOTOGRAPHER, index=False)

    return True


def listJobsPhotographer():
    global list_jobs_photographer_db

    while True:
        print("\n" + "="*63 + " List Tawaran " + "="*63)

        if list_jobs_photographer_db.empty:
            print("Tidak ada tawaran yang tersedia.")
            return False

        display_db = list_jobs_photographer_db.reset_index(drop=True).rename_axis('No').reset_index().assign(No=lambda x: x['No'] + 1)
        print(display_db[['No', 'judul', 'deskripsi', 'tema', 'lokasi', 'tanggal', 'waktu', 'budget', 'status']])

        print(f"\nKetik nomor urut dari 1 sampai {len(list_jobs_photographer_db)} untuk menerima tawaran.")
        print("Ketik 'hapus' untuk menghapus tawaran.")
        print("Ketik 'x' untuk kembali.")

        accept = input("Pilih aksi: ").strip().lower()

        if accept == 'x':
            return False

        if accept == 'hapus':
            try:
                message_no = int(input("Masukkan nomor tawaran yang ingin dihapus: "))
                if removeJob(message_no):
                    print("\n🗑️ Tawaran berhasil dihapus.")
            except ValueError:
                print("\nNomor tawaran tidak valid.")
            continue

        if accept.isdigit() and 1 <= int(accept) <= len(list_jobs_photographer_db):
            back_to_list = False

            # confirm_negotiate = input("Apakah Anda ingin menegosiasikan budget? (y/n): ").lower()

            # if confirm_negotiate == 'y':
            #     new_budget = input("Masukkan budget baru yang diinginkan: ")
            #     index = int(accept) - 1
            #     list_jobs_photographer_db.at[index, 'negotiated_budget'] = new_budget
            #     list_jobs_photographer_db.to_csv(FILE_PATH_PHOTOGRAPHER, index=False)
            #     print(f"\n💰 Budget berhasil diajukan sebesar: {new_budget}")

            while True:
                print("\n💬 Photographer mengajukan negosiasi")
                print(f"💰 Budget diajukan: {list_jobs_photographer_db.iloc[int(accept) - 1]['negotiated_budget']}")
                print("\n(y) Terima tawaran\n(n) Tolak tawaran\n(b) Ajukan negosiasi budget\n(x) Kembali ke daftar tawaran")
                confirm = input("Terima tawaran ini? pilih diantara (y/n/b/x): ").lower()

                if confirm == 'y':
                    selected_message = list_jobs_photographer_db.iloc[int(accept) - 1]
                    updateJobStatus(int(accept), 'accepted')
                    print(f"\n✅ Tawaran diterima: {selected_message['judul']}")
                    print("📌 Status berubah menjadi Accepted")
                    back_to_list = True
                    break

                elif confirm == 'n':
                    selected_message = list_jobs_photographer_db.iloc[int(accept) - 1]
                    updateJobStatus(int(accept), 'rejected')
                    print(f"\n❌ Tawaran ditolak: {selected_message['judul']}")
                    print("📌 Status berubah menjadi Rejected")
                    back_to_list = True
                    break

                elif confirm == 'b':
                    new_budget = input("Masukkan budget baru: ")

                    if not validasi_angka(new_budget) or int(new_budget) <= 0:
                        print("\nBudget harus berupa angka dan lebih dari 0.")
                        continue

                    negotiateJob(int(accept), new_budget)
                    print("💬 Negosiasi balasan dikirim ke Finder.")
                    back_to_list = True
                    break

                elif confirm == 'x':
                    back_to_list = True
                    break

                else:
                    print("\nInput tidak valid.")

            if back_to_list:
                continue

        else:
            print("\nPilihan tidak valid.")

# listJobsPhotographer()