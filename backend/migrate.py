"""
Mavjud jadvalga yangi ustunlarni qo'shadi (ALTER TABLE).
Ishga tushirish: python migrate.py  (backend/ papkasidan)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine
from sqlalchemy import text

migrations = [
    "ALTER TABLE candidates ADD COLUMN IF NOT EXISTS bio VARCHAR(1000)",
    "ALTER TABLE candidates ADD COLUMN IF NOT EXISTS photo_url VARCHAR(500)",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE",
    "ALTER TABLE users ADD COLUMN IF NOT EXISTS hashed_password VARCHAR",
]

with engine.connect() as conn:
    for sql in migrations:
        try:
            conn.execute(text(sql))
            print(f"  OK: {sql[:60]}...")
        except Exception as e:
            print(f"  SKIP ({e}): {sql[:60]}...")
    conn.commit()

print("\nMigration yakunlandi!")
