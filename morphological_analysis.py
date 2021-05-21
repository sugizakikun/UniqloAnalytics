# -*- coding: utf-8 -*-
"""
@author: Miki Sugihara
"""

import pandas
import urllib.request
import re
import MeCab

#改行コードを取り除く
def remove_new_line_character(text):
    text = text.replace('\n', '');
    text = text.replace('\r', '');
    return text;


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


# リストを文字列に変換する関数
def join_list_str(list):
    return ' '.join(list)


# ストップワード
stopwords = set_stopwords();

#内容語（名詞・形容詞・動詞・副詞）のみを抽出
tagger = MeCab.Tagger()

def extract_content_words(text):
    content_words = [];
    node = tagger.parseToNode(text);
    
    while node:
        if( node.feature.split(",")[0] not in ['助詞', '助動詞', '接続詞', '補助記号']):
            if( node.surface not in stopwords ):
                content_words.append(node.surface)
        node = node.next;
    
    content_words.pop(0);

    return join_list_str(content_words);
    


review_df = pandas.read_csv('review_data.csv', index_col=0);

#　改行コードを取り除く
review_df['remove_new_line_character'] = review_df['comment'].map(remove_new_line_character);

# 数字を0に置換
review_df['comment_number_to_zero'] = review_df['remove_new_line_character'].map(replace_number_to_zero)

#　分かち書きしたカラムをdfに追加する  
review_df['lsbw'] = review_df['comment_number_to_zero'].map(extract_content_words)
print(review_df['lsbw']);


#review_df['excluded'] = review_df['lsbw'].map(exclude_stopword)



