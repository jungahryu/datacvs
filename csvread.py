import pandas as pd

# CSV 파일을 'cp949' 인코딩으로 읽기
data = pd.read_csv('data.csv', encoding='cp949')

# 데이터 확인
print(data.head())

def filter_stores(data, region=None, category=None, menu=None, price_range=None):
    filtered = data

    if region:
        filtered = filtered[filtered["지역명"].str.contains(region)]

    if category:
        filtered = filtered[filtered["업종명"] == category]

    if menu:
        filtered = filtered[filtered["메뉴명"].str.contains(menu)]

    if price_range:
        min_price, max_price = price_range
        filtered = filtered[
            (filtered["가격"] >= min_price) & (filtered["가격"] <= max_price)
        ]

    return filtered

from fastapi import FastAPI, Query
from typing import Optional, List

app = FastAPI()

@app.get("/stores/")
def get_stores(
    region: Optional[str] = None,
    category: Optional[str] = None,
    menu: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    # CSV 데이터 로드 (이 부분은 메모리 효율성을 위해 적절히 개선 필요)
    data = pd.read_csv("data.csv")
    
    # 필터링
    result = filter_stores(
        data, 
        region=region, 
        category=category, 
        menu=menu, 
        price_range=(min_price, max_price) if min_price and max_price else None
    )
    
    return result.to_dict(orient="records")



