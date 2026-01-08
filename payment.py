import pandas as pd

from utility import cardTemplate, autoIncrementCustom, updateRowById, headerTemplate, footerTemplate

def menuPayment(state, applications_info, event_info, photographer_info):
    FILE_PATH_APPLICATIONS = 'storage/jobsApplications.csv' if 'job_id' in applications_info else 'storage/catalogApplications.csv'
    PAYMENT_CSV_PATH = 'storage/payments.csv'
    payment_db = pd.read_csv(PAYMENT_CSV_PATH)

    headerTemplate("MENU PEMBAYARAN", state, profile=True)
    print("Detail Pekerjaan:")
    print(f"Title        : {event_info['title']}")
    print(f"Budget       : {applications_info['negotiated_budget']}")
    print(f"Photographer : {photographer_info['username']}\n")
    print("--------------------------------")
    print("Pilih Pembayaran:")
    print("[1] QRIS")
    print("[2] Cash")
    print("[B] Batal")
    footerTemplate()
    metode = input("Masukan pilihan: ").lower()

    if metode == 'b':
        cardTemplate("Batal!", "Pembayaran dibatalkan.")
        return

    if metode not in ['1', '2']:
        cardTemplate("Gagal", f"input '{metode}' tidak valid.")
        return

    total = int(applications_info['negotiated_budget'])
    tipe_pembayaran = "full" 

    if metode == '1':
        print("\nPilih Tipe Pembayaran:")
        print("[1] Bayar Full")
        print("[2] Bayar DP (50%)")
        print("[B] Batal")
        tipe = input("Masukan pilihan: ").lower()

        if tipe == 'b':
            cardTemplate("Batal!", "Pembayaran dibatalkan.")
            return

        if tipe == '2':
            tipe_pembayaran = "dp"
            total = total // 2
        elif tipe != '1':
            cardTemplate("Gagal", "Pilihan tipe pembayaran tidak valid.")
            return
        
        headerTemplate("PEMBAYARAN QRIS", state, profile=True)
        print("Merchant    : CLIXORA")
        print(f"Total Bayar : Rp{total}\n")

        print("""
███████████████████████
█ ▄▄▄▄▄ █▀▄▀██ ▄▄▄▄▄ ██
█ █   █ █▄▀█▄█ █   █ ██
█ █▄▄▄█ █ ▀▄▀█ █▄▄▄█ ██
█▄▄▄▄▄▄▄█▄█▄█▄▄▄▄▄▄▄▄██
█ ▀▀ ▀▄▀▄ ▄▀ ▄ ▀▀▀ ▀ ██
█ ▀▄█ ▄▀ ▀▀▄█▄ ▀ ▀█ ███
█ ▄▄▄▄▄ █ ▀ ▄▀█ ▄▄▄▄▄ █
█ █   █ █▄▀ ▀▄█ █   █ █
█ █▄▄▄█ █ ▀▄█▀▄ █▄▄▄█ █
█▄▄▄▄▄▄▄█▄█▄█▄█▄▄▄▄▄▄▄█

QRIS PAYMENT
Scan menggunakan e-wallet Anda
""".strip())
        footerTemplate()

        while True:
            konfirmasi = input("\nKetik [bayar] setelah pembayaran berhasil atau [batal] untuk membatalkan: ")

            if konfirmasi.lower() == 'bayar':
                payment_data = {
                    'payment_id': autoIncrementCustom("pm", PAYMENT_CSV_PATH, 'payment_id'), 
                    'user_id': applications_info['user_id'], 
                    'application_id': applications_info['applications_id'], 
                    'application_type': 'catalog' if 'catalog_id' in applications_info else 'job', 
                    'payment_method': 'qris',
                    'payment_type': tipe_pembayaran,
                    'payment_refs': autoIncrementCustom("ref", PAYMENT_CSV_PATH, 'payment_refs'),
                    'amount': total,
                    'status': 'paid',
                    'paid_at': pd.Timestamp.now()
                    }
                payment_df = pd.DataFrame([payment_data])
                payment_df.to_csv('storage/payments.csv', mode='a', header=False, index=False)
                
                updateRowById(
                    FILE_PATH_APPLICATIONS,
                    'applications_id',
                    applications_info['applications_id'],
                    {'status': 'on going (paid)'}
                )
                cardTemplate("Berhasil", f"Pembayaran sebesar Rp{total} telah berhasil dilakukan kepada {photographer_info['username']}.\nTerimakasih telah menggunakan layanan Clixora!")
                return
            elif konfirmasi.lower() == 'batal':
                cardTemplate("Batal!","Pembayaran dibatalkan.")
                return
            else:
                cardTemplate(f"Input '{konfirmasi}' tidak valid.")
            
    elif metode == '2':
        headerTemplate("PEMBAYARAN CASH", state, profile=True)
        print("Anda memilih metode pembayaran Cash.") 
        print(f"Silahkan lakukan pembayaran secara langsung kepada Photographer saat pekerjaan selesai\n Siapkan uang Tunai sebesar {total}!.") 
        print("Jika sudah membayar Photographer, silahkan konfirmasi pembayaran kepada Clixora.")
        footerTemplate()
        input("Ketik Enter jika sudah mengerti: ")
        payment_data = {
            'payment_id': autoIncrementCustom("pm", payment_db, 'payment_id'), 
            'user_id': applications_info['user_id'], 
            'application_id': applications_info['applications_id'], 
            'application_type': 'catalog' if 'catalog_id' in applications_info else 'job', 
            'payment_method': 'cash',
            'payment_type': tipe_pembayaran,
            'payment_refs': autoIncrementCustom("ref", payment_db, 'payment_refs'),
            'amount': total,
            'status': 'pending',
            'paid_at': ""
            }
        cardTemplate("Berhasil", f"Pembayaran sebesar Rp{total} telah tercatat sebagai 'pending'. Silahkan lakukan pembayaran secara langsung kepada Photographer saat pekerjaan selesai.")
