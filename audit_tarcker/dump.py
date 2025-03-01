import sqlite3
from audit_tarcker.config import AuditTrack

conn = sqlite3.connect(AuditTrack)
with open("dump.sql", "w") as f:
    for line in conn.iterdump():
        f.write(f"{line}\n")
conn.close()

print("✅ SQLite database dumped to dump.sql")
