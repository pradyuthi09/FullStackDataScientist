import os
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)


def top_books():

    resp = sb.table("books").select("book_id, title, borrow_records(record_id)").execute()
    data = resp.data or []

    for b in data:
        b["borrow_count"] = len(b.get("borrow_records", []))


    top = sorted(data, key=lambda x: x["borrow_count"], reverse=True)[:5]
    return top

def overdue_members():
    resp = sb.table("borrow_records").select(
        "record_id, borrow_date, return_date, members(name,email), books(title)"
    ).execute()
    data = resp.data or []

    overdue = []
    now = datetime.utcnow()
    for r in data:
        if r["return_date"] is None:
            borrow_date = datetime.fromisoformat(r["borrow_date"])
            if now - borrow_date > timedelta(days=14):
                overdue.append({
                    "member_name": r["members"]["name"],
                    "member_email": r["members"]["email"],
                    "book_title": r["books"]["title"],
                    "borrow_date": r["borrow_date"]
                })
    return overdue

def member_borrow_counts():

    resp = sb.table("members").select("member_id, name, borrow_records(record_id)").execute()
    data = resp.data or []

    for m in data:
        m["total_borrowed"] = len(m.get("borrow_records", []))
    return data

if __name__ == "__main__":
    print(" Library Reports")
    print("1. Top 5 Most Borrowed Books")
    print("2. Members with Overdue Books (>14 days)")
    print("3. Total Books Borrowed per Member")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == "1":
        rows = top_books()
        print("\nTop 5 Most Borrowed Books:")
        for row in rows:
            print(f"{row['title']} — {row['borrow_count']} times")

    elif choice == "2":
        rows = overdue_members()
        print("\nOverdue Members (14+ days):")
        for row in rows:
            print(f"{row['member_name']} ({row['member_email']}) borrowed '{row['book_title']}' on {row['borrow_date']}")

    elif choice == "3":
        rows = member_borrow_counts()
        print("\nBooks Borrowed Per Member:")
        for row in rows:
            print(f"{row['name']} — {row['total_borrowed']} books")

    else:
        print("Invalid choice")
