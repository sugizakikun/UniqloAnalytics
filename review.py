# -*- coding: utf-8 -*-
import requests
import math

# 分析対象のデータを抽出 & 整形
def extract_analysis_data(review):
    return [
                review['reviewId'],
                review['productId'],
                review['name'],
                review['gender'],
                review['ageRange'],
                review['shoeSize'],
                review['heightRange'], 
                review['weightRange'],
                review['purchasedSize'],
                review['rate'],
                review['fit'],
                review['comment'],
            ];

def get_review_data(products):
    HEADERS = {"content-type": "application/json"};
    
    #API URLの接頭辞
    base_url = "https://www.uniqlo.com/jp/api/commerce/v5/ja/products/";
    
    #　解析対象のレビューデータを格納
    review = [];
    
    for product in products: 
        product_id = product['product_id'];
        
        # 過剰にリクエストを送らないため、１ページあたりのデータ数を25に設定
        limit = 25
        
        #　レビューの総ページ数
        page = (math.floor(product['rating_count'] / limit) + 1);
        
        for i in range(page):
            review_url = base_url + product_id + "/reviews?limit=" + str(limit) + "&offset=" + str(i*limit)
        
            html = requests.get(review_url,  headers=HEADERS);
            data = html.json();
        
            #商品レビューをAPIで取得
            review_api = data['result']['reviews']
            
            #APIデータの整形
            review = review + list(map(extract_analysis_data,  review_api));     
    
    return review;    


    
