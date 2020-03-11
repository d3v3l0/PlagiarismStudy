import time
from datetime import datetime, timedelta
from operator import itemgetter

def currentTime():
    return str(timedelta(seconds = time.time() - start_time)).split('.')[0]

start_time = time.time()

print(currentTime(), 'STARTED OPERATING — GATHERING DATA')

bookkeeping_blocks_project = {}
with open('../SourcererCC/tokenizers/block-level/blocks_tokens/files-tokens-all.tokens', 'r', encoding='utf8') as fin:
    for line in fin:
        data = line.split(',')
        bookkeeping_blocks_project[int(data[1])] = int(data[0])

print(currentTime(), 'Read projects data')

bookkeeping_blocks_blame = {}
with open('data/StatisticsBlameBlocks.txt', 'r') as fin:
    for line in fin:
        data = line.rstrip().split(';')
        bookkeeping_blocks_blame[int(data[0])] = datetime.strptime(data[-1],'%Y-%m-%d')

print(currentTime(), 'Read blames data')

bookkeeping_files_license = {}
with open('data/StatisticsLicensesFiles.txt', 'r') as fin:
    for line in fin:
        data = line.rstrip().split(';')
        bookkeeping_files_license[int(data[0])] = data[-1]

print(currentTime(), 'Read licenses data')

count = 0
bookkeeping_plagiarism = {}

with open('data/StatisticsNeighbors.txt', 'r') as fin:
    for line in fin:
        count = count + 1
        current_block = int(line.split(';')[0])
        clone_blocks = set()
        for i in line.split(';')[1].rstrip().split(','):
            clone_blocks.add(int(i))
        for i in clone_blocks:
            if (bookkeeping_blocks_blame[i] < bookkeeping_blocks_blame[current_block]) and (bookkeeping_blocks_project[i] != bookkeeping_blocks_project[current_block]):
                borrow = bookkeeping_files_license[int(str(i)[5:])] + '/' + bookkeeping_files_license[int(str(current_block)[5:])]
                if borrow not in bookkeeping_plagiarism:
                    bookkeeping_plagiarism[borrow] = 1
                else:
                    bookkeeping_plagiarism[borrow] = bookkeeping_plagiarism[borrow] + 1
        if count % 10000 == 0:
            print(currentTime(), 'Processed', count, 'lines')

print(currentTime(), 'Completed processing')

sorted_plagiarism = sorted(bookkeeping_plagiarism.items(), key=itemgetter(1), reverse = True)
with open('data/Plagiarism.txt','w+') as fout:
    for i in sorted_plagiarism:
        fout.write(str(i[0]) + ';' + str(i[1]) + '\n')

print(currentTime(), 'Sorted and wrote the data to file')
print(currentTime(), 'ANALYSIS COMPLETE')
