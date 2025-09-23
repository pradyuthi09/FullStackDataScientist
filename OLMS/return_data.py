import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

sb: Client = create_client(url, key)

def return_book(record_id: int):
  
    try:
        resp = sb.rpc("return_book", {"p_record_id": record_id}).execute()
        if resp.data:
            return f" Book successfully returned (Record {record_id})"
        else:
            return "Nothing returned ."
    except Exception as e:
        return f" Error: {e}"

if __name__ == "__main__":
    print(" Return Book Transaction")
    try:
        rid = int(input("Enter Borrow Record ID to return: ").strip())
        result = return_book(rid)
        print(result)
    except ValueError:
        print(" Invalid input. Please enter a number.")
