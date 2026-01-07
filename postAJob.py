import pandas as pd

from utility import autoIncrementNumber, cardTemplate, validasiTanggal, validasiWaktu, askInput, selectTheme

jobs_db = pd.read_csv('storage/jobs.csv')

def form_post_job(state):
    print("\n" + "="*44 + " Form Postingan Lowongan " + "="*44)
    print("Ketik 'batal' pada input apapun untuk membatalkan pembuatan lowongan.\n")
    judul = askInput("Masukkan Judul Lowongan: ", True)
    if (judul):
        deskripsi = askInput("Masukkan Deskripsi Lowongan: ", True)
        if (deskripsi):
            lokasi = askInput("Masukkan Lokasi Lowongan: ", True)
            if (lokasi):
                tema = selectTheme()
                if tema is None:
                    return
                if (tema):
                    while True:
                        tanggal = askInput("Masukkan Tanggal Lowongan (DD-MM-YYYY): ", True)
                        if (tanggal is None):
                            return
                        if validasiTanggal(tanggal):
                            break
                        print("Format tanggal salah! Gunakan DD-MM-YYYY")

                    while True:
                        waktu = askInput("Masukkan Waktu Lowongan (HH:MM): ", True)
                        if (waktu is None):
                            return  
                        if validasiWaktu(waktu):
                            break
                        print("Format waktu salah! Gunakan HH:MM")

                    while True:
                        print("Tipe Budget:\n[1] Per Jam\n[2] Per Proyek")
                        tipe_budget_pilihan = askInput("Pilih Tipe Budget Katalog: ", True)
                        if (tipe_budget_pilihan is None):
                            return
                        if (tipe_budget_pilihan == '1'):
                            tipe_budget = 'jam'
                            per_jam = askInput("Masukkan Besaran Budget Per Jam: ", True)
                            if (per_jam is None):
                                return
                            budget = per_jam
                            break
                        elif (tipe_budget_pilihan == '2'):
                            tipe_budget = 'proyek'
                            per_proyek = askInput("Masukkan Besaran Budget Per Proyek: ", True)
                            if (per_proyek is None):
                                return
                            budget = per_proyek
                            break
                        else:
                            print("Masukkan Tipe Budget yang Valid! (1 atau 2)")

                    jobs_data = {
                        "job_id": autoIncrementNumber(jobs_db),
                        "user_id": state['account_session']['user_id'] or "",
                        "title": judul,
                        "description": deskripsi,
                        "theme": ' '.join(tema) if tema else "",
                        "tipe_budget": tipe_budget,
                        "budget": budget,
                        "location": lokasi,
                        "date_needed": tanggal,
                        "time": waktu,
                        "status": "available",
                    }
                        
                    post_job_df = pd.DataFrame([jobs_data])
                    post_job_df.to_csv('storage/jobs.csv', mode='a', header=False, index=False)

                    cardTemplate("Berhasil", "Lowongan berhasil diunggah!")

# form_post_job()