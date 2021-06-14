import parsing

def write_term_index(data):
    with open('term_index.txt', 'w') as f:
        # for each document
        for key, value in data.items():
            f.write("{}\t".format(key))
            # for every the postion o each term
            for i in value[-1]:
                f.write('{}:{}\t'.format(i[0], i[-1][0]))
            f.write('\n')

def write_term_info(data):
    with open('term_info.txt', 'w') as f:
        for key, value in data.items():
            offset = f.tell()
            occur = value[1]
            total_count = len(value[-1])
            f.write("{}\t{}\t{}\t{}\n".format(key, offset, occur, total_count))

# to write termIds and docIds
def write_Ids(data, filename):
    with open(filename, 'w') as f:
        for key, value in data.items():
            f.write("{}\t{}\n".format(value, key))


if __name__ == '__main__':
    termIds, docIds, termInfo, termCount = parsing.Tokenization()
    write_Ids(termIds, 'termids.txt')
    write_Ids(docIds,'docids.txt')
    write_term_info(termInfo)
    write_term_index(termInfo)






