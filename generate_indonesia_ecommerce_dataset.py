"""
================================================================
 Indonesia E-Commerce Apparel Dataset Generator
 Senior Data Engineer Script
 Target : 50.000 rows | Period : Jan 2023 – Dec 2025
================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings("ignore")

SEED = 42
np.random.seed(SEED)
random.seed(SEED)

N_ROWS        = 50_000
DIRTY_RATIO   = 0.05          # 5% dirty data
START_DATE    = datetime(2023, 1, 1)
END_DATE      = datetime(2025, 12, 31, 23, 59, 59)
OUTPUT_FILE   = "/mnt/user-data/outputs/indonesia_ecommerce_apparel_2023_2025.csv"

# ── Product catalogue ──────────────────────────────────────────
PRODUCTS = {
    "Kaos Polos":       (59_000,  149_000),
    "Kaos Grafis":      (79_000,  199_000),
    "Kemeja Casual":    (99_000,  299_000),
    "Kemeja Formal":    (149_000, 399_000),
    "Jaket Hoodie":     (149_000, 399_000),
    "Jaket Denim":      (199_000, 499_000),
    "Jaket Windbreaker":(179_000, 449_000),
    "Celana Jeans":     (149_000, 399_000),
    "Celana Chino":     (129_000, 349_000),
    "Celana Pendek":    (79_000,  199_000),
    "Rok Mini":         (89_000,  229_000),
    "Rok Midi":         (99_000,  249_000),
    "Dress Casual":     (129_000, 349_000),
    "Dress Formal":     (199_000, 499_000),
    "Cardigan":         (119_000, 299_000),
    "Sweater":          (129_000, 329_000),
    "Polo Shirt":       (99_000,  249_000),
    "Tank Top":         (49_000,  129_000),
    "Blouse":           (99_000,  279_000),
    "Outer":            (179_000, 479_000),
}
PRODUCT_NAMES  = list(PRODUCTS.keys())
PRODUCT_WEIGHTS = [
    8, 7, 9, 6, 8, 5, 4, 9, 7, 6,
    4, 4, 6, 4, 5, 6, 5, 5, 5, 3
]

# ── Cities & shipping cost logic ──────────────────────────────
# (city, province, tier)  tier 1=murah, 2=sedang, 3=mahal, 4=sangat mahal
CITIES = [
    # Jawa – tier 1-2
    ("Jakarta Selatan",  "DKI Jakarta",       1),
    ("Jakarta Utara",    "DKI Jakarta",       1),
    ("Jakarta Barat",    "DKI Jakarta",       1),
    ("Jakarta Timur",    "DKI Jakarta",       1),
    ("Jakarta Pusat",    "DKI Jakarta",       1),
    ("Bandung",          "Jawa Barat",        1),
    ("Bekasi",           "Jawa Barat",        1),
    ("Depok",            "Jawa Barat",        1),
    ("Bogor",            "Jawa Barat",        1),
    ("Tangerang",        "Banten",            1),
    ("Tangerang Selatan","Banten",            1),
    ("Surabaya",         "Jawa Timur",        1),
    ("Malang",           "Jawa Timur",        2),
    ("Semarang",         "Jawa Tengah",       1),
    ("Yogyakarta",       "DI Yogyakarta",     2),
    ("Solo",             "Jawa Tengah",       2),
    ("Medan",            "Sumatera Utara",    2),
    ("Palembang",        "Sumatera Selatan",  2),
    ("Pekanbaru",        "Riau",              2),
    ("Batam",            "Kepri",             2),
    ("Padang",           "Sumatera Barat",    2),
    ("Bandar Lampung",   "Lampung",           2),
    ("Makassar",         "Sulsel",            2),
    ("Balikpapan",       "Kaltim",            3),
    ("Samarinda",        "Kaltim",            3),
    ("Pontianak",        "Kalbar",            3),
    ("Banjarmasin",      "Kalsel",            3),
    ("Denpasar",         "Bali",              2),
    ("Mataram",          "NTB",               3),
    ("Kupang",           "NTT",               4),
    ("Manado",           "Sulut",             3),
    ("Ambon",            "Maluku",            4),
    ("Jayapura",         "Papua",             4),
    ("Sorong",           "Papua Barat",       4),
    ("Cirebon",          "Jawa Barat",        2),
    ("Tasikmalaya",      "Jawa Barat",        2),
    ("Sukabumi",         "Jawa Barat",        2),
    ("Kediri",           "Jawa Timur",        2),
    ("Jember",           "Jawa Timur",        2),
    ("Purwokerto",       "Jawa Tengah",       2),
]
CITY_NAMES    = [c[0] for c in CITIES]
CITY_TIERS    = {c[0]: c[2] for c in CITIES}
# city popularity weight (Jabodetabek & big cities dominate)
CITY_WEIGHTS  = [
    10, 6, 6, 6, 5,   # Jakarta
    8, 7, 5, 5, 7, 5, # Jawa Barat & Banten
    7, 4, 4, 4, 3,    # Jatim & Jateng
    4, 3, 3, 3, 2, 2, # Sumatera
    3, 2, 2, 2, 2,    # Sulsel & Kalimantan
    3, 2, 1,          # Bali, NTB, NTT
    2, 1, 1,          # Sulut, Maluku, Papua
    1,                # Papua Barat
    2, 2, 2, 2, 2, 2  # kota menengah
]

SHIPPING_BASE = {1: (9_000, 15_000), 2: (15_000, 25_000),
                 3: (25_000, 45_000), 4: (45_000, 75_000)}

# ── Payment methods ────────────────────────────────────────────
PAYMENT_METHODS  = ["E-Wallet", "Transfer Bank", "COD", "Kartu Kredit"]
PAYMENT_WEIGHTS  = [40, 30, 20, 10]

# ── Order status ───────────────────────────────────────────────
# base rates per payment
STATUS_RATES = {
    "E-Wallet":      {"Completed": 0.92, "Cancelled": 0.05, "Returned": 0.03},
    "Transfer Bank": {"Completed": 0.90, "Cancelled": 0.07, "Returned": 0.03},
    "COD":           {"Completed": 0.78, "Cancelled": 0.14, "Returned": 0.08},
    "Kartu Kredit":  {"Completed": 0.91, "Cancelled": 0.05, "Returned": 0.04},
}

# ── Promo / campaign dates ─────────────────────────────────────
def is_promo_day(dt: datetime) -> bool:
    md = (dt.month, dt.day)
    promo_dates = {
        (1, 1), (1, 15),                   # Tahun Baru
        (2, 2),                             # 2.2
        (3, 3),                             # 3.3
        (4, 4),                             # 4.4
        (5, 5),                             # 5.5
        (6, 6),                             # 6.6
        (7, 7),                             # 7.7
        (8, 8), (8, 17),                    # 8.8, HUT RI
        (9, 9),                             # 9.9
        (10, 10),                           # 10.10
        (11, 11),                           # 11.11 Harbolnas
        (12, 12), (12, 24), (12, 25),       # 12.12, Natal
    }
    # Payday: tanggal 25-1 bulan berikutnya
    if dt.day >= 25 or dt.day == 1:
        return True
    return md in promo_dates

def is_payday(dt: datetime) -> bool:
    return dt.day >= 25 or dt.day == 1

def promo_hour_weight(hour: int) -> float:
    """Simulasi lonjakan jam 12 siang & 20.00 malam."""
    if hour in (11, 12, 13):
        return 3.0
    if hour in (19, 20, 21):
        return 3.5
    if 0 <= hour <= 5:
        return 0.3
    return 1.0

# ── Date generator ─────────────────────────────────────────────
def generate_dates(n: int) -> list:
    total_seconds = int((END_DATE - START_DATE).total_seconds())
    # Base uniform random seconds
    raw_seconds = np.random.randint(0, total_seconds, size=n * 3)
    raw_dates   = [START_DATE + timedelta(seconds=int(s)) for s in raw_seconds]

    # Apply hour-weight sampling (rejection-like)
    selected = []
    for dt in raw_dates:
        w = promo_hour_weight(dt.hour)
        if random.random() < w / 3.5:
            selected.append(dt)
        if len(selected) == n:
            break

    # Fill remaining with direct random if needed
    while len(selected) < n:
        s  = random.randint(0, total_seconds)
        dt = START_DATE + timedelta(seconds=s)
        selected.append(dt)

    return selected

# ══════════════════════════════════════════════════════════════
#  MAIN GENERATION
# ══════════════════════════════════════════════════════════════
print("⏳ Generating dates …")
dates = generate_dates(N_ROWS)
dates.sort()   # kronologis

print("⏳ Building columns …")

# Order_ID
order_ids = [f"ORD-{d.year}-{str(i+1).zfill(5)}" for i, d in enumerate(dates)]

# Product & price
products   = random.choices(PRODUCT_NAMES, weights=PRODUCT_WEIGHTS, k=N_ROWS)
unit_prices = [
    round(random.randint(*PRODUCTS[p]) / 1000) * 1000
    for p in products
]

# Quantity
quantities = np.random.choice([1, 2, 3, 4, 5],
                               p=[0.40, 0.30, 0.15, 0.10, 0.05],
                               size=N_ROWS)

# City
cities     = random.choices(CITY_NAMES, weights=CITY_WEIGHTS, k=N_ROWS)
city_tiers = [CITY_TIERS[c] for c in cities]

# Shipping cost
shipping_costs = [
    round(random.randint(*SHIPPING_BASE[t]) / 500) * 500
    for t in city_tiers
]

# Payment method
payments = random.choices(PAYMENT_METHODS, weights=PAYMENT_WEIGHTS, k=N_ROWS)

# Discount
discounts = []
for i, dt in enumerate(dates):
    price = unit_prices[i]
    qty   = quantities[i]
    gross = price * qty
    if is_promo_day(dt) and (dt.month, dt.day) in {(11, 11), (12, 12)}:
        rate = random.uniform(0.20, 0.50)   # Harbolnas besar
    elif is_promo_day(dt):
        rate = random.uniform(0.10, 0.30)
    elif is_payday(dt):
        rate = random.uniform(0.05, 0.20)
    else:
        rate = random.choices([0, random.uniform(0.05, 0.15)],
                               weights=[0.55, 0.45])[0]
    discounts.append(round(gross * rate / 1000) * 1000)

# Order status
statuses = []
for pay in payments:
    rates  = STATUS_RATES[pay]
    status = random.choices(list(rates.keys()),
                            weights=list(rates.values()))[0]
    statuses.append(status)

# ── Assemble clean DataFrame ───────────────────────────────────
df = pd.DataFrame({
    "Order_ID":         order_ids,
    "Transaction_Date": [d.strftime("%Y-%m-%d %H:%M:%S") for d in dates],
    "Product_Category": products,
    "Unit_Price":       unit_prices,
    "Quantity":         quantities,
    "Discount_Amount":  discounts,
    "Shipping_City":    cities,
    "Payment_Method":   payments,
    "Shipping_Cost":    shipping_costs,
    "Order_Status":     statuses,
})

# ══════════════════════════════════════════════════════════════
#  INJECT DIRTY DATA  (~5%)
# ══════════════════════════════════════════════════════════════
print("⏳ Injecting dirty data …")

n_dirty = int(N_ROWS * DIRTY_RATIO)
dirty_idx = np.random.choice(N_ROWS, size=n_dirty, replace=False)

# Split dirty pool into 4 buckets
np.random.shuffle(dirty_idx)
b1 = dirty_idx[:500]           # Negative Unit_Price
b2 = dirty_idx[500:1000]       # Typo Shipping_City
b3 = dirty_idx[1000:1500]      # NaN Discount_Amount
b4 = dirty_idx[1500:2000]      # NaN Payment_Method
b5 = dirty_idx[2000:2100]      # Duplicate Order_ID
b6 = dirty_idx[2100:2200]      # Unit_Price = 0
b7 = dirty_idx[2200:2300]      # Quantity = 0 or negative
b8 = dirty_idx[2300:2500]      # Shipping_Cost outlier (sangat murah/mahal)

# b1 – Negative Unit_Price
df.loc[b1, "Unit_Price"] = df.loc[b1, "Unit_Price"] * -1

# b2 – Typo cities
typo_map = {
    "Jakarta Selatan":  ["Jakrata Selatan",  "Jakarta Selatan "],
    "Jakarta Utara":    ["Jakarta Utraa",    "JakartaUtara"],
    "Bandung":          ["Bandun",           "Badung"],
    "Surabaya":         ["Surabay",          "Surabaya "],
    "Medan":            ["Medaan",           "Medan "],
    "Makassar":         ["Makasaar",         "Makasar"],
    "Denpasar":         ["Denpasaar",        "Denpasar "],
    "Yogyakarta":       ["Jogyakarta",       "Yogjakarta"],
    "Semarang":         ["Semrang",          "Semerang"],
    "Balikpapan":       ["Balikppan",        "Balikapapan"],
}
for idx in b2:
    city = df.at[idx, "Shipping_City"]
    if city in typo_map:
        df.at[idx, "Shipping_City"] = random.choice(typo_map[city])
    else:
        # generic typo: tambah spasi di akhir atau dobel huruf
        df.at[idx, "Shipping_City"] = city + " "

# b3 – NaN Discount_Amount
df.loc[b3, "Discount_Amount"] = np.nan

# b4 – NaN Payment_Method
df.loc[b4, "Payment_Method"] = np.nan

# b5 – Duplicate Order_ID (ambil ID dari baris lain)
for idx in b5:
    ref = random.choice([i for i in range(N_ROWS) if i != idx])
    df.at[idx, "Order_ID"] = df.at[ref, "Order_ID"]

# b6 – Unit_Price = 0
df.loc[b6, "Unit_Price"] = 0

# b7 – Quantity = 0 atau -1
df.loc[b7, "Quantity"] = np.random.choice([0, -1], size=len(b7))

# b8 – Shipping_Cost outlier
df.loc[b8[:100], "Shipping_Cost"] = 0          # gratis total (mencurigakan)
df.loc[b8[100:], "Shipping_Cost"] = np.random.randint(200_000, 500_000,
                                                        size=len(b8[100:]))

# ── Save ───────────────────────────────────────────────────────
print(f"⏳ Saving to {OUTPUT_FILE} …")
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

# ── Summary report ─────────────────────────────────────────────
print("\n" + "="*60)
print("  DATASET GENERATION COMPLETE")
print("="*60)
print(f"  Total rows          : {len(df):,}")
print(f"  Date range          : {df['Transaction_Date'].min()}  →  {df['Transaction_Date'].max()}")
print(f"  Unique products     : {df['Product_Category'].nunique()}")
print(f"  Unique cities       : {df['Shipping_City'].nunique()}")
print(f"  Payment methods     : {df['Payment_Method'].value_counts().to_dict()}")
print(f"  Order status dist.  : {df['Order_Status'].value_counts().to_dict()}")
print(f"\n  --- Dirty Data Injected ---")
print(f"  Negative Unit_Price : {(df['Unit_Price'] < 0).sum()}")
print(f"  Zero Unit_Price     : {(df['Unit_Price'] == 0).sum()}")
print(f"  Zero/Neg Quantity   : {(df['Quantity'] <= 0).sum()}")
print(f"  Typo cities         : ~{len(b2)}")
print(f"  NaN Discount_Amount : {df['Discount_Amount'].isna().sum()}")
print(f"  NaN Payment_Method  : {df['Payment_Method'].isna().sum()}")
print(f"  Duplicate Order_ID  : ~{len(b5)}")
print(f"  Shipping outliers   : ~{len(b8)}")
print("="*60)
print(f"\n✅ File saved → {OUTPUT_FILE}")
