import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)


def list_books():
    resp = sb.table("books").select("*").order("book_id").execute()
    return resp.data

def search_books(field, keyword):
    resp = sb.table("books").select("*").ilike(field, f"%{keyword}%").execute()
    return resp.data

def show_member_details(member_id):
    member = sb.table("members").select("*").eq("member_id", member_id).single().execute().data
    if not member:
        return None

    borrowed = (
        sb.table("borrow_records")
        .select("record_id, borrow_date, return_date, books(title,author)")
        .eq("member_id", member_id)
        .execute()
        .data
    )
    return {"member": member, "borrowed": borrowed}


if __name__ == "__main__":
    while True:
        print("\n Library - Read Operations")
        print("1. List all books")
        print("2. Search books")
        print("3. Show member details & borrowed books")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            for b in list_books():
                print(f"{b['book_id']}: '{b['title']}' by {b['author']} | Stock: {b['stock']}")

        elif choice == "2":
            field = input("Search by (title/author/category): ").strip().lower()
            if field not in ["title", "author", "category"]:
                print("Invalid field")
                continue
            keyword = input("Enter keyword: ").strip()
            for b in search_books(field, keyword):
                print(b)

        elif choice == "3":
            mid = int(input("Enter Member ID: "))
            details = show_member_details(mid)
            if not details:
                print("Member not found")
            else:
                print("Member:", details["member"])
                print("Borrowed:")
                for r in details["borrowed"]:
                    print(r)

        elif choice == "0":
            break

        else:
            print("Invalid choice")
