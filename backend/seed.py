from app.database import SessionLocal
from app.models import Region, District

def seed_data():
    db = SessionLocal()
    
    # 1. Avval bazada viloyatlar bor-yo'qligini tekshiramiz (ikki marta qo'shilib ketmasligi uchun)
    if db.query(Region).first():
        print("--- Viloyatlar allaqachon bazada mavjud. ---")
        db.close()
        return

    print("--- Viloyatlarni qo'shish boshlandi... ---")
    
    # 2. O'zbekiston viloyatlari ro'yxati
    uzb_regions = [
        "Andijon viloyati", "Buxoro viloyati", "Farg'ona viloyati", 
        "Jizzax viloyati", "Xorazm viloyati", "Namangan viloyati", 
        "Navoiy viloyati", "Qashqadaryo viloyati", "Qoraqalpog'iston Respublikasi", 
        "Samarqand viloyati", "Sirdaryo viloyati", "Surxondaryo viloyati", 
        "Toshkent viloyati", "Toshkent shahri"
    ]
    
    # 3. Viloyatlarni bazaga yozish
    for r_name in uzb_regions:
        region = Region(name=r_name)
        db.add(region)
        db.commit() # ID olish uchun har safar commit qilamiz
        db.refresh(region)
        
        # Namuna uchun har bir viloyatga bittadan tuman qo'shib ketamiz
        sample_district = District(name=f"{r_name} markazi", region_id=region.id)
        db.add(sample_district)
    
    db.commit()
    print("--- Barcha viloyat va namunaviy tumanlar muvaffaqiyatli qo'shildi! ---")
    db.close()

if __name__ == "__main__":
    seed_data()