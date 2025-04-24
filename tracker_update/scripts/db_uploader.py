import psycopg2
import os
import re

def upload_to_postgres(tech, week_num, csv_path):
    table_suffix_pattern = re.compile(rf"{tech}_wk(\d{{4}})$")

    conn = psycopg2.connect(
        dbname="postgres", user="postgres", password="aaa", host="localhost", port="5432"
    )
    cur = conn.cursor()

    # 🔍 Step 1: Fetch all matching tables
    cur.execute("""
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public' AND tablename LIKE %s
    """, (f"{tech}_wk%",))
    table_names = [row[0] for row in cur.fetchall()]

    # 🔍 Step 2: Extract numeric week suffixes and sort
    matching_weeks = sorted([
        int(match.group(1))
        for name in table_names
        if (match := table_suffix_pattern.match(name))
        and f"{tech}_wk{week_num[-4:]}" != name  # skip current week table
    ])

    if not matching_weeks:
        raise ValueError(f"No existing base tables found for {tech}")

    latest_week = matching_weeks[-1]
    base_table = f"{tech}_wk{latest_week}"
    table_name = f"{tech}_wk{week_num[-4:]}"
    
    # 🔁 Determine correct cell column
    cell_column = {
        "lte": "cell_name",
        "nr": "nr_cell_name"
    }.get(tech.lower(), "cell_name")

    # 🧱 Create and populate the table
    cur.execute(f"CREATE TABLE {table_name} (LIKE {base_table} INCLUDING ALL);")
    cur.execute(f"ALTER TABLE {table_name} DROP COLUMN site;")

    with open(csv_path, 'r', encoding='utf-8') as f:
        cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER DELIMITER ','", f)

    cur.execute(f"ALTER TABLE {table_name} ADD COLUMN site TEXT;")
    cur.execute(f"""
        UPDATE {table_name}
        SET site = CASE
            WHEN {cell_column} ~ '[A-Z]{{3}}\d{{4}}|[A-Z]{{4}}\d{{3}}'
            THEN substring({cell_column} FROM '([A-Z]{{3}}\d{{4}}|[A-Z]{{4}}\d{{3}})')
            ELSE 'No Site Name'
        END;
    """)

    conn.commit()
    cur.close()
    conn.close()

    print(f" {table_name} created using base {base_table} and data uploaded.")
