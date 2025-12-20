import pandas as pd

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

def autoIncrementNumber(db_name):
    if (db_name.empty):
        return 1
    else:
        latest_id = db_name.iloc[-1, 0] or 0
        new_id = int(latest_id) + 1
        return new_id

def askInput(prompt):
    value = input(prompt)
    if (value.lower() == "batal"):
        print("Operasi dibatalkan, kembali ke menu Sebelumnya")
        return None
    return value

def cardTemplate(title, message):
    print("\n" + "="*44 + f" {title} " + "="*44)
    print(message)
    panjang_text = int(88+len(title)+2)
    print("="*panjang_text)