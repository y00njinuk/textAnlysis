from konlpy.tag import Okt
from collections import Counter
import pandas as pd
import sys

import warnings
warnings.filterwarnings("ignore")

# sys.argv[1] : text file directory <txt dir>

def read_txt(dir):
    f = open(dir, 'r')
    text = f.read()
    f.close()
    return(text)

def main():
    if len(sys.argv) is 2:
        text = read_txt(sys.argv[1])
    else:
        print("Usage: TextFrequency.py Text <txt dir>")
        return(0)

    okt = Okt()
    noun = okt.nouns(text)

    for i,v in enumerate(noun):
        if len(v) <2:
            noun.pop(i)
    
    count = Counter(noun)
    
    noun_list = count.most_common(50)

    df = pd.DataFrame(columns = ['Word', 'Freq'])
    df2 = pd.DataFrame(columns = ['TOT_CNT'])

    tot_cnt = 0
    for i, noun in enumerate(noun_list):
        df.loc[i] = [noun[0], noun[1]]
        tot_cnt = tot_cnt + noun[1]

    df2.loc[0] = tot_cnt

    out = df.to_json(orient='records', force_ascii=False)
    out2 = df2.to_json(orient='records', force_ascii=False)
    out = "{\"COUNT\":%s,\"TOT_FREQ\":%s}" % (out2, out)
    print(out)


if __name__=='__main__':
    main()
