import pandas as pd

post_db = pd.read_csv('Clixora-CLI-Project/storage/post.csv')
account_db = pd.read_csv('Clixora-CLI-Project/storage/user.csv')

def forYouPage(): 
    print("\n" + "="*44 + " For You Page " + "="*44)
    
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
    print("-----------------")
    print("6. Kembali")
    print("0. Keluar")
    print("99. logout")
    print("="*102) 
    print("Masukan 0 untuk keluar, 6 untuk kembali ke menu navigasi, atau 99 untuk logout.")
    input_navigasi = int(input(f"Masukan nomor postingan untuk melihat detailnya : "))
    if input_navigasi == 4:
        return 
    
# forYouPage()