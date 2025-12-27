import pandas as pd

from postAJob import validasi_angka
from utility import cardTemplate

FILE_PATH_PHOTOGRAPHER = 'storage/listJobsPhotographer.csv'
FILE_PATH_FINDER = 'storage/jobsApplications.csv'

list_jobs_photographer_db = pd.read_csv(FILE_PATH_PHOTOGRAPHER)
list_jobs_finder_db = pd.read_csv(FILE_PATH_FINDER)


def syncFinderWithPhotographer():
    global list_jobs_finder_db, list_jobs_photographer_db

    for idx, row in list_jobs_finder_db.iterrows():
        match = list_jobs_photographer_db[
            list_jobs_photographer_db['applications_id'] == row['applications_id']
        ]

        if not match.empty:
            list_jobs_finder_db.at[idx, 'status'] = match.iloc[0]['status']
            list_jobs_finder_db.at[idx, 'negotiated_budget'] = match.iloc[0].get('negotiated_budget', '')

    list_jobs_finder_db.to_csv(FILE_PATH_FINDER, index=False)


def updateFinderJob(message_no, status=None, negotiated_budget=None):
    global list_jobs_finder_db, list_jobs_photographer_db

    index = message_no - 1
    if index < 0 or index >= len(list_jobs_finder_db):
        print("Nomor tidak valid.")
        return False

    applications_id = list_jobs_finder_db.iloc[index]['applications_id']

    if status:
        list_jobs_finder_db.at[index, 'status'] = status
        list_jobs_photographer_db.loc[
            list_jobs_photographer_db['applications_id'] == applications_id,
            'status'
        ] = status

    if negotiated_budget:
        list_jobs_finder_db.at[index, 'negotiated_budget'] = negotiated_budget
        list_jobs_finder_db.at[index, 'status'] = 'negotiation'

        list_jobs_photographer_db.loc[
            list_jobs_photographer_db['applications_id'] == applications_id,
            'negotiated_budget'
        ] = negotiated_budget

        list_jobs_photographer_db.loc[
            list_jobs_photographer_db['applications_id'] == applications_id,
            'status'
        ] = 'negotiation'

    list_jobs_finder_db.to_csv(FILE_PATH_FINDER, index=False)
    list_jobs_photographer_db.to_csv(FILE_PATH_PHOTOGRAPHER, index=False)

    return True


def listJobsFinder(state, job_id):
    global list_jobs_finder_db
    jobs_db = pd.read_csv('storage/jobs.csv')

    # syncFinderWithPhotographer()

    while True:
        print("\n" + "="*63 + " Tawaran Finder " + "="*63)

        if list_jobs_finder_db.empty:
            cardTemplate("Info!","Belum ada tawaran yang tersedia.")
            return

        # display_db = (
        #     list_jobs_finder_db
        #     .reset_index(drop=True)
        #     .rename_axis('No')
        #     .reset_index()
        #     .assign(No=lambda x: x['No'] + 1)
        # )
        applications_selected = list_jobs_finder_db[list_jobs_finder_db['job_id'] == job_id] 
        user_db = pd.read_csv('storage/user.csv')

        for index, row in applications_selected.iterrows():
            job_info = jobs_db[jobs_db['job_id'] == row['job_id']].iloc[0]
            print(
                f"{row['applications_id']}. "
                f"Title: {job_info['title']} | "
                f"Status: {row['status']} | "
                f"Budget Asli: {job_info['budget']} | "
                f"Budget Diajukan: {row['negotiated_budget']}  | "
                f"oleh @{user_db[user_db['user_id'] == row['user_id']].iloc[0]['username']}"
            )

        print(f"\nPilih nomor 1–{len(list_jobs_finder_db)}")
        print("(x) Kembali")

        choice = input("Pilih: ").lower()

        if choice == 'x':
            return 

        if not choice.isdigit() or not (1 <= int(choice) <= len(list_jobs_finder_db)):
            print("Pilihan tidak valid.")
            continue

        index = int(choice) - 1
        selected = list_jobs_finder_db.iloc[index]

        # jila belum ada negosiasi
        if pd.isna(selected['negotiated_budget']) or str(selected['negotiated_budget']).strip() == '':
            print("\n⏳ Menunggu negosiasi dari Photographer.")
            print("❗ Anda belum dapat melakukan aksi apa pun.")
            continue

        # jika sudah ada negosiasi
        while True:
            print("\n💬 Photographer mengajukan negosiasi")
            print(f"💰 Budget diajukan: {selected['negotiated_budget']}")
            print("\n(b) Ajukan negosiasi balik")
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

                updateFinderJob(int(choice), negotiated_budget=new_budget)
                print("💰 Negosiasi balasan dikirim ke Photographer.")
                break

            elif action == 'x':
                break

            else:
                print("Input tidak valid.")


# listJobsFinder()