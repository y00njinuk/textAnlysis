
from lexrankr import LexRank
import sys
import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

# sys.argv[1] : text file directory <txt dir>
# sys.argv[2] : number of summaries <int>

def read_txt(dir):
    f = open(dir, 'r')
    text = f.read()
    f.close()
    return(text)

def main():
    if len(sys.argv) is 2:
        text = read_txt(sys.argv[1])
        num_summaries = 3 # default number of summaries
    elif len(sys.argv) is 3:
        text = read_txt(sys.argv[1])
        num_summaries = int(sys.argv[2])
    else:
        print("Usage: TextSummarize.py [Text <txt dir>, num_summaries <int>]")
        return(0)

    lexrank = LexRank()  # can init with various settings
    lexrank.summarize(text)
    summaries = lexrank.probe(num_summaries)
    
    df = pd.DataFrame(columns = ['rank', 'summary'])
    for i, summary in enumerate(summaries):
        df.loc[i] = [i+1, summary]

    out = df.to_json(orient='records', force_ascii=False)
    out = "{\"RESULT\":%s}" % out
    print(out)

if __name__=='__main__':
    main()
