import requests
import json
import review
import pandas

# レビューデータのデータフレームの作成
def create_review_data_frame(reviews):
    # レビューテーブルのカラム
    COLUMNS = ['reviewId','productId', 'name', 'gender', 'ageRange', 'shoeSize', 'heightRange', 'weightRange', 'purchasedSize', 'rate', 'fit', 'comment' ]   
    return pandas.DataFrame(reviews, columns=COLUMNS);

HEADERS = {"content-type": "application/json"}

load_url = "https://www.uniqlo.com/jp/api/commerce/v5/ja/products?path=%2C%2C1568%2C3685&categoryId=1568"
html = requests.get(load_url,  headers=HEADERS);
data = html.json();

# 商品情報のAPI取得
items = data['result']['items']

# APIの整形
print(json.dumps(items, indent=4));

products = []; 

# productsに商品名, 商品ID, 評定値, レビューした人の人数を追加
# データの形式はsample_data.pyを参照すること
for item in items:
    info =  {
                "product_name"  : item['name'],
                "product_id"    : item['productId'],
                "rating_score"  : item['rating']['average'],
                "rating_count"  : item['rating']['count']
            };
    
    products.append(info);

# カテゴリー内の各商品のレビューを配列格納
review = review.get_review_data(products)

#　収集したデータでデータフレームを作成
review_data_frame = create_review_data_frame(review)

#　CSVファイルの作成
review_data_frame.to_csv('review_data.csv', encoding='utf_8_sig');
