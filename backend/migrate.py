# backend/migrate.py
# Task: TASK-002 | Spec: REQ-01
# Database migration script — creates all tables in Neon PostgreSQL

from database import create_db_and_tables

if __name__ == "__main__":
    print("Running database migration...")
    create_db_and_tables()
    print("Done. Tables created: task, conversation, message")
