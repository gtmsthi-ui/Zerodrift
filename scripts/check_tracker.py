import sqlite3

c = sqlite3.connect("my_account/linkedin_tracker.db")
tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]
print("Tables:", tables)
for t in tables:
    print("\n--- Table:", t)
    cols = [col[1] for col in c.execute(f"PRAGMA table_info({t})")]
    print("Cols:", cols)
    for row in c.execute(f"SELECT * FROM {t} LIMIT 5"):
        print("Row:", row)

