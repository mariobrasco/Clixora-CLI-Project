import pandas as pd

from utility import cardTemplate, headerTemplate, footerTemplate, mergeCSV
from jobApplications import listJobsApplications, listJobsFinder
from catalogApplications import listCatalogApplications, listOrderApplications

#======================= PHOTOGRAFERS =======================
def myCatalog(state):
    while True:
        catalog_db = pd.read_csv('storage/catalog.csv')
        catalog_db_user = catalog_db[catalog_db['user_id'] == state['account_session']['user_id']]
        catalog_db_user = catalog_db_user.rename(columns={
            'catalog_id': 'Catalog Id',
            'title': 'Judul Catalog',
            'theme': 'Tema',
            'budget': 'Budget',
            'status': 'Status'
        })
        headerTemplate("Katalog Saya", state, profile=True)
        print(catalog_db_user[['Catalog Id','Judul Catalog', 'Tema', 'Budget', 'Status']].to_string(index=False))
        print("--------------------------------")
        print("[K] Kembali    [X] Keluar dari program     [S] logout.")
        footerTemplate()
        
        aksi = input("Masukan Catalog Id untuk melihat Detail atau Aksi: ")
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun {state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(aksi.isdigit() and int(aksi) in catalog_db_user['Catalog Id'].values):
            catalog_id = int(aksi)
            catalog_to_edit = catalog_db_user[catalog_db_user['Catalog Id'] == catalog_id].iloc[0]
            # cardTemplate("Info!", f"Anda memilih catalog dengan ID {catalog_id} dan judul '{catalog_to_edit['Judul Catalog']}' untuk diedit.")
            listCatalogApplications(state,catalog_id)


def myApplications(state):
    while True:
        # applications_db = pd.read_csv('storage/jobsApplications.csv')
        # applications_db_user = applications_db[applications_db['user_id'] == state['account_session']['user_id']]
        merged_db = mergeCSV('storage/jobsApplications.csv', 'storage/jobs.csv', 'job_id', 'job_id')
        merged_db = merged_db.rename(columns={
            'applications_id': 'Lamaran Id',
            'title': 'Judul Lowongan',
            'location': 'Lokasi',
            'theme': 'Tema',
            'date_needed': 'Tanggal',
            'time': 'Waktu',
            'negotiated_budget': 'Budget',
            'message': 'Pesan',
            'status_left': 'Status Lamaran'
        })
        headerTemplate("Lamaran Saya", state, profile=True)
        print(merged_db[['Lamaran Id', "Judul Lowongan", "Lokasi", "Tema", "Tanggal", "Waktu", "Pesan", 'Budget', 'Status Lamaran']].to_string(index=False))
        print("--------------------------------")
        print("[K] Kembali    [X] Keluar dari program     [S] logout.")
        footerTemplate()
        aksi = input("Masukan application id untuk melihat atau aksi: ")
        
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun {state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(int(aksi) in merged_db['Lamaran Id'].values):
            application_id = int(aksi)
            listJobsApplications(state,application_id)
            
#======================= FINDERS =======================
def myJobs(state):
    while True:
        jobs_db = pd.read_csv('storage/jobs.csv')
        jobs_db_user = jobs_db[jobs_db['user_id'] == state['account_session']['user_id']]
        jobs_db_user = jobs_db_user.rename(columns={
            'job_id': 'Job Id',
            'title': 'Judul Lowongan',
            'theme': 'Tema',
            'tipe_budget': 'Tipe Budget',
            'budget': 'Budget',
            'location': 'Lokasi',
            'date_needed': 'Tanggal Dibutuhkan',
            'time': 'Waktu',
            'status': 'Status'
        })
        
        headerTemplate("Lowongan Saya", state, profile=True)
        print(jobs_db_user[['Job Id','Judul Lowongan', 'Tema', 'Lokasi', 'Tanggal Dibutuhkan', 'Waktu', 'Budget', 'Tipe Budget', 'Status']].to_string(index=False))
        print("--------------------------------")
        print("[K] Kembali    [X] Keluar dari program     [S] logout.")
        footerTemplate()
        aksi = input("Masukan Job Id untuk melihat Detail atau Aksi: ")
        
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  @{state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(int(aksi) in jobs_db_user['Job Id'].values):
            job_id = int(aksi)
            job_to_edit = jobs_db_user[jobs_db_user['Job Id'] == job_id].iloc[0]
            # print(f"Anda memilih lowongan dengan ID {job_id} dan judul '{job_to_edit['title']}' untuk diedit.")
            listJobsFinder(state, job_id)            

def myOrders(state):
    while True:
        # orders_db = pd.read_csv('storage/catalogApplications.csv')
        # orders_db_user = orders_db[orders_db['user_id'] == state['account_session']['user_id']]
        merge_db = mergeCSV('storage/catalogApplications.csv', 'storage/catalog.csv', 'catalog_id', 'catalog_id')
        merge_db = merge_db.rename(columns={
            'applications_id': 'Id Pesanan',
            'title': 'Judul Catalog',
            'message': 'Pesan',
            'location': 'Lokasi',
            'date': 'Tanggal',
            'time': 'Waktu',
            'negotiated_budget': 'Budget Diajukan',
            'status_left': 'Status'
        })
        headerTemplate("Pesanan Saya", state, profile=True)
        print(merge_db[['Id Pesanan','Judul Catalog', 'Pesan', 'Lokasi', 'Tanggal', 'Waktu', 'Budget Diajukan', 'Status']].to_string(index=False))
        print("--------------------------------")
        print("[K] Kembali    [X] Keluar dari program     [S] logout.")
        footerTemplate()
        aksi = input("Masukan order id untuk melihat detail atau aksi: ")
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  @{state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(int(aksi) in merge_db['Id Pesanan'].values):
            applications_id = int(aksi)
            listOrderApplications(state, applications_id)
        