import requests
import review
import pandas

# レビューデータのデータフレームの作成
def create_review_data_frame(reviews):
    # レビューテーブルのカラム
    COLUMNS = ['reviewId','productId', 'name', 'gender', 'ageRange', 'shoeSize', 'heightRange', 'weightRange', 'purchasedSize', 'rate', 'fit', 'comment' ]   
    return pandas.DataFrame(reviews, columns=COLUMNS);


CATEGORIES = [{'id' :1071, 'name'   :"WOMEN"},
              {'id' :1072, 'name'   :"MEN"}]


products = []; 

for category in CATEGORIES: 
    load_url = "https://www.uniqlo.com/jp/api/commerce/v5/ja/products?q=%E3%82%A8%E3%82%A2%E3%83%AA%E3%82%BA%E3%83%A0%20T%E3%82%B7%E3%83%A3%E3%83%84&path=" + str(category['id'])+ "&offset=0&limit=28"
    
    HEADERS = {"content-type": "application/json"}
    html = requests.get(load_url,  headers=HEADERS);
    data = html.json();
    
    # 商品情報のAPI取得
    items = data['result']['items']
    
    # productsに商品名, 商品ID, 評定値, レビューした人の人数を追加
    # データの形式はsample_data.pyを参照すること
    for item in items:
        if  item['genderName'] == category['name'] :
            info =  {
                        "product_name"  : item['name'],
                        "product_id"    : item['productId'],
                        "rating_score"  : item['rating']['average'],
                        "rating_count"  : item['rating']['count'],
                        "gender"        : item['genderName'] 
                    };
            
            products.append(info);

# カテゴリー内の各商品のレビューを配列格納
review = review.get_review_data(products)

#　収集したデータでデータフレームを作成
review_data_frame = create_review_data_frame(review)

#　CSVファイルの作成
review_data_frame.to_csv('airism_review.csv', encoding='utf_8_sig');
