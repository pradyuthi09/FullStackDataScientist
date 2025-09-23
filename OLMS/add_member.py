
import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)

def add_member(name, email):
    payload = {"name": name, "email": email}
    resp = sb.table("members").insert(payload).execute()
    return resp.data

def add_book(title, author, category, stock):
    payload = {
        "title": title,
        "author": author,
        "category": category,
        "stock": stock
    }
    resp = sb.table("books").insert(payload).execute()
    return resp.data

if __name__ == "__main__":
    print("Library Management System - Create Records")
    print("1. Register new member")
    print("2. Add new book")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        name = input("Enter member name: ").strip()
        email = input("Enter member email: ").strip()
        created = add_member(name, email)
        print("Inserted Member:", created)

    elif choice == "2":
        title = input("Enter book title: ").strip()
        author = input("Enter author: ").strip()
        category = input("Enter category: ").strip()
        stock = int(input("Enter stock: ").strip())
        created = add_book(title, author, category, stock)
        print("Inserted Book:", created)

    else:
        print("Invalid choice")

  