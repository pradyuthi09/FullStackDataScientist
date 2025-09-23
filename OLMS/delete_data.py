import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)



def delete_member(member_id: int):
    active = (
        sb.table("borrow_records")
        .select("record_id")
        .eq("member_id", member_id)
        .is_("return_date", None)   
        .execute()
    )

    if active.data:  
        return {"error": "Member has active borrowed books,Cannot delete."}

    resp = sb.table("members").delete().eq("member_id", member_id).execute()
    if resp.data:
        return {"success": f" Member {member_id} deleted.", "data": resp.data}
    return {"error": " Member not found."}


def delete_book(book_id: int):
    
    active = (
        sb.table("borrow_records")
        .select("record_id")
        .eq("book_id", book_id)
        .is_("return_date", None)
        .execute()
    )

    if active.data:  
        return {"error": "Book is currently borrowed. Cannot delete."}

    resp = sb.table("books").delete().eq("book_id", book_id).execute()
    if resp.data:
        return { f"Book {book_id} deleted."}
    return {"error": "Book not found."}


if __name__ == "__main__":
    print("Library Management System - Delete Records")
    print("1. Delete Member")
    print("2. Delete Book")
    choice = input("Enter choice : ").strip()

    if choice == "1":
        mid = int(input("Enter Member ID to delete: ").strip())
        result = delete_member(mid)
        print(result)

    elif choice == "2":
        bid = int(input("Enter Book ID to delete: ").strip())
        result = delete_book(bid)
        print(result)

    else:
        print("Invalid choice")

