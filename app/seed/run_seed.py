import os, json, csv, time
import psycopg2

OUT_DIR = os.getenv("SEED_OUTPUT_DIR", "/seed_output")

def wait_for_db_and_table(dsn: str, attempts=60, delay=2):
    for _ in range(attempts):
        try:
            conn = psycopg2.connect(dsn)
            conn.autocommit = True
            cur = conn.cursor()

            # sprawdź czy tabela users istnieje
            cur.execute("SELECT to_regclass('public.users');")
            exists = cur.fetchone()[0] is not None

            cur.close()
            conn.close()

            if exists:
                return

        except Exception:
            pass

        time.sleep(delay)

    raise RuntimeError("DB reachable, but users table not found")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    host = os.getenv("POSTGRES_HOST", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    user = os.getenv("POSTGRES_USER", "app")
    password = os.getenv("POSTGRES_PASSWORD", "app")
    dbname = os.getenv("POSTGRES_DB", "appdb")
    dsn = f"host={host} port={port} dbname={dbname} user={user} password={password}"

    wait_for_db_and_table(dsn)

    emails = [f"user{i}@example.com" for i in range(1, 6)]

    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    cur = conn.cursor()

    for e in emails:
        cur.execute("INSERT INTO users(email, created_at) VALUES (%s, NOW()) ON CONFLICT DO NOTHING;", (e,))

    with open(os.path.join(OUT_DIR, "seed.log"), "w", encoding="utf-8") as f:
        f.write("Seed completed\n")
        f.write("\n".join(emails))

    with open(os.path.join(OUT_DIR, "users.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["email"])
        for e in emails:
            w.writerow([e])

    with open(os.path.join(OUT_DIR, "data.json"), "w", encoding="utf-8") as f:
        json.dump({"seeded_users": emails}, f, indent=2)

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
