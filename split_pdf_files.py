from PyPDF2 import PdfReader,PdfWriter
import os
def chapter_name_edit(name):
    new_name = name
    not_allowed = [
        "\\",
        "/",
        ":",
        "*",
        "?",
        '"',
        "<",
        ">",
        "|",
                ]   
    for i in new_name:
        if not_allowed.__contains__(i):
            new_name = new_name.replace(i,"_")
    return new_name
def split_pdf(path_or_dir):
    pdfs = []
    if(path_or_dir.upper().endswith(".PDF")):
        pdfs.append(path_or_dir)
    else:
        for i in os.listdir(path_or_dir):
           if(i.upper().endswith(".PDF")):
                pdfs.append(f'{path_or_dir}\\{i}')
    for pdf_file in pdfs:
        
        file_name = pdf_file.split(".")[0]
        print(f"Start spliting {file_name}.......")
        reader = PdfReader(pdf_file)
        chapters = []
        chapte = reader.outline
        for i in chapte:
            page_namber = reader.get_page_number(i.page)
            chapters.append({
                "page":page_namber,"title":i.title
            })
        for i in chapters:
            try:
                # print(f"{i['title']} start on {i['page']} end on {chapters[chapters.index(i) +1 ]['page'] - 1}")
                chapters[chapters.index(i)]["start"] = i['page']
                chapters[chapters.index(i)]["end"] = chapters[chapters.index(i) +1 ]['page'] - 1
            except:
                # print(f"{i['title']} start on {i['page']} end on {len(reader.pages)}")
                chapters[chapters.index(i)]["start"] = i['page']
                chapters[chapters.index(i)]["end"] = len(reader.pages)
        try:
            os.makedirs(file_name)
        except:
            pass

        for i in chapters:
            print(f"Writing {i['title']} from {file_name}")
            chapter_ = PdfWriter()
            index = i['start']
            while index != i['end'] +1:
                try:
                    chapter_.add_page(reader.pages[index])
                except:
                    pass
                index+=1
            file = open(f'{file_name}\\{chapter_name_edit(i["title"])}.pdf',"wb")
            chapter_.write(file)
            file.close()
            
while True:
    path = input("pdf file / Folder path:")
    split_pdf(path)
    print("Done.....")
