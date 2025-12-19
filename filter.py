# DATA RESTORAN
postingan = [
    {"nama": "Warung Nasi Padang", "kategori": "Indonesian", "budget": 25000, "rating": 4.8, "jarak": 0.8},
    {"nama": "Sushi Tei Express", "kategori": "Japanese", "budget": 50000, "rating": 4.6, "jarak": 1.2},
    {"nama": "Starbucks Coffee", "kategori": "Coffee", "budget": 40000, "rating": 4.7, "jarak": 0.5},
    {"nama": "Burger Queen", "kategori": "Burger", "budget": 30000, "rating": 4.3, "jarak": 1.8}
]

hasil = postingan[:]  # salin data awal

print("=== FILTER RESTORAN FOODFAST ===")

# PILIH FILTER KATEGORI
pilih = input("Filter berdasarkan kategori? (y/n): ")
if pilih.lower() == "y":
    kategori = input("Masukkan kategori: ")
    hasil = [r for r in hasil if r["kategori"].lower() == kategori.lower()]

# PILIH FILTER BUDGET
pilih = input("Filter berdasarkan budget? (y/n): ")
if pilih.lower() == "y":
    max_budget = int(input("Masukkan budget maksimal: "))
    hasil = [r for r in hasil if r["budget"] <= max_budget]

# PILIH FILTER RATING
pilih = input("Filter berdasarkan rating? (y/n): ")
if pilih.lower() == "y":
    min_rating = float(input("Masukkan rating minimal: "))
    hasil = [r for r in hasil if r["rating"] >= min_rating]

# PILIH FILTER JARAK
pilih = input("Filter berdasarkan jarak? (y/n): ")
if pilih.lower() == "y":
    max_jarak = float(input("Masukkan jarak maksimal (KM): "))
    hasil = [r for r in hasil if r["jarak"] <= max_jarak]

# OUTPUT

print("\nHasil Filter:")

if not hasil:
    print("Tidak ada restoran yang sesuai.")
else:
    for r in hasil:
        print(f"- {r['nama']} | ⭐ {r['rating']} | {r['jarak']} KM | Rp {r['budget']}")
