# RAG Playground

## Context

I trained some internal policies documents in order to play around with RAG

## Overview

ai: mistral (scored high on METB and was cheapish)
- https://huggingface.co/spaces/mteb/leaderboard

vector store: libsql (thought turso would support it for libsql as well but they don't as of now :( ), workaround was i stored them as string (lol) and used numpy to calculate the cosine similarity
- https://turso.tech/blog/turso-brings-native-vector-search-to-sqlite

pdf to markdown generation: pymupdf4llm (pretty fast and mupdf seems to only support this for python)
- https://pymupdf4llm.readthedocs.io/en/latest/

text splitter: Chose level 3 cause the context of these PDF's could fit in a chat and I didn't like any levels lower
- https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb

prompt engineering: didn't play around too much but just took the best zero-shot CoT trigger prompt from APE
- https://www.promptingguide.ai/techniques/ape

## Structure

- Make sure you have your MISTRAL_API_KEY
- The structure of the folders look like this

```
2024/
├── answers.md
├── documents
│   ├── prepared-md
│   │   ├── Privacy_Policy.md
│   │   ├── Government_Relations_Policy.md
│   │   ├── ...
│   │   └── Security_Trading_Policy.md
│   └── raw-pdf
│       ├── Privacy_Policy.pdf
│       ├── ...
│       ├── Government_Relations_Policy.pdf
│       └── Security_Trading_Policy.pdf
├── embed.db // This is just artifacts from using libsql (it didn't work anyway so a sqlite db file should also work)
│   ├── data
│   ├── data-shm
│   ├── data-wal
│   ├── stats.json
│   └── wallog
└── questions.html
```

## Output example

```
python3 get-answers.py
----------------
QUESTION

To whom can you make a whistleblower disclosure to under the Mirvac
Whistleblower Policy:

Mirvac Whistleblower Hotline

Mirvac Group General manager, Risk & Audit or any member of Mirvac’s
internal or external audit team

Any member of the Executive Leadership Team

Mirvac’s Human Resources Managers

All of the above

DOC
/Users/knd/Code/mirvac/lto-group-compliance/2024/documents/prepared-md/Microsoft Word - 2022.06 Fraud Bribery and Corruption Policy (Final).docx.md
----------------
ANSWER
The question asks who can a whistleblower disclosure be made to under the Mirvac Whistleblower Policy. To answer this question, we need to find information in the provided context that specifies the parties to whom such disclosures can be made.

After reading through the provided policy document, we can find the relevant information in section 3.1 under the obligations as a Workplace Participant. It states that if an employee sees or suspects any fraud, bribery, or corruption, they must report it immediately to their line manager or one-up manager. If those reporting avenues are unavailable, they may report the matter to any of the channels outlined in the Mirvac Whistleblower Policy, including the Whistleblower Investigation Officer (Mirvac's Group General Manager, Risk & Internal Audit) or the Mirvac Whistleblower Hotline. If the reporter is a Workplace Participant other than an employee, they must report the matter to the Mirvac Whistleblower Investigation Officer or the Mirvac Whistleblower Hotline.

Based on the information provided in the policy document, the correct answer to the question is option 'All of the above', which includes:
- Mirvac Whistleblower Hotline
- Mirvac Group General manager, Risk & Audit or any member of Mirvac’s internal or external audit team
- Any member of the Executive Leadership Team
- Mirvac’s Human Resources Managers
python3 get-answers.py
---------------- QUESTION -------------

To whom can you make a whistleblower disclosure to under the Mirvac
Whistleblower Policy:

Mirvac Whistleblower Hotline

Mirvac Group General manager, Risk & Audit or any member of Mirvac’s
internal or external audit team

Any member of the Executive Leadership Team

Mirvac’s Human Resources Managers

All of the above

---------------- DOCS -------------
/Users/knd/Code/mirvac/lto-group-compliance/2024/documents/prepared-md/Microsoft Word - 2022.06 Fraud Bribery and Corruption Policy (Final).docx.md
---------------- ANSWER -------------
The question asks who can a whistleblower disclosure be made to under the Mirvac Whistleblower Policy. To answer this question, we need to find information in the provided context that relates to the Mirvac Whistleblower Policy and the available options for reporting.

In the context provided, there is a mention of the Mirvac Whistleblower Policy under section 1 PURPOSE, which lists it as one of the related policies. However, the details of the policy are not provided in the given text.

Nonetheless, there are some clues in the text that can help us answer the question. In section 3.1 OBLIGATIONS TO PREVENT FRAUD, BRIBERY OR CORRUPTION, it is mentioned that:

"If you see or suspect any actual or potential for fraud, bribery or corruption you must, if you are an employee, report it immediately to your line manager or one up manager. If for some reason those reporting avenues are unavailable, you may report the matter to any of the channels outlined in the Mirvac Whistleblower Policy, including to the Whistleblower Investigation Officer (Mirvac's Group General Manager, Risk & Internal Audit) or the Mirvac Whistleblower Hotline."

Based on this information, we can infer that a whistleblower disclosure can be made to the following options:

* Line manager or one up manager (not explicitly mentioned in the answer options)
* Mirvac Whistleblower Hotline
* Mirvac Group General Manager, Risk & Internal Audit or any member of Mirvac’s internal or external audit team (this can be inferred as the Whistleblower Investigation Officer is Mirvac's Group General Manager, Risk & Internal Audit)

However, the answer options also include "Any member of the Executive Leadership Team" and "Mirvac’s Human Resources Managers," which are not explicitly mentioned in the text. Therefore, based on the information provided, we cannot definitively say that these two options are valid.

Given the available information, the most accurate answer would be "Mirvac Whistleblower Hotline" and "Mirvac Group General Manager, Risk & Internal Audit or any member of Mirvac’s internal or external audit team." However, if we assume that the Executive Leadership Team and Human Resources Managers are also valid options based on general whistleblowing practices, then the answer would be "All of the above."
```
