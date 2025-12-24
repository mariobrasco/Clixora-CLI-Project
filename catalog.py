import pandas as pd
from applyJobs import applyJobs

def catalogList(state):
    post_db = pd.read_csv('storage/post.csv')
    account_db = pd.read_csv('storage/user.csv')

    # FILTER OPSIONAL
    filtered_post_db = post_db  # default: tanpa filter

    print("\nApakah ingin menggunakan filter?")
    print("1. Ya")
    print("2. Tidak")

    pilih_filter = input("Pilih (1/2): ").strip()

    if pilih_filter == '1':
        print("\nFilter berdasarkan TYPE")
        available_types = post_db['type'].unique()
        print("Tipe tersedia:", ", ".join(available_types))

        selected_type = input("Masukkan type (kosongkan untuk batal): ").strip()

        if selected_type:
            hasil_filter = post_db[post_db['type'] == selected_type]
            if hasil_filter.empty:
                print("Tidak ada data dengan type tersebut. Menampilkan semua data.")
            else:
                filtered_post_db = hasil_filter
    # ==================================================

    while True:
        print("\n" + "="*44 + " Catalog List " + "="*44)

        no_width = len(str(len(filtered_post_db))) + 2
        content_width = max(filtered_post_db['content'].astype(str).apply(len).max(), len("Content")) + 2
        type_width = max(filtered_post_db['type'].astype(str).apply(len).max(), len("Type")) + 2

        # Header
        print(
            f"{'No'.ljust(no_width)}| "
            f"{'Content'.ljust(content_width)}| "
            f"{'Type'.ljust(type_width)}"
        )

        print("-" * (no_width + content_width + type_width + 4))

        # Isi
        for i, row in filtered_post_db.iterrows():
            user_id = row['user_id']
            user_info = account_db[account_db['user_id'] == user_id].iloc[0]
            print(
                f"{str(i+1).ljust(no_width)}| "
                f"{row['content'].ljust(content_width)}| "
                f"{row['type'].ljust(type_width)}"
                f" (made by {user_info['username']} in {user_info['location']})"
            )

        print("="*102)

        if state['account_session'] is not None:
            print("Ketik 'kembali' untuk kembali, ketik 'x' untuk keluar dari program dan 'logout' untuk logout.")
        else:
            print("Ketik 'kembali' untuk kembali, ketik 'x' untuk keluar dari program.")

        input_navigasi = input("Masukan nomor postingan untuk melihat detailnya : ")

        if input_navigasi == "kembali":
            return
        elif input_navigasi == "x":
            exit()
        elif input_navigasi == "logout":
            print("Logout...")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif input_navigasi.isdigit() and 1 <= int(input_navigasi) <= len(filtered_post_db):
            selected_index = int(input_navigasi) - 1
            selected_post = filtered_post_db.iloc[selected_index]

            user_info = account_db[account_db['user_id'] == selected_post['user_id']].iloc[0]

            print("\n" + "="*40 + " DETAIL POSTINGAN " + "="*40)
            print(f"Content: \n{selected_post['content']}")
            print(f"\nType: {selected_post['type']}")
            print(f"by @{user_info['username']} in {user_info['location']}")
            print("="*98)

            aksi = input(
                "Jika tertarik dengan postingan ini ketik 1 untuk melanjutkan transaksi, atau 0 untuk kembali:"
            )
            if aksi == '1':
                applyJobs()
            else:
                print("Kembali ke For You Page.")
        else:
            print("Nomor postingan tidak valid!")

if __name__ == "__main__":
    state = {
        "account_session": None,
        "input_navigasi": None
    }
    catalogList(state)
