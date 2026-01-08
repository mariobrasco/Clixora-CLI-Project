import pandas as pd

from utility import cardTemplate, headerTemplate, footerTemplate, mergeCSV, updateRowById, selectTheme, deleteRowById, deleteInstant
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
            'status': 'Status',
            'sold_count': 'Terjual'
        })
        
        headerTemplate("Katalog Saya", state, profile=True)
        print("Jumlah Catalog Anda: ", len(catalog_db_user), "|", "Jumlah Catalog Terjual: ", catalog_db_user['Terjual'].sum())
        if catalog_db_user.empty:
            print("⚠️  Anda belum memiliki katalog.")
        else:
            print(catalog_db_user[['Catalog Id','Judul Catalog', 'Tema', 'Budget', 'Status', 'Terjual']].to_string(index=False))
        print("--------------------------------")
        print("[K] Kembali    [X] Keluar dari program     [L] logout")
        footerTemplate()
        
        aksi = input("Masukan Catalog Id untuk melihat Detail atau Aksi: ")
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "l"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun {state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif aksi.isdigit() and int(aksi) in catalog_db_user['Catalog Id'].values:
            catalog_id = int(aksi)

            catalog_detail = catalog_db[catalog_db['catalog_id'] == catalog_id].iloc[0]

            while True:
                headerTemplate("Detail Catalog", state, profile=True)

                print(f"Catalog ID : {catalog_detail['catalog_id']}")
                print(f"Judul      : {catalog_detail['title']}")
                print(f"Description: {catalog_detail['description']}")
                print(f"Tema       : {catalog_detail['theme']}")
                print(f"Tipe Budget: {catalog_detail['tipe_budget']}")
                print(f"Budget     : {catalog_detail['budget']}")
                print(f"Status     : {catalog_detail['status']}")
                print("--------------------------------")
                print("[1] Lihat Tawaran      [2] Edit Catalog     [3] Hapus Catalog")
                print("[K] Kembali")
                footerTemplate()

                aksi_detail = input("Pilih Aksi: ").lower()

                if aksi_detail == '1':
                    listCatalogApplications(state, catalog_id)

                elif aksi_detail == '2':
                    headerTemplate("Edit Catalog", state, profile=True)
                    print("Kosongkan input jika tidak ingin mengubah kolom tersebut.")
                    new_title = input(f"Judul Catalog ({catalog_detail['title']}): ")
                    new_description = input(f"Deskripsi ({catalog_detail['description']}): ")
                    new_theme = selectTheme(catalog_detail['theme'].split())
                    print("Tipe Budget:")
                    print("[1] Per Jam\n[2] Per Proyek")
                    new_tipe_budget = input(f"Tipe Budget ({catalog_detail['tipe_budget']}): ")  
                    new_budget = input(f"Budget ({catalog_detail['budget']}): ")
                    new_status = input(f"Status ({catalog_detail['status']}): ")
                    
                    if new_title:
                        catalog_detail['title'] = new_title
                    if new_description:
                        catalog_detail['description'] = new_description
                    if new_theme:
                        catalog_detail['theme'] = " ".join(new_theme)
                    if new_budget:
                        catalog_detail['budget'] = int(new_budget)
                    if new_status:
                        catalog_detail['status'] = new_status
                    if new_tipe_budget:
                        catalog_detail['tipe_budget'] = 'jam' if new_tipe_budget == '1' else 'proyek'
                        
                    updateRowById(
                        'storage/catalog.csv',
                        'catalog_id',
                        catalog_id,
                        {'title': catalog_detail['title'], 
                         'description': catalog_detail['description'], 
                         'theme': catalog_detail['theme'], 
                         'budget': catalog_detail['budget'], 
                         'status': catalog_detail['status'], 
                         'tipe_budget': catalog_detail['tipe_budget']},
                    )
                    break  

                elif aksi_detail == '3':
                    if (deleteRowById(
                        'storage/catalog.csv',
                        'catalog_id',
                        catalog_id,
                        "Menghapus catalog akan menghapus semua data tawaran yang terkait!"
                    )):
                        deleteInstant(
                            'storage/catalogApplications.csv',
                            'catalog_id',
                            catalog_id
                        )
                    break

                elif aksi_detail == 'k':
                    break
                else:
                    cardTemplate("Peringatan!", "Pilihan tidak valid.")

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
        if merged_db.empty:
            print("⚠️  Anda belum memiliki lamaran.")
        else:
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
            'title': 'Judul',
            'theme': 'Tema',
            'tipe_budget': 'Tipe Budget',
            'budget': 'Budget',
            'location': 'Lokasi',
            'date_needed': 'Tanggal',
            'time': 'Waktu',
            'status': 'Status'
        })
        
        headerTemplate("Lowongan Saya", state, profile=True)
        if jobs_db_user.empty:
            print("⚠️  Anda belum memiliki lowongan.")
        else:
            print(jobs_db_user[['Job Id','Judul', 'Tema', 'Lokasi', 'Tanggal', 'Waktu', 'Budget', 'Tipe Budget', 'Status']].to_string(index=False))
        print("--------------------------------")
        print("[K] Kembali    [X] Keluar dari program     [S] logout.")
        footerTemplate()
        aksi = input("Masukan Job Id untuk melihat Detail atau Aksi: ")
        
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun {state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(int(aksi) in jobs_db_user['Job Id'].values):
            job_id = int(aksi)
            job_detail = jobs_db[jobs_db['job_id'] == job_id].iloc[0]
            
            while True:
                headerTemplate("Detail Lowongan", state, profile=True)

                print(f"Job ID        : {job_detail['job_id']}")
                print(f"Judul         : {job_detail['title']}")
                print(f"Deskripsi     : {job_detail['description']}")
                print(f"Tema          : {job_detail['theme']}")
                print(f"Tipe Budget   : {job_detail['tipe_budget']}")
                print(f"Budget        : {job_detail['budget']}")
                print(f"Lokasi        : {job_detail['location']}")
                print(f"Tanggal       : {job_detail['date_needed']}")
                print(f"Waktu         : {job_detail['time']}")
                print(f"Status        : {job_detail['status']}")
                print("--------------------------------")
                print("[1] Lihat Pelamar     [2] Edit Lowongan     [3] Hapus Lowongan")
                print("[K] Kembali")
                footerTemplate()

                aksi_detail = input("Pilih Aksi: ").lower()

                if aksi_detail == '1':
                    listJobsFinder(state, job_id)

                elif aksi_detail == 'k':
                    break
                
                elif aksi_detail == '2':
                    headerTemplate("Edit Catalog", state, profile=True)
                    print("Kosongkan input jika tidak ingin mengubah kolom tersebut.")
                    
                    new_title = input(f"Judul Catalog ({job_detail['title']}): ")
                    new_description = input(f"Deskripsi ({job_detail['description']}): ")
                    new_theme = selectTheme(job_detail['theme'].split())
                    print("Tipe Budget:")
                    print("[1] Per Jam\n[2] Per Proyek")
                    new_tipe_budget = input(f"Tipe Budget ({job_detail['tipe_budget']}): ")  
                    new_budget = input(f"Budget ({job_detail['budget']}): ")
                    new_location = input(f"Lokasi ({job_detail['location']}): ")
                    new_date_needed = input(f"Tanggal Dibutuhkan ({job_detail['date_needed']}): ")
                    new_time = input(f"Waktu ({job_detail['time']}): ")
                    new_status = input(f"Status ({job_detail['status']}): ")
                    
                    if new_title:
                        job_detail['title'] = new_title
                    if new_description:
                        job_detail['description'] = new_description
                    if new_theme:
                        job_detail['theme'] = " ".join(new_theme)
                    if new_budget:
                        job_detail['budget'] = int(new_budget)
                    if new_status:
                        job_detail['status'] = new_status
                    if new_tipe_budget:
                        job_detail['tipe_budget'] = 'jam' if new_tipe_budget == '1' else 'proyek'
                    if new_location:
                        job_detail['location'] = new_location
                    if new_date_needed:
                        job_detail['date_needed'] = new_date_needed
                    if new_time:
                        job_detail['time'] = new_time
                    
                    updateRowById(
                        'storage/jobs.csv',
                        'job_id',
                        job_id,
                        {'title': job_detail['title'], 
                         'description': job_detail['description'], 
                         'theme': job_detail['theme'], 
                         'budget': job_detail['budget'], 
                         'status': job_detail['status'], 
                         'tipe_budget': job_detail['tipe_budget'], 
                         'location': job_detail['location'], 
                         'date_needed': job_detail['date_needed'], 
                         'time': job_detail['time']},
                    )
                    break  # reload list setelah edit

                elif aksi_detail == '3':
                    
                    if deleteRowById(
                        'storage/jobs.csv',
                        'job_id',
                        job_id,
                        "Menghapus lowongan akan menghapus semua data lamaran yang terkait!"
                    ):
                        deleteInstant(
                            'storage/jobsApplications.csv',
                            'job_id',
                            job_id
                        )
                    break
                else:
                    cardTemplate("Peringatan!", "Pilihan tidak valid.")
                     
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
        if merge_db.empty:
            print("⚠️  Anda belum memiliki pesanan.")
        else:
            print(merge_db[['Id Pesanan','Judul Catalog', 'Pesan', 'Lokasi', 'Tanggal', 'Waktu', 'Budget Diajukan', 'Status']].to_string(index=False))
        print("--------------------------------")
        print("[K] Kembali    [X] Keluar dari program     [S] logout.")
        footerTemplate()
        aksi = input("Masukan Id Pesanan untuk melihat detail atau aksi: ")
        if (aksi == "k"):
            return
        elif (aksi == "x"):
            exit()
        elif (aksi == "s"):
            cardTemplate("Berhasil!",f"Anda Telah Logout dari akun {state['account_session']['username']}.")
            state['account_session'] = None
            state["input_navigasi"] = None
            return
        elif(int(aksi) in merge_db['Id Pesanan'].values):
            applications_id = int(aksi)
            listOrderApplications(state, applications_id)
        