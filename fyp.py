import pandas as pd

post_db = pd.read_csv('storage/post.csv')
account_db = pd.read_csv('storage/user.csv')

def forYouPage(state):
    while True: 
        print("\n" + "="*44 + " For You Page " + "="*44)
        
        # merged_db = post_db.merge(account_db, on='user_id', how='left', suffixes=('_post', '_user'))
        # print(merged_db[['content', 'type', 'username', 'location']])

        no_width = len(str(len(post_db))) + 2
        content_width = max(post_db['content'].astype(str).apply(len).max(), len("Content")) + 2
        type_width = max(post_db['type'].astype(str).apply(len).max(), len("Type")) + 2

        # Header
        print(
            
            f"{'No'.ljust(no_width)}| "
            f"{'Content'.ljust(content_width)}| "
            f"{'Type'.ljust(type_width)}"
        )

        print("-" * (no_width + content_width + type_width + 4))

        # Isi
        for i, row in post_db.iterrows():
            user_id = row['user_id']
            user_info = account_db[account_db['user_id'] == user_id].iloc[0]
            print(
                f"{str(i+1).ljust(no_width)}| "
                f"{row['content'].ljust(content_width)}| "
                f"{row['type'].ljust(type_width)}"
                f" (made by {user_info['username']} in {user_info['location']})"
            )
        # print("-----------------")
        # print("0. Keluar")
        print("="*102)

        if (state['account_session'] is not None):
            print("Ketik 'kembali' untuk kembali, ketik 'x' untuk keluar dari program dan 'logout' untuk logout.")
        else:
            print("Ketik 'kembali' untuk kembali, ketik 'x' untuk keluar dari program.")
        input_navigasi = (input("Masukan nomor postingan untuk melihat detailnya : "))

        if (input_navigasi == "kembali"):
            return
        elif (input_navigasi == "x"):
            exit()
        elif (input_navigasi == "logout"):
            print("Logout...")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif (1 <= int(input_navigasi) <= len(post_db)):
            selected_index = int(input_navigasi) - 1
            selected_post = post_db.iloc[selected_index]

            user_info = account_db[account_db['user_id'] == selected_post['user_id']].iloc[0]

            print("\n" + "="*40 + " DETAIL POSTINGAN " + "="*40)
            print(f"Content: \n{selected_post['content']}")
            print(f"\nType: {selected_post['type']}")
            print(f"by @{user_info['username']} in {user_info['location']}")
            print("="*98)
            aksi = input("Jika tertarik dengan postingan ini ketik 1 untuk melanjutkan transaksi, atau 0 untuk kembali:")
            if (aksi == '1'):
                print(f"Berhasil Memilih Tawaran {selected_post['content']} dari @{user_info['username']}")
                print("Ketik '1' untuk melanjutkan dan '0' untuk batal")
            else:
                print("Kembali ke For You Page.")
        else:
            print("Nomor postingan tidak valid!")

    
# forYouPage()