import pandas as pd

# ======================= Helper  ======================= 
def login(username, password, state):
    account_db = pd.read_csv('storage/user.csv')
    account = account_db[(account_db['username'] == username) & (account_db['password'] == password)]
    
    if (not account.empty):
        state["account_session"] = account.iloc[0]
    return not account.empty

def autoIncrementUserId(role_id):
    account_db = pd.read_csv('storage/user.csv')
    # Filter existing IDs by role prefix (p or f)
    role_users = account_db[account_db['user_id'].str.startswith(role_id)]

    if (len(role_users) == 0):
        new_number = 1
    else:
        max_id = role_users['user_id'].str[1:].astype(int).max()
        new_number = max_id + 1

    # Format number into 3 digits (e.g., 001, 002, 015)
    new_user_id = f"{role_id}{new_number:03}"
    return new_user_id

def autoIncrementCustom(char, db_name, column_name):
    account_db = pd.read_csv(db_name)

    # Filter rows that start with the given prefix
    prefix_users = account_db[
        account_db[column_name].astype(str).str.startswith(char)
    ]

    if len(prefix_users) == 0:
        new_number = 1
    else:
        # Remove prefix dynamically based on its length
        max_id = (
            prefix_users[column_name].str[len(char):].astype(int).max()
        )
        new_number = max_id + 1

    # Always format as 3 digits
    new_id = f"{char}{new_number:03}"
    return new_id

def autoIncrementNumber(db_name):
    if (db_name.empty):
        return 1
    else:
        latest_id = db_name.iloc[-1, 0] or 0
        new_id = int(latest_id) + 1
        return new_id

def askInput(message, required):
    value = input(message)
    
    if (value.lower() == "batal"):
        cardTemplate("Info!", "Operasi dibatalkan, kembali ke menu Sebelumnya")
        return 
    if (value.lower() == "lupa"):
        return "lupa"
    if (required and not value):
        cardTemplate("Required!", "Input tidak boleh kosong, silahkan coba lagi.")
        return askInput(message, required)
    
    return value

def cardTemplate(title, message):
    panjang_card = int(len(message))
    if ((panjang_card % 2) != 0):
        panjang_card +=1
    panjang_header = panjang_card // 2
    print("\n" + "="*panjang_header + f" {title} " + "="*panjang_header)
    print(message)
    
    panjang_text = int(panjang_card+len(title)+2)
    print("="*panjang_text)
    
def headerTemplate(title, state=None, profile=False):
    max_length = 120
    panjang_title = len(title)
    each_side = (max_length - panjang_title - 2) // 2
    left_side = each_side
    info_side = each_side
    
    if (profile):
        profile_info = len(f" {state['account_session']['username']} ({state['account_session']['role']})")
        info_side = each_side - profile_info
        
    if ((each_side * 2 + panjang_title + 2) > max_length ):
        left_side -= 1
    elif ((each_side * 2 + panjang_title + 2) < max_length ):
        info_side += 1
    
    # print(left_side, info_side, panjang_title, )
    print("\n" + "="*left_side + f" {title} " + "="*info_side + " " + (state['account_session']['username'] + f" ({state['account_session']['role']})" if profile and state else ""))

def footerTemplate():
    print("="*120)

def validasiAngka(teks):
    for char in teks:
        if char < '0' or char > '9':
            return False
    return True

def validasiEmail(email):
    if "@" not in email or "." not in email:
        return False

    parts = email.split("@")
    if len(parts) != 2:
        return False

    if "." not in parts[1]:
        return False

    return True

def validasiTanggal(tanggal):
    # format: dd-mm-yyyy → length 10
    if len(tanggal) != 10:
        return False

    if tanggal[2] != "-" or tanggal[5] != "-":
        return False

    hari_str = tanggal[0:2]
    bulan_str = tanggal[3:5]
    tahun_str = tanggal[6:10]

    if not (validasiAngka(hari_str) and validasiAngka(bulan_str) and validasiAngka(tahun_str)):
        return False

    hari = int(hari_str)
    bulan = int(bulan_str)
    tahun = int(tahun_str)

    if hari < 1 or hari > 31:
        return False
    if bulan < 1 or bulan > 12:
        return False
    if tahun < 1000 or tahun > 9999:
        return False

    return True

def validasiWaktu(waktu):
    if len(waktu) != 5:
        return False
    if waktu[2] != ":":
        return False

    jam = waktu[0:2]
    menit = waktu[3:5]

    if not (validasiAngka(jam) and validasiAngka(menit)):
        return False

    jam = int(jam)
    menit = int(menit)

    if jam < 0 or jam > 23:
        return False
    if menit < 0 or menit > 59:
        return False

    return True

# ======================= CRUD ======================= 
def getAllData(db_name):
    db = pd.read_csv(db_name)
    start_no = 1
    db.insert(0, 'No', range(start_no, start_no + len(db)))
    return db

def getDataSpesificColumn(db_name, select_columns):
    db = pd.read_csv(db_name)
    db = db[select_columns]
    return db

def getRowById(db_name, key_column, id_value):
    db = pd.read_csv(db_name)
    selected_row = db[db[key_column] == id_value]
    return selected_row

def mergeCSV(
    left_db,
    right_db,
    left_key,
    right_key,
    how='left',
    suffixes=('_left', '_right')
):
    left = pd.read_csv(left_db)
    right = pd.read_csv(right_db)

    return pd.merge(
        left,
        right,
        left_on=left_key,
        right_on=right_key,
        how=how,
        suffixes=suffixes
    )

def searchAndFilterByDBName(
    db_name,
    keyword=None,
    search_columns=None,
    filters=None,
    select_columns=None
):
    db = pd.read_csv(db_name)

    # Filter
    if filters:
        for col, val in filters.items():
            if isinstance(val, list):
                db = db[db[col].isin(val)]
            else:
                db = db[db[col] == val]

    # Search
    if keyword:
        if search_columns is None:
            search_columns = db.columns

        mask = False
        for col in search_columns:
            mask = mask | db[col].astype(str).str.contains(keyword, case=False, na=False)

        db = db[mask]

    # Columns
    if select_columns:
        db = db[select_columns]

    return db

def searchAndFilterByDataFrame(
    df,
    keyword=None,
    search_columns=None,
    filters=None,
    select_columns=None,
    page=1,
    per_page=5
):
    # Filter
    if filters:
        for col, val in filters.items():
            if isinstance(val, list):
                df = df[df[col].isin(val)]
            else:
                df = df[df[col] == val]

    # Search
    if keyword:
        if search_columns is None:
            search_columns = df.columns

        mask = False
        for col in search_columns:
            mask = mask | df[col].astype(str).str.contains(keyword, case=False, na=False)

        df = df[mask]

    # Select columns
    if select_columns:
        valid_cols = [c for c in select_columns if c in df.columns]
        df = df[valid_cols]

    # 🔹 total pages (before slicing)
    total_rows = len(df)
    total_pages = total_rows // per_page
    if total_rows % per_page != 0:
        total_pages += 1

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    df = df.iloc[start:end]

    # Add 'no' column (starts from 1)
    start_no = (page - 1) * per_page + 1
    df.insert(0, 'No', range(start_no, start_no + len(df)))

    return df, total_pages

def updateRowById(db_name, key_column, id_value, update_data):
    
    db = pd.read_csv(db_name)
    selected_row = db[key_column] == id_value
    
    for key, value in update_data.items():
        db.loc[selected_row, key] = value
    
    db.to_csv(db_name, index=False)
    cardTemplate("Berhasil", "Data berhasil diperbarui.")

def deleteRowById(db_name, key_column, id_value, message=""):
    db = pd.read_csv(db_name)
    cardTemplate("Peringatan!", f"{message}, Yakin? \n[Y] Ya     [N] Tidak")
    confirm = input("Masukkan pilihan Anda: ")
    
    if (confirm.lower() == 'y'):
        db = db[db[key_column] != id_value]
        db.to_csv(db_name, index=False)
        cardTemplate("Berhasil", "Data berhasil dihapus.")
        return True
        
    if (confirm.lower() == 'n'):
        cardTemplate("Info!", "Penghapusan data dibatalkan.")
        return False
        
    db = pd.read_csv(db_name)

def deleteInstant(db_name, key_column, id_value):
    db = pd.read_csv(db_name)
    
    db = db[db[key_column] != id_value]
    db.to_csv(db_name, index=False)
    # cardTemplate("Berhasil", "Data berhasil dihapus.")
        
    db = pd.read_csv(db_name)
        
# ======================= Select ======================= 
def selectTheme(picked=None):
    picked_themes = picked if picked else []
    themes = [
        "Wedding", "School", "Event", "Nature", "Aerial", "Sports",
        "Product", "Street", "Documentary", "Fashion", "Advertising",
        "Vintage", "Outdoor", "Indoor"
    ]
    
    while True:
        print("="*40 + " TEMA PILIHAN " + "="*40)
        count = 0

        for i, theme in enumerate(themes, start=1):
            label = f"[{i}] {theme}"

            if theme in picked_themes:
                label += " (✓)"

            print(label.ljust(20), end="")

            count += 1
            if count == 4:
                print()
                count = 0

        print()
        print("-------------------------")
        print("[D] Selesai memilih")
        print("[R] Hapus tema terpilih")
        print("[X] Batal")
        print("="*88)

        pilihan = input("Pilih tema (nomor / D / R / X): ").lower()

        # Cancel
        if pilihan == 'x':
            cardTemplate("Info!", "Operasi dibatalkan, kembali ke menu sebelumnya")
            return None

        # Done
        if pilihan == 'd':
            if not picked_themes:
                print("\nMinimal pilih 1 tema.\n")
                continue
            return picked_themes

        # Remove selected theme
        if pilihan == 'r':
            if not picked_themes:
                print("\nBelum ada tema yang dipilih.\n")
                continue

            print("\nTema terpilih:")
            for i, theme in enumerate(picked_themes, start=1):
                print(f"[{i}] {theme}")

            remove_input = input("Masukkan nomor tema yang ingin dihapus: ")

            if remove_input.isdigit():
                idx = int(remove_input)
                if 1 <= idx <= len(picked_themes):
                    removed = picked_themes.pop(idx - 1)
                    cardTemplate("Berhasil!", f"'{removed}' berhasil dihapus.")
                else:
                    cardTemplate("Peringatan!", "Nomor tidak valid.")
            else:
                cardTemplate("Peringatan!", "Input harus berupa angka.")

            continue

        # Add theme
        if pilihan.isdigit():
            idx = int(pilihan)
            if 1 <= idx <= len(themes):
                selected_theme = themes[idx - 1]
                if selected_theme in picked_themes:
                    cardTemplate("Info!", "Tema sudah dipilih.")
                else:
                    picked_themes.append(selected_theme)
                    cardTemplate("Berhasil!", f"'{selected_theme}' berhasil ditambahkan.")
            else:
                cardTemplate("Peringatan!", "Pilihan tidak valid.")
        else:
            cardTemplate("Peringatan!", "Input tidak dikenali.")
