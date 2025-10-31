import random

# 名前入力
player_name = input("チャレンジャーの名前を教えてね: ")
if not player_name:
    player_name = "名無し"

# じゃんけんの手
list1 = ["グー", "チョキ", "パー"]
# 方向
list2 = ["上", "下", "左", "右"]

# じゃんけん
def janken():
    print("\n最初はグー、じゃんけん…")
    while True:
        player = input(f"{player_name}の手（グー/チョキ/パー）: ")
        if player not in list1:
            print("グー、チョキ、パーのどれかを入力してね！")
            continue
        com = random.choice(list1)
        print(f"{player_name}: {player} | 相手: {com}")  
        
        if player == com:
            print("あいこで…")
        else:
            break  # 勝敗決着
    
    # 勝ち負け判定
    if (player == "グー" and com == "チョキ") or \
       (player == "チョキ" and com == "パー") or \
       (player == "パー" and com == "グー"):
        return "player"
    else:
        return "cpu"

# あっち向いてホイ
def acchimuitehoi(winner):
    print("\nあっち向いて…")
    
    if winner == "player":
        while True:
            player_dir = input(f"{player_name}が指をさす方向（上/下/左/右）: ")
            if player_dir in list2:
                break
            print("上/下/左/右 から入力してね！")
        com_dir = random.choice(list2)
    else:

        while True:
            player_dir = input(f"{player_name}が顔を向ける方向（上/下/左/右）: ")
            if player_dir in list2:
                break
            print("上/下/左/右 から入力してね！")
        com_dir = random.choice(list2)
        print(f"相手が指をさす: {com_dir}")
    
    print(f"あなた: {player_dir} | 相手: {com_dir}")
    return player_dir == com_dir

# === メインゲーム ===
print("\nあっち向いてホイ 連勝チャレンジ！")
print("何回連続で勝ち続けられるかな？？\n")

score = 0  # 連勝数

while True:
    winner = janken()
    
    if acchimuitehoi(winner):
        if winner == "player":
            score += 1
            print(f"\n{score}連勝！次も勝つぞ{player_name}!")
            print("次の相手が現れた…！\n")
        else:
            print(f"\n{score}連勝で終了！よく頑張ったね、{player_name}!")
            break
    else:
        print("外れた！じゃんけんからやり直しだ！\n")

print(f"\n最終連勝数: {score} 連勝！")
print(f"諦めたらそこで終了ですよ、{player_name}!")