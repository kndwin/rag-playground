import os
from mistralai.client import MistralClient
import libsql_client
from helpers import absoluteFilePaths

db = libsql_client.create_client_sync("ws://127.0.0.1:8080")
ai = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])

questions = [
"""
To whom can you make a whistleblower disclosure to under the Mirvac
Whistleblower Policy:

Mirvac Whistleblower Hotline

Mirvac Group General manager, Risk & Audit or any member of Mirvac’s
internal or external audit team

Any member of the Executive Leadership Team

Mirvac’s Human Resources Managers

All of the above
"""
]

def main():
    try:
        db.batch([
        "DROP TABlE IF EXISTS questions;",
        """
        CREATE TABLE questions (
          question TEXT,
          year INT,
          embedding FLOAT32(3)
        );
        """
        ])


        print("> Embedding...")
        # get embeddings
        embeddings = ai.embeddings(
            "mistral-embed", questions
        ).data

        print("> Storing...")
        # store
        insert_args = []
        for i, question in enumerate(questions):
            embeddings_str = str(embeddings[i].embedding)
            insert_args.append(
                (question, 2024, f"vectors({embeddings_str})")
            )

        db.batch([
            libsql_client.Statement(
                "INSERT INTO questions VALUES (?, ?, ?)", args
                ) for args in insert_args
            ])

        print("> Done!")

    except Exception as e:
        print(e)
    finally:
        db.close()



if __name__ == "__main__":
    main()
