# -*- coding: utf-8 -*-
"""
@author: Miki Sugihara
"""

import pandas
import preprocess as p
from sklearn.feature_extraction.text import TfidfVectorizer

# TF-IDF の結果からi 番目のドキュメントの特徴的な上位 n 語を取り出す関数
# terms = 単語リスト
# tfidfs = TF-IDF行列
def extract_feature_words(terms, tfidfs, i, n):
    tfidf_array = tfidfs[i]
    top_n_idx = tfidf_array.argsort()[-n:][::-1]
    words = [terms[idx] for idx in top_n_idx]
    return words


review_df = pandas.read_csv('airism_review.csv', index_col=0);

women_review = p.split_review_for_gender(review_df, '女性');
men_review = p.split_review_for_gender(review_df, '男性');

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

# 新しい列を追加
merge_df['tfidf'] = ''

# 結果の出力
for i in range(0, len(merge_df['sum_review'])):
    print ('------------------------------------------')
    print (merge_df['score'][i])
    feature_words = extract_feature_words(terms, tfidfs, i, 150)
    print ('feature_words:')
    print(feature_words)
    merge_df.at[i, 'tfidf'] = feature_words


l1 = merge_df.at[0, 'tfidf']
l2 = merge_df.at[1, 'tfidf']

# 3.5以上にしか存在しない単語
result = set(l1) - set(l2)
print(result)

# 3.3以下にしか存在しない単語
result = set(l2) - set(l1)
print(result)