```
python
# kabuka.py
import requests
import json

# ==================== 設定 ====================
API_KEY = "ここにAPI key"
URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"

MOOD_KEYWORDS = {
    "ガッツリ": "ステーキ ハンバーグ 肉 ラーメン 丼",
    "さっぱり": "サラダ 冷麺 魚 そば うどん",
    "豪華": "フレンチ イタリアン 寿司 割烹",
    "ヘルシー": "野菜 サラダ 豆腐 玄米 低カロリー",
    "甘い": "カフェ パンケーキ スイーツ デザート",
    "辛い": "激辛 麻婆 カレー 担々麺",
    "おしゃれ": "カフェ ワイン ビストロ",
    "安い": "定食 ラーメン 牛丼 うどん",
    "ひとり": "カウンター ラーメン そば",
}

# ==================== 座標取得 ====================
def get_lat_lng(location):
    geocode_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location, "format": "json", "limit": 1}
    headers = {"User-Agent": "LunchFinder/1.0"}
    try:
        r = requests.get(geocode_url, params=params, headers=headers, timeout=10)
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0].get("display_name", "")
    except:
        pass
    return None, None, ""

# ==================== 距離自動決定 ====================
def auto_range(lat, lng, place_name):
    """場所に応じて検索距離を自動決定"""
    urban_areas = ["東京", "大阪", "名古屋", "横浜", "京都", "神戸", "札幌", "福岡", "仙台", "広島"]
    if any(city in place_name for city in urban_areas):
        return 2  # 都市部: 500m
    elif "駅" in place_name or "町" in place_name or "市" in place_name:
        return 3  # 駅周辺: 1km
    else:
        return 5  # 地方: 3km

# ==================== 予算コード ====================
def get_budget_code(budget_input):
    if not budget_input:
        return ""
    try:
        min_b, max_b = map(int, budget_input.replace(" ", "").split("-"))
        codes = []
        budget_map = {
            (0, 1000): "B001", (1001, 2000): "B002", (2001, 3000): "B003",
            (3001, 4000): "B004", (4001, 5000): "B005", (5001, 999999): "B006",
        }
        for (min_r, max_r), code in budget_map.items():
            if min_b <= max_r and max_b >= min_r:
                codes.append(code)
        return ",".join(codes)
    except:
        print("金額帯の形式が不正です。無視します。")
        return ""

# ==================== 検索（リトライ付き） ====================
def search_with_fallback(keyword, lat, lng, range_val, budget_code="", mood=""):
    base_params = {
        "key": API_KEY, "lat": lat, "lng": lng,
        "range": range_val, "order": 4, "count": 10, "format": "json"
    }

    mood_kw = MOOD_KEYWORDS.get(mood, mood) if mood else ""
    full_keyword = f"{keyword} {mood_kw}".strip()

    trials = [
        {"keyword": full_keyword, "budget": budget_code},
        {"keyword": keyword, "budget": budget_code},
        {"keyword": full_keyword, "budget": ""},
        {"keyword": keyword, "budget": "", "range": min(5, range_val + 1)},
        {"keyword": keyword, "budget": "", "range": min(5, range_val + 2)},
        {"keyword": "ランチ", "lat": 35.6812, "lng": 139.7671, "range": 3, "budget": ""},
    ]

    for i, mod in enumerate(trials):
        params = base_params.copy()
        params.update(mod)
        if "keyword" in mod:
            params["keyword"] = mod["keyword"]

        dist_km = {1:0.3, 2:0.5, 3:1, 4:2, 5:3}.get(params.get("range", 3), 3)
        print(f"  試行 {i+1}: '{params['keyword']}' | {dist_km}km以内")

        try:
            r = requests.get(URL, params=params, timeout=15)
            if r.status_code != 200: continue
            data = r.json()
            results = data.get("results", {})
            if "error" in results: continue
            shops = results.get("shop", [])
            if shops:
                print(f"    → {len(shops)}件ヒット！")
                return shops, params
        except:
            continue
    return [], {}

# ==================== メイン ====================
def main():
    print("=== 気分でランチ探し（距離は自動！） ===")
    
    keyword = input("場所を入力（例: 渋谷, 東京駅）: ").strip()
    if not keyword:
        keyword = "東京駅"

    budget_input = input("金額帯（例: 1000-3000, 空欄=無制限）: ").strip()
    mood = input("あなたの気分は？（例: ガッツリ, さっぱり）: ").strip()

    print(f"
「{keyword}」を検索中...")
    lat, lng, place_name = get_lat_lng(keyword)
    if not lat:
        print("場所が見つかりません。東京駅を基準にします。")
        lat, lng = 35.6812, 139.7671
        place_name = "東京駅"

    # 距離自動決定
    range_val = auto_range(lat, lng, place_name)
    dist_km = {1:0.3, 2:0.5, 3:1, 4:2, 5:3}.get(range_val, 3)
    print(f"→ 自動距離: {dist_km}km以内（{place_name}基準）")

    budget_code = get_budget_code(budget_input)

    print(f"
検索開始...")
    shops, used_params = search_with_fallback(
        keyword=keyword, lat=lat, lng=lng,
        range_val=range_val, budget_code=budget_code, mood=mood
    )

    if not shops:
        print("
該当なし... 明日またトライ！")
        return

    # 結果表示
    used_range = used_params.get("range", range_val)
    final_dist = {1:0.3, 2:0.5, 3:1, 4:2, 5:3}.get(used_range, 3)
    print(f"
{'='*50}")
    print(f"  結果: {len(shops)}件 | 距離: {final_dist}km以内")
    print(f"  場所: {keyword} | 気分: {mood or 'なし'}")
    print(f"{'='*50}")

    for i, shop in enumerate(shops, 1):
        name = shop.get("name", "不明")
        genre = shop.get("genre", {}).get("name", "不明")
        budget = shop.get("budget", {}).get("average", "不明")
        address = shop.get("address", "")
        distance = shop.get("distance", "不明")
        url = shop.get("urls", {}).get("pc", "")

        match_tag = ""
        if mood:
            text = f"{name} {genre}".lower()
            if mood.lower() in text:
                match_tag = " 完璧マッチ！"
            elif any(k in text for k in mood.lower().split()):
                match_tag = " 合いそう"

        print(f"
{i}. {name}{match_tag}")
        print(f"   ジャンル: {genre} | 予算: {budget}")
        print(f"   住所: {address} | 距離: {distance}m")
        if url:
            print(f"   詳細: {url}")

# ==================== 実行 ====================
if __name__ == "__main__":
    main()
```