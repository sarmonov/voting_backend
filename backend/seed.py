import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.database import SessionLocal
from app.db.init_db import init_db
from app.models.region import Region, District
from app.models.candidate import Candidate

UZB_REGIONS = [
    "Andijon viloyati", "Buxoro viloyati", "Fargona viloyati",
    "Jizzax viloyati", "Xorazm viloyati", "Namangan viloyati",
    "Navoiy viloyati", "Qashqadaryo viloyati", "Qoraqalpogiston Respublikasi",
    "Samarqand viloyati", "Sirdaryo viloyati", "Surxondaryo viloyati",
    "Toshkent viloyati", "Toshkent shahri",
]

SAMPLE_CANDIDATES = [
    {"name": "Shavkat Mirziyoyev", "party": "Liberal-Demokratik Partiya", "bio": "Prezident"},
    {"name": "Nozim Nomzod", "party": "Milliy Tiklanish Demokratik Partiyasi", "bio": "Namuna nomzod"},
]

def seed_regions(db):
    if db.query(Region).first():
        print("-- Viloyatlar allaqachon mavjud.")
        return
    for r_name in UZB_REGIONS:
        region = Region(name=r_name)
        db.add(region)
        db.commit()
        db.refresh(region)
        db.add(District(name=f"{r_name} markazi", region_id=region.id))
    db.commit()
    print(f"   {len(UZB_REGIONS)} ta viloyat qoshildi.")

def seed_candidates(db):
    if db.query(Candidate).first():
        print("-- Nomzodlar allaqachon mavjud.")
        return
    for c in SAMPLE_CANDIDATES:
        db.add(Candidate(**c))
    db.commit()
    print(f"   {len(SAMPLE_CANDIDATES)} ta nomzod qoshildi.")

def main():
    init_db()
    db = SessionLocal()
    try:
        seed_regions(db)
        seed_candidates(db)
        print("Seed muvaffaqiyatli yakunlandi!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
