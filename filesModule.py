import os

def list_files(directory, doc_dic):
    list = []
    # Walk the tree.
    for root, dirs, files in os.walk(directory):
        for filename in files:
            list.append(os.path.join(root, filename))
            doc_dic.write(f'{filename} {len(list) - 1}\n')
        break
    doc_dic.close()
    return list

def get_file_content(filepath):
    with open(filepath, 'r') as file:
        file_content = file.read()
    return file_content

def parse_index_line(text):
    brk = text.index(' ')
    parts = [text[:brk], text[brk+1:]] # Break text to two parts (term and postings)
    term, posts = parts[0], parts[1].removesuffix('\n')
    return term, posts

def parse_index(path):
    dic = {}
    with open(path, 'r') as file:
        for line in file.readlines():
            term, post = parse_index_line(line)
            dic[term] = post
    return dic

def open_write(root, ifolder, fname):
    make_dir(root, ifolder)
    path = os.path.join(root, ifolder, str(fname))
    return open(path, 'w')

def open_reads(root, ifolder, max):
    list = []
    for n in range(0, max):
        path = os.path.join(root, ifolder, str(n))
        file = open(path, 'r')
        list.append(file)
    return list

def clear_dir(root, ifolder):
    path = os.path.join(root, ifolder)
    if os.path.exists(path):
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))
        os.rmdir(path)

def make_dir(root, folder):
    path = os.path.join(root, folder)
    if not os.path.exists(path):
        os.mkdir(path)