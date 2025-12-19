import pandas as pd

FILE_PATH = 'storage/listJobs.csv'
messages_db = pd.read_csv(FILE_PATH)

def updateMessageStatus(message_no, new_status):
    global messages_db

    index = message_no - 1

    if index < 0 or index >= len(messages_db):
        print("Nomor tawaran tidak valid.")
        return False

    messages_db.at[index, 'status'] = new_status
    messages_db.to_csv(FILE_PATH, index=False)

    return True


def removeMessage(message_no):
    global messages_db

    index = message_no - 1

    if index < 0 or index >= len(messages_db):
        print("Nomor tawaran tidak valid.")
        return False

    messages_db = messages_db.drop(index).reset_index(drop=True)
    messages_db.to_csv(FILE_PATH, index=False)

    return True


def loadMessages():
    global messages_db

    while True:
        print("\n" + "="*63 + " List Tawaran " + "="*63)

        if messages_db.empty:
            print("Tidak ada tawaran yang tersedia.")
            return False

        display_db = messages_db.reset_index(drop=True).rename_axis('No').reset_index().assign(No=lambda x: x['No'] + 1)
        print(display_db[['No', 'judul', 'deskripsi', 'tema', 'lokasi', 'tanggal', 'waktu', 'tipe_budget', 'budget', 'status']])

        print(f"\nKetik nomor urut dari 1 sampai {len(messages_db)} untuk menerima tawaran.")
        print("Ketik 'hapus' untuk menghapus tawaran.")
        print("Ketik 'x' untuk kembali.")

        accept = input("Pilih aksi: ").strip().lower()

        if accept == 'x':
            return False

        if accept == 'hapus':
            try:
                message_no = int(input("Masukkan nomor tawaran yang ingin dihapus: "))
                if removeMessage(message_no):
                    print("\n🗑️ Tawaran berhasil dihapus.")
            except ValueError:
                print("\nNomor tawaran tidak valid.")
            continue

        if accept.isdigit() and 1 <= int(accept) <= len(messages_db):
            back_to_list = False

            while True:
                print("\n(y) Terima tawaran\n(n) Tolak tawaran\n(x) Kembali ke daftar tawaran")
                confirm = input("Terima tawaran ini? pilih diantara (y/n/x): ").lower()

                if confirm == 'y':
                    selected_message = messages_db.iloc[int(accept) - 1]
                    updateMessageStatus(int(accept), 'accepted')
                    print(f"\n✅ Tawaran diterima: {selected_message['judul']}")
                    print("📌 Status berubah menjadi Accepted")
                    back_to_list = True
                    break

                elif confirm == 'n':
                    selected_message = messages_db.iloc[int(accept) - 1]
                    updateMessageStatus(int(accept), 'rejected')
                    print(f"\n❌ Tawaran ditolak: {selected_message['judul']}")
                    print("📌 Status berubah menjadi Rejected")
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

loadMessages()