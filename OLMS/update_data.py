import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def update_book_stock(book_id, added_stock):

    resp = sb.table("books").select("stock").eq("book_id", book_id).execute()
    if not resp.data:
        return { " Book not found."}

    current_stock = resp.data[0]["stock"]
    new_stock = current_stock + added_stock
    
    update_resp = sb.table("books").update({"stock": new_stock}).eq("book_id", book_id).execute()
    return {"success": f" Stock updated to {new_stock}", "data": update_resp.data}



def update_member(member_id, new_name=None, new_email=None):
    payload = {}
    if new_name:
        payload["name"] = new_name
    if new_email:
        payload["email"] = new_email

    if not payload:
        return { " No update fields provided."}

    resp = sb.table("members").update(payload).eq("member_id", member_id).execute()
    if resp.data:
        return {"success": " Member info updated.", "data": resp.data}
    return {" Member not found."}



def main_menu():
    while True:
        print("\n Library Management System - Update Records")
        print("1. Update book stock")
        print("2. Update member info")
        print("0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            book_id = int(input("Enter book ID: ").strip())
            added_stock = int(input("Enter number of copies to add: ").strip())
            print(update_book_stock(book_id, added_stock))

        elif choice == "2":
            member_id = int(input("Enter member ID: ").strip())
            new_name = input("Enter new name (leave blank to skip): ").strip()
            new_email = input("Enter new email (leave blank to skip): ").strip()
            print(update_member(member_id, new_name or None, new_email or None))

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main_menu()

