import pandas as pd

from utility import cardTemplate
from jobApplications import listJobsApplications, listJobsFinder
from catalogApplications import listCatalogApplications, listOrderApplications


def myCatalog(state):
    while True:
        catalog_db = pd.read_csv('storage/catalog.csv')
        
        catalog_db_user = catalog_db[catalog_db['user_id'] == state['account_session']['user_id']]
        print("="*44 + " Catalog Saya " + "="*44)
        print(catalog_db_user[['catalog_id','title', 'theme', 'budget', 'status']].to_string(index=False))
        print("="*102)
        print("Aksi: \n[k] Kembali \n[x] Keluar dari program \n[s] logout.")
        aksi = input("Masukan catalog id untuk mengedit atau aksi: ")
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  @{state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(int(aksi) in catalog_db_user['catalog_id'].values):
            catalog_id = int(aksi)
            catalog_to_edit = catalog_db_user[catalog_db_user['catalog_id'] == catalog_id].iloc[0]
            print(f"Anda memilih catalog dengan ID {catalog_id} dan judul '{catalog_to_edit['title']}' untuk diedit.")
            listCatalogApplications(catalog_id)


def myApplications(state):
    while True:
        applications_db = pd.read_csv('storage/jobsApplications.csv')
        
        applications_db_user = applications_db[applications_db['user_id'] == state['account_session']['user_id']]
        print("="*44 + " Lamaran Saya " + "="*44)
        print(applications_db_user[['applications_id','job_id', 'negotiated_budget', 'status']].to_string(index=False))
        print("="*102)
        print("Aksi: \n[k] Kembali \n[x] Keluar dari program \n[s] logout.")
        aksi = input("Masukan application id untuk melihat atau aksi: ")
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  @{state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(int(aksi) in applications_db_user['applications_id'].values):
            application_id = int(aksi)
            listJobsApplications(application_id)
            

def myJobs(state):
    while True:
        jobs_db = pd.read_csv('storage/jobs.csv')
        
        jobs_db_user = jobs_db[jobs_db['user_id'] == state['account_session']['user_id']]
        print("="*44 + " Lowongan Saya " + "="*44)
        print(jobs_db_user[['job_id','title', 'theme', 'budget', 'status']].to_string(index=False))
        print("="*102)
        print("Aksi: \n[k] Kembali \n[x] Keluar dari program \n[s] logout.")
        aksi = input("Masukan job id untuk mengedit atau aksi: ")
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun  @{state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(int(aksi) in jobs_db_user['job_id'].values):
            job_id = int(aksi)
            job_to_edit = jobs_db_user[jobs_db_user['job_id'] == job_id].iloc[0]
            print(f"Anda memilih lowongan dengan ID {job_id} dan judul '{job_to_edit['title']}' untuk diedit.")
            listJobsFinder(state, job_id)            

def myOrders(state):
    while True:
        orders_db = pd.read_csv('storage/catalogApplications.csv')
        
        orders_db_user = orders_db[orders_db['user_id'] == state['account_session']['user_id']]
        print("="*44 + " Pesanan Saya " + "="*44)
        print(orders_db_user[['applications_id','catalog_id', 'message', 'location', 'date', 'time', 'negotiated_budget', 'status']].to_string(index=False))
        print("="*102)
        print("Aksi: \n[k] Kembali \n[x] Keluar dari program \n[s] logout.")
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
        elif(int(aksi) in orders_db_user['applications_id'].values):
            applications_id = int(aksi)
            listOrderApplications(applications_id)
        