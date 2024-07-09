from helpers import absoluteFilePaths
import pymupdf4llm
import pathlib

raw_pdf_directory = "2024/documents/raw-pdf"
prepared_md_directory = "2024/documents/prepared-md"

def main():
    print("Preparing 2024 docs...")
    for filename in absoluteFilePaths(raw_pdf_directory):
        print("Converting " + filename)
        md_text = pymupdf4llm.to_markdown(filename)
        
        filename = filename.replace(raw_pdf_directory, prepared_md_directory)   
        filename = filename.replace(".pdf", ".md")
        pathlib.Path(filename).write_text(md_text)
        print("Converted " + filename)

    print("Done!")

if __name__ == "__main__":
    main()
