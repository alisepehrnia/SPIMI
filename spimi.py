import os
import time
import filesModule as files
import langModule as lang

# Config Vars
_root, _ifolder = r'toy-data', '_index1'
_block_size, _post_init_size = 5, 3
_stemming, _alpha =  False, True

files.clear_dir(_root, _ifolder) # delete old index files

# Global Vars
_files_list = files.list_files(_root, files.open_write(_root, _ifolder, 'docs'))
_index, n = 0, 0
_posts_size = {}

def SPIMI_INDEX_CONSTRUCTION(stemming, alpha):
    global n
    n = 0
    while(_index < len(_files_list)):
        token_stream = PARSE_NEXT_BLOCK(stemming, alpha)
        SPIMI_INVERT(token_stream)
        n = n + 1
    MERGE_BLOCKS(f_list(n), f('index'))

def PARSE_NEXT_BLOCK(stemming, alpha):
    global _index
    block = []
    stop = min(_index + _block_size, len(_files_list))
    for i in range(_index, stop):
        file_content = files.get_file_content(_files_list[i])
        term_docIDs = lang.get_term_docIDs(file_content, i, stemming, alpha)
        block.extend(term_docIDs)
    _index = _index + _block_size
    return block

def SPIMI_INVERT(token_stream):
    output_file = NEW_FILE() #= output_file ← NEW_FILE()
    dictionary = {} #= dictionary ← NEW_HASH()
    while(True): #= while(free memory available)
        for token in token_stream: #= do token ← next(token_stream)
            term, docID = token[0], token[1]
            if term not in dictionary: #= if term(token) ∉ dictionary then
                postings_list = dictionary[term] = [] #= postings_list ← ADD_TO_DICTIONARY(dictionary, term(token))
            else:
                postings_list = dictionary[term] #= postings_list ← GET_POSTINGS_LIST(dictionary, term(token))
            if full(postings_list, term): #= if full(postings_list) then
                _posts_size[term] *= 2 #= postings_list ← DOUBLE_POSTINGS_LIST(dictionary, term(token))
            postings_list.append(docID) #= ADD_TO_POSTINGS_LIST(postings_list, docID)
        break # To stop while from infinite loop!
    sorted_terms = sorted(dictionary.items(), key=lambda x: x[0]) #= sorted_terms ← SORT_TERMS(dictionary)
    WRITE_BLOCK_TO_DISK(sorted_terms, dictionary, output_file)
    return output_file

def MERGE_BLOCKS(input_files, output_file):
    curr_lines = [file.readline().removesuffix('\n') for file in input_files]
    prev_term, curr_term = None, None
    first = True

    while len(input_files) > 0:
        #m = min(curr_lines, key = lambda l: prs(l))
        m = min(curr_lines, key = lambda l: (l.split(' ')[0], int(l.split(' ')[1])))
        p = curr_lines.index(m) # Index of doc with smallest term and smallest postings list
        curr_term, last_posts = files.parse_index_line(m) # Parse current line

        if curr_term != prev_term:
            if first:
                first = False
            else:
                output_file.write('\n') # Go to new line if its not the first line
            output_file.write(f'{curr_term} {last_posts}')
            prev_term = curr_term
        else:
            output_file.write(f' {last_posts}')

        nwline = input_files[p].readline()
        curr_lines[p] = nwline
        if nwline == '' or nwline == '\n' :
            input_files[p].close()
            input_files.pop(p)
            curr_lines.pop(p) 

    output_file.close()

def full(list, term):
    global _posts_size
    if term in _posts_size:
        return len(list) >= _posts_size[term]
    else:
        _posts_size[term] = _post_init_size
        return False

def WRITE_BLOCK_TO_DISK(sorted_terms, dictionary, output_file):
    for term, postings in sorted_terms:
        output = f'{term} ' + ' '.join([str(i) for i in postings]) + '\n'
        output_file.write(output)
    output_file.close()

def NEW_FILE():
    files.make_dir(_root, _ifolder)
    return files.open_write(_root, _ifolder, str(n))

#fn
def f(n):
    return files.open_write(_root, _ifolder, n)

#f1,...,fn
def f_list(max):
    return files.open_reads(_root, _ifolder, max)

start = time.perf_counter()
SPIMI_INDEX_CONSTRUCTION(_stemming, _alpha)
end = time.perf_counter()

print('//Number of files proccessed: ', len(_files_list))
print('//Number of blocks proccessed: ', n)
lines_num = 0
with open(os.path.join(_root, _ifolder, 'index'), 'r') as file:
        lines_num = len(file.readlines())
print('//Total words in dictionary: ', lines_num)
print('//Index construction time: ', ((end - start) * 1000), 'ms')

# Performance count
""" times, t_sum = 0, 0

for i in range(10):
    start = time.perf_counter()
    SPIMI_INDEX_CONSTRUCTION(_stemming, _alpha)
    end = time.perf_counter()

    t_sum += end - start
    times += 1

print(t_sum / times * 1000, "ms") """
#