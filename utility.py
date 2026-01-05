import pandas as pd

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
    if (required and not value):
        cardTemplate("Required!", "Input tidak boleh kosong, silahkan coba lagi.")
        return askInput(message, required)
    
    return value

def cardTemplate(title, message):
    print("\n" + "="*44 + f" {title} " + "="*44)
    print(message)
    
    panjang_text = int(88+len(title)+2)
    print("="*panjang_text)
    
def validasiEmail(email):
    if "@" not in email or "." not in email:
        return False

    parts = email.split("@")
    if len(parts) != 2:
        return False

    if "." not in parts[1]:
        return False

    return True

# ======================= CRUD ======================= 

def updateRowById(db_name, key_column, id_value, update_data):
    
    db = pd.read_csv(db_name)
    selected_row = db[key_column] == id_value
    
    for key, value in update_data.items():
        db.loc[selected_row, key] = value
    
    db.to_csv(db_name, index=False)
    cardTemplate("Berhasil", "Data berhasil diperbarui.")

def deleteRowById(db_name, key_column, id_value):
    db = pd.read_csv(db_name)
    cardTemplate("Peringatan!", f"Apakah anda yakin untuk Menghapus data {db[db[key_column] == id_value].to_string(index=False)}? \n[Y] Ya \n[N] Tidak")
    confirm = input("Masukkan pilihan Anda: ")
    
    if (confirm.lower() == 'y'):
        db = db[db[key_column] != id_value]
        db.to_csv(db_name, index=False)
        cardTemplate("Berhasil", "Data berhasil dihapus.")
        
    if (confirm.lower() == 'n'):
        cardTemplate("Info!", "Penghapusan data dibatalkan.")
        
    db = pd.read_csv(db_name)