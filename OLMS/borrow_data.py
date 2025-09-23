import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
sb: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def borrow_book(member_id, book_id):
    
    resp = sb.table("books").select("stock").eq("book_id", book_id).execute()
    if not resp.data:
        return {"Book not found."}

    stock = resp.data[0]["stock"]
    if stock <= 0:
        return { " Book not available."}

    try:
        sb.table("books").update({"stock": stock - 1}).eq("book_id", book_id).execute()

        
        sb.table("borrow_records").insert({
            "member_id": member_id,
            "book_id": book_id
        }).execute()

        return { f" Book {book_id} borrowed by member {member_id}"}

    except Exception as e:
        return {"error": f"Transaction failed: {str(e)}"}

if __name__ == "__main__":

        print("Library Management System - Borrow Book")
        print("1. Borrow a book")
        print("0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            member_id = int(input("Enter member ID: ").strip())
            book_id = int(input("Enter book ID: ").strip())
            print(borrow_book(member_id, book_id))

        elif choice == "0":
            print("Exiting")
    

        else:
            print("Invalid choice")

    