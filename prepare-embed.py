import os
import pathlib
from langchain_text_splitters import MarkdownHeaderTextSplitter
from mistralai.client import MistralClient
import libsql_client
from helpers import absoluteFilePaths

db = libsql_client.create_client_sync("ws://127.0.0.1:8080")
ai = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])

raw_pdf_directory = "2024/documents/raw-pdf"
prepared_md_directory = "2024/documents/prepared-md"


headers_to_split_on = [
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

def main():
    try:
        db.batch([
        "DROP TABlE IF EXISTS pdf_embeddings;",
        """
        CREATE TABLE pdf_embeddings (
          title TEXT,
          chunk INT,
          content TEXT, 
          embedding FLOAT32(3)
        );
        """
        ])
        for filename in absoluteFilePaths(prepared_md_directory):
            print(filename)
            print("> Splitting...")
            md_text = pathlib.Path(filename).read_text()
            chunks = splitter.split_text(md_text)

            print("> Embedding...")
            embeddings = ai.embeddings(
                    "mistral-embed",[ chunk.page_content for chunk in chunks]
            ).data
            print("> Storing...")
            insert_args = []
            for i, chunk in enumerate(chunks):
                embeddings_str = str(embeddings[i].embedding)
                insert_args.append(
                    (filename, i , chunk.page_content, f"vectors({embeddings_str})")
                )

            db.batch([
                libsql_client.Statement("INSERT INTO pdf_embeddings VALUES (?, ?, ?, ?)",
                args
                ) for args in insert_args
            ])
    except Exception as e:
        print(e)
    finally:
        db.close()

if __name__ == "__main__":
    main()
