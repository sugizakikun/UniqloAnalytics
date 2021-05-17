# -*- coding: utf-8 -*-
"""
@author: Miki Sugihara
"""

import pandas
import urllib.request
import re
import MeCab

# 形態素解析に関係ない数字を全て⓪に置換する関数
def replace_number_to_zero(text):
    changed_text = re.sub(r'[0-9]+', "0", text) #半角
    changed_text = re.sub(r'[０-９]+', "0", changed_text) #全角
    return changed_text


# ストップワードの定義
def set_stopwords():
    slothlib_path = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    slothlib_file = urllib.request.urlopen(slothlib_path)
    slothlib_stopwords = [line.decode("utf-8").strip() for line in slothlib_file]
    slothlib_stopwords = [ss for ss in slothlib_stopwords if not ss==u'']
    return set(slothlib_stopwords);

# 新語を含むmecab-ipadic-neologdで形態素解析する
tagger = MeCab.Tagger()

# 分かち書きした結果を返す関数
def leaving_space_between_words_column(text):
    splitted = ' '.join([x.split('\t')[0] for x in tagger.parse(text).splitlines()[:-1] if x.split('\t')[1].split(',')[0] not in ['助詞', '助動詞', '接続詞', '動詞', '記号']])
    return splitted


review_df = pandas.read_csv('review_data.csv', index_col=0);

# 数字を0に置換
review_df['comment_number_to_zero'] = review_df['comment'].map(replace_number_to_zero)

# 分かち書きしたカラムをdfに追加する
#review_df['lsbw'] = review_df['comment_number_to_zero'].map(leaving_space_between_words_column)
review_df.head()

print( leaving_space_between_words_column(review_df['comment_number_to_zero'][0]))

print(leaving_space_between_words_column( review_df['comment_number_to_zero'])

