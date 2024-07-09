import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import numpy as np
import libsql_client
from helpers import absoluteFilePaths

db = libsql_client.create_client_sync("ws://127.0.0.1:8080")
ai = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])

def main():
    try:
        questions = db.execute("SELECT * FROM questions")
        pdfs = db.execute("SELECT * FROM pdf_embeddings")

        for q in questions:
            [question, year, embedding_str] = q
            q_vec = np.fromstring(embedding_str[9:-2], sep=",")

            closest_pdfs = []
            for p in pdfs:
                [title, chunk, content, embedding_str] = p
                # stored as "vector([...])" string (i thought libsql would work but it's only supported in turso)
                p_vec = np.fromstring(embedding_str[9:-2], sep=",")

                cos_sum = np.dot(q_vec, p_vec)
                closest_pdfs.append((cos_sum, title, content))

            closest_pdfs = sorted(closest_pdfs, key=lambda x: x[0], reverse=True)
            top_pdf = closest_pdfs[0]
            [cos_sum, title, pdf_content] = top_pdf

            # APE method (https://www.promptingguide.ai/techniques/ape)
            message_content = """
            You are determining what is the answer given a multiple choice question.
            The question is:
            {}

            The context to answer this question is:
            {}

            Let's work this out in a step by step way to be sure we have the right answer.
            Explain your answer in as much detail as possible.
            """.format(question, pdf_content)

            message = ChatMessage(
                    role="user",
                    content=message_content
            )
            response = ai.chat(
                    model="mistral-large-latest",
                    messages=[message]
            )

            print("---------------- QUESTION -------------")
            print(question)
            print("---------------- DOCS -------------")
            print(title)
            print("---------------- ANSWER -------------")
            print(response.choices[0].message.content)


    except Exception as e:
        print(e)
    finally:
        db.close()

if __name__ == "__main__":
    main()
