from app.nl2sql import generate_sql

if __name__ == "__main__":
    question = input("Enter your analytics question:\n> ")
    generate_sql(question)
