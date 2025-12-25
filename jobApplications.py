import pandas as pd

from postAJob import validasi_angka
from utility import cardTemplate

# FILE_PATH_PHOTOGRAPHER = 'storage/catalogApplications.csv'
FILE_PATH_FINDER = 'storage/jobsApplications.csv'

# list_jobs_photographer_db = pd.read_csv(FILE_PATH_PHOTOGRAPHER)
list_jobs_finder_db = pd.read_csv(FILE_PATH_FINDER)


# def syncFinderWithPhotographer():
#     global list_jobs_finder_db, list_jobs_photographer_db

#     for idx, row in list_jobs_finder_db.iterrows():
#         match = list_jobs_photographer_db[
#             list_jobs_photographer_db['applications_id'] == row['applications_id']
#         ]

#         if not match.empty:
#             list_jobs_finder_db.at[idx, 'status'] = match.iloc[0]['status']
#             list_jobs_finder_db.at[idx, 'negotiated_budget'] = match.iloc[0].get('negotiated_budget', '')

#     list_jobs_finder_db.to_csv(FILE_PATH_FINDER, index=False)


# def updateFinderJob(message_no, status=None, negotiated_budget=None):
#     global list_jobs_finder_db, list_jobs_photographer_db

#     index = message_no - 1
#     if index < 0 or index >= len(list_jobs_finder_db):
#         print("Nomor tidak valid.")
#         return False

#     applications_id = list_jobs_finder_db.iloc[index]['applications_id']

#     if status:
#         list_jobs_finder_db.at[index, 'status'] = status
#         list_jobs_photographer_db.loc[
#             list_jobs_photographer_db['applications_id'] == applications_id,
#             'status'
#         ] = status

#     if negotiated_budget:
#         list_jobs_finder_db.at[index, 'negotiated_budget'] = negotiated_budget
#         list_jobs_finder_db.at[index, 'status'] = 'negotiation'

#         list_jobs_photographer_db.loc[
#             list_jobs_photographer_db['applications_id'] == applications_id,
#             'negotiated_budget'
#         ] = negotiated_budget

#         list_jobs_photographer_db.loc[
#             list_jobs_photographer_db['applications_id'] == applications_id,
#             'status'
#         ] = 'negotiation'

#     list_jobs_finder_db.to_csv(FILE_PATH_FINDER, index=False)
#     list_jobs_photographer_db.to_csv(FILE_PATH_PHOTOGRAPHER, index=False)

#     return True

def updateFinderJob(applications_id, status, negotiated_budget):
    global list_jobs_finder_db

    # selected = list_jobs_finder_db[list_jobs_finder_db['applications_id'] == applications_id].index[0]
    # if index < 0 or index >= len(list_jobs_finder_db):
    #     print("Nomor tidak valid.")
    #     return False

    selected_row = list_jobs_finder_db['applications_id'] == applications_id
    
    list_jobs_finder_db.loc[selected_row, 'status'] = status
    list_jobs_finder_db.loc[selected_row, 'negotiated_budget'] = negotiated_budget

    # if negotiated_budget:
    #     list_jobs_finder_db.at[index, 'negotiated_budget'] = negotiated_budget
    #     list_jobs_finder_db.at[index, 'status'] = 'negotiation'

    list_jobs_finder_db.to_csv(FILE_PATH_FINDER, index=False)

    return True


def listJobsFinder(state, job_id):
    global list_jobs_finder_db
    jobs_db = pd.read_csv('storage/jobs.csv')

    # syncFinderWithPhotographer()

    while True:
        print("\n" + "="*63 + " List Tawaran " + "="*63)

        if list_jobs_finder_db.empty:
            cardTemplate("Info!","Belum ada yang melamar lowongan anda.")
            return
        
        applications_selected = list_jobs_finder_db[list_jobs_finder_db['job_id'] == job_id] 
        user_db = pd.read_csv('storage/user.csv')
        job_info = jobs_db[jobs_db['job_id'] == job_id].iloc[0]
        
        print(f"Lowongan: {job_info['title']} | Budget Asli: {job_info['budget']}")
        for index, row in applications_selected.iterrows():
            print(
                f"Id Tawaran: {row['applications_id']}. "
                f"Budget Diajukan: {row['negotiated_budget']}  | "
                f"oleh @{user_db[user_db['user_id'] == row['user_id']].iloc[0]['username']}  |"
                f"Status: {row['status']}"
            )
        print("="*135)

        print(f"Aksi:")
        print("[x] Kembali")

        choice = input("Masukan Id Tawaran untuk menindak lanjuti atau Aksi: ").lower()

        if choice == 'x':
            return 

        # if not choice.isdigit() or not (1 <= int(choice) <= len(list_jobs_finder_db)):
        #     print("Pilihan tidak valid.")
        #     continue
        # index = int(choice) - 1
        
        selected =  applications_selected[applications_selected['applications_id'] == int(choice)].iloc[0]

        # jila belum ada negosiasi
        # if pd.isna(selected['negotiated_budget']) or str(selected['negotiated_budget']).strip() == '':
        #     print("\n⏳ Menunggu negosiasi dari Photographer.")
        #     print("❗ Anda belum dapat melakukan aksi apa pun.")
        #     continue
        
        if (selected['status'] == 'waiting for photographer'):
            cardTemplate("Info!","Menunggu Photographer merespon tawaran Anda.")
            continue
        
        if (selected['status'] == 'accepted'):
            cardTemplate("Info!","Tawaran sudah diterima sebelumnya.")
            continue
        
        while True:
            print("\n💬 Photographer mengajukan negosiasi")
            print(f"💰 Budget diajukan: {selected['negotiated_budget']}")
            print("\n[a] Terima tawaran")
            print("(b) Ajukan negosiasi balik")
            print("(x) Kembali")

            action = input("Aksi: ").lower()

            if action == 'b':
                new_budget = input("Masukkan budget baru: ")
                if new_budget <= '0':
                    print("\nBudget harus lebih dari 0.")
                    continue

                if not validasi_angka(new_budget):
                    print("\nBudget harus berupa angka.")
                    continue

                updateFinderJob(selected['applications_id'], status='waiting for response', negotiated_budget=new_budget)
                print("💰 Negosiasi balasan dikirim ke Photographer.")
                break
            
            elif action == 'a':
                updateFinderJob(selected['applications_id'], status='accepted', negotiated_budget=selected['negotiated_budget'])
                cardTemplate("Berhasil!",f"✅ Tawaran @{user_db[user_db['user_id'] == selected['user_id']].iloc[0]['username']} diterima dengan Harga {selected['negotiated_budget']}.")
                break

            elif action == 'x':
                break

            else:
                print("Input tidak valid.")


# listJobsFinder()