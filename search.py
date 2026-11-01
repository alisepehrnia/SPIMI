import os
import time
import filesModule as files
import langModule as lang

# Config Vars
_root, _ifolder = r'data', '_index'
_index_path = os.path.join(_root, _ifolder, 'index')
_stemming, _alpha = True, True

def search_two_terms(list):
    term1, term2 = list[0], list[1]
    if term1 in dic and term2 in dic:
        s1 = set(dic[term1].split(' '))
        s2 = set(dic[term2].split(' '))
        result = ' '.join(sorted(s1.intersection(s2)))
        if len(result) > 0:
            return result
    return None

start = time.perf_counter()
dic = files.parse_index(_index_path)
end = time.perf_counter()
print('//Index reconstruction time: ', ((end - start) * 1000), 'ms', '\n')

# Test if every postings-list in index is sorted correctly
test = True
for k in dic:
    v = [int(n) for n in dic[k].split(' ')]
    v_sorted = sorted(v)
    if v_sorted != v:
        test = False
        break
print(test)
#

query = input("Enter one/two word(s) to search for:\t")
start = time.perf_counter()
terms = lang.proccess_text(query, _stemming, _alpha)
end = time.perf_counter()
print('//Query parse time: ', ((end - start) * 1000), 'ms', '\n')

start = time.perf_counter()
if len(terms) > 0:
    two = False
    result = None
    if len(terms) >= 2:
        two = True
        terms = [terms[0], terms[1]]
        result = search_two_terms(terms)
    else:
        result = dic[terms[0]]
    end = time.perf_counter()
    print('Document ids witch contains ', f'{terms}:\n {result}', '\n')
    print('//Search time: ', ((end - start) * 1000), 'ms', '\n')
else:
    print("Enter meaningful words to search for!")

