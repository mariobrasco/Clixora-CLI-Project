# DATA RESTORAN
postingan = [
    {"nama": "Warung Nasi Padang", "kategori": "Indonesian", "budget": 25000, "rating": 4.8, "jarak": 0.8},
    {"nama": "Sushi Tei Express", "kategori": "Japanese", "budget": 50000, "rating": 4.6, "jarak": 1.2},
    {"nama": "Starbucks Coffee", "kategori": "Coffee", "budget": 40000, "rating": 4.7, "jarak": 0.5},
    {"nama": "Burger Queen", "kategori": "Burger", "budget": 30000, "rating": 4.3, "jarak": 1.8}
]

hasil = []

# MENU FILTER (SAMA KONSEP)
print("=== FILTER FOODFAST ===")
print("1. Filter berdasarkan Kategori")
print("2. Filter berdasarkan Budget")
print("3. Filter berdasarkan Rating")
print("4. Filter berdasarkan Jarak")

pilihan = input("Pilih salah satu filter (1-4): ")

# FILTER KATEGORI
if pilihan == "1":
    kategori_list = ["Indonesian", "Japanese", "Coffee", "Burger"]

    print("\nPilih Kategori:")
    for i in range(len(kategori_list)):
        print(f"{i+1}. {kategori_list[i]}")

    pilih_kategori = int(input("Masukkan pilihan: "))
    kategori = kategori_list[pilih_kategori - 1]

    for r in postingan:
        if r["kategori"] == kategori:
            hasil.append(r)

# FILTER BUDGET
elif pilihan == "2":
    print("\nPilih Budget:")
    print("1. <= 25.000")
    print("2. <= 30.000")
    print("3. <= 50.000")

    pilih_budget = input("Masukkan pilihan: ")

    if pilih_budget == "1":
        max_budget = 25000
    elif pilih_budget == "2":
        max_budget = 30000
    else:
        max_budget = 50000

    for r in postingan:
        if r["budget"] <= max_budget:
            hasil.append(r)

# FILTER RATING
elif pilihan == "3":
    print("\nPilih Rating:")
    print("1. >= 4.0")
    print("2. >= 4.5")
    print("3. >= 4.8")

    pilih_rating = input("Masukkan pilihan: ")

    if pilih_rating == "1":
        min_rating = 4.0
    elif pilih_rating == "2":
        min_rating = 4.5
    else:
        min_rating = 4.8

    for r in postingan:
        if r["rating"] >= min_rating:
            hasil.append(r)

# FILTER JARAK
elif pilihan == "4":
    print("\nPilih Jarak:")
    print("1. <= 1 KM")
    print("2. <= 2 KM")

    pilih_jarak = input("Masukkan pilihan: ")

    if pilih_jarak == "1":
        max_jarak = 1
    else:
        max_jarak = 2

    for r in postingan:
        if r["jarak"] <= max_jarak:
            hasil.append(r)

# OUTPUT (SAMA)
print("\n Hasil Filter:")
if not hasil:
    print("Tidak ada Foodfast yang sesuai.")
else:
    for r in hasil:
        print(f"- {r['nama']} | {r['kategori']} | ⭐ {r['rating']} | {r['jarak']} KM")
