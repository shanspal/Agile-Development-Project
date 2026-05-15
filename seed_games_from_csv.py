#!/usr/bin/env python3
"""
Seed the Rate My Game SQLite database from a CSV file.

Expected CSV columns:
name,company,gameplay,difficulty,tags

Example tags format:
Open World|Action|RPG

Run from the project root:
    python3 seed_games_from_csv.py

Optional:
    python3 seed_games_from_csv.py --csv games_seed_100.csv --db instance/database.db
"""

import argparse
import csv
import sqlite3
from pathlib import Path


ALLOWED_TAGS = {
    "Action",
    "RPG",
    "Multiplayer",
    "Singleplayer",
    "Story-Rich",
    "Casual",
    "Competitive",
    "Puzzle",
    "Horror",
    "Open World",
    "Indie",
    "Strategy",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Insert seed game data into database.db.")
    parser.add_argument(
        "--csv",
        default="games_seed_100.csv",
        help="Path to the CSV file. Default: games_seed_100.csv",
    )
    parser.add_argument(
        "--db",
        default="instance/database.db",
        help="Path to the SQLite database. Default: instance/database.db",
    )
    parser.add_argument(
        "--append-ratings",
        action="store_true",
        help=(
            "Append a new rating instead of replacing existing ratings/tags "
            "for games with the same name."
        ),
    )
    return parser.parse_args()


def normalize_tag(tag):
    return tag.strip()


def validate_score(value, field_name, row_number):
    try:
        score = float(value)
    except ValueError as exc:
        raise ValueError(f"Row {row_number}: {field_name} must be a number.") from exc

    if score < 0 or score > 5:
        raise ValueError(f"Row {row_number}: {field_name} must be between 0 and 5.")

    # Keep one decimal place because the project rating scale uses 0.1 steps.
    return round(score, 1)


def get_existing_game_id(cursor, name):
    cursor.execute(
        "SELECT id FROM games WHERE LOWER(name) = LOWER(?) ORDER BY id LIMIT 1",
        (name,),
    )
    result = cursor.fetchone()
    return result[0] if result else None


def insert_or_update_game(cursor, name, company):
    game_id = get_existing_game_id(cursor, name)

    if game_id is None:
        cursor.execute(
            "INSERT INTO games (name, company) VALUES (?, ?)",
            (name, company),
        )
        return cursor.lastrowid, "inserted"

    cursor.execute(
        "UPDATE games SET company = ? WHERE id = ?",
        (company, game_id),
    )
    return game_id, "updated"


def replace_seed_data(cursor, game_id):
    cursor.execute("DELETE FROM ratings WHERE game_id = ?", (game_id,))
    cursor.execute("DELETE FROM game_tags WHERE game_id = ?", (game_id,))


def insert_rating(cursor, game_id, gameplay, difficulty):
    cursor.execute(
        """
        INSERT INTO ratings (game_id, gameplay, difficulty, created_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """,
        (game_id, gameplay, difficulty),
    )


def insert_tags(cursor, game_id, tags):
    for tag in tags:
        cursor.execute(
            """
            INSERT INTO game_tags (game_id, tag_name, count)
            VALUES (?, ?, ?)
            """,
            (game_id, tag, 1),
        )


def main():
    args = parse_args()

    csv_path = Path(args.csv)
    db_path = Path(args.db)

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    inserted_games = 0
    updated_games = 0
    total_rows = 0

    conn = sqlite3.connect(db_path)

    try:
        cursor = conn.cursor()

        with csv_path.open(newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            required_columns = {"name", "company", "gameplay", "difficulty", "tags"}
            missing_columns = required_columns - set(reader.fieldnames or [])
            if missing_columns:
                raise ValueError(f"CSV is missing columns: {sorted(missing_columns)}")

            for row_number, row in enumerate(reader, start=2):
                total_rows += 1

                name = row["name"].strip()
                company = row["company"].strip()
                gameplay = validate_score(row["gameplay"], "gameplay", row_number)
                difficulty = validate_score(row["difficulty"], "difficulty", row_number)

                if not name:
                    raise ValueError(f"Row {row_number}: name cannot be empty.")
                if not company:
                    raise ValueError(f"Row {row_number}: company cannot be empty.")

                tags = [
                    normalize_tag(tag)
                    for tag in row["tags"].split("|")
                    if normalize_tag(tag)
                ]

                if not tags:
                    raise ValueError(f"Row {row_number}: at least one tag is required.")

                invalid_tags = [tag for tag in tags if tag not in ALLOWED_TAGS]
                if invalid_tags:
                    raise ValueError(
                        f"Row {row_number}: invalid tag(s): {invalid_tags}. "
                        f"Allowed tags are: {sorted(ALLOWED_TAGS)}"
                    )

                game_id, status = insert_or_update_game(cursor, name, company)

                if status == "inserted":
                    inserted_games += 1
                else:
                    updated_games += 1

                if not args.append_ratings:
                    replace_seed_data(cursor, game_id)

                insert_rating(cursor, game_id, gameplay, difficulty)
                insert_tags(cursor, game_id, tags)

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    print("Seed import completed.")
    print(f"Rows read: {total_rows}")
    print(f"Games inserted: {inserted_games}")
    print(f"Games updated: {updated_games}")
    if args.append_ratings:
        print("Mode: appended ratings/tags")
    else:
        print("Mode: replaced existing ratings/tags for matching game names")


if __name__ == "__main__":
    main()
