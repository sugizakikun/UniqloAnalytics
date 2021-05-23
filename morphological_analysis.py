# -*- coding: utf-8 -*-
"""
@author: Miki Sugihara
"""

import pandas
import urllib.request
import re
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer

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
    
    slothlib_stopwords += ['0', 'センチ', 'キロ', 'cm', 'kg', 'ユニクロ', 'UNIQLO', 'Uniqlo', 'ｃｍ', 'ｋｇ'] 
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
        if( node.feature.split(",")[0] not in ['助詞', '助動詞', '接続詞', '動詞', '補助記号']):
            if( node.surface not in stopwords ):
                content_words.append(node.surface)
        node = node.next;
    
    content_words.pop(0);

    return join_list_str(content_words);


def split_review_for_gender(review_df, gender):     
    #　改行コードを取り除く
    review_df['remove_new_line_character'] = review_df['comment'].map(remove_new_line_character);
    
    # 数字を0に置換
    review_df['comment_number_to_zero'] = review_df['remove_new_line_character'].map(replace_number_to_zero)
    
    #　分かち書きしたカラムをdfに追加する  
    review_df['lsbw'] = review_df['comment_number_to_zero'].map(extract_content_words)
    
    return review_df[review_df['gender'] == gender]



review_df = pandas.read_csv('airism_review.csv', index_col=0);

women_review = split_review_for_gender(review_df, '女性');
men_review = split_review_for_gender(review_df, '男性');

# 女性の口コミテキストの結合
sum_review_women = ''
for text in women_review['lsbw']:
    sum_review_women += text
    
# 男性の口コミテキストの結合
sum_review_men = ''
for text in men_review['lsbw']:
    sum_review_men += text
    
# 男性と女性の口コミを合体させたデータフレームの作成
merge_df = pandas.DataFrame({'score': ['女性', '男性'],
                    'sum_review': [sum_review_women, sum_review_men]})


# TF-IDFの計算
tfidf_vectorizer = TfidfVectorizer(
    min_df = 0.03,
    ngram_range=(1, 2) # n_gramのレンジを1と2で計算
)

# 文章内の全単語のTfidf値を取得
tfidf_matrix = tfidf_vectorizer.fit_transform(merge_df['sum_review'])

# index 順の単語リスト
terms = tfidf_vectorizer.get_feature_names()


tfidfs = tfidf_matrix.toarray()

# 形状
print(tfidfs.shape)
