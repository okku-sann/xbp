import random

list=["グー","チョキ","パー"]
#playerの出す手を決める
player = input("あなた：")
#comの出す手を決める
com = random.choice(list)
print("相手:{}".format(com))

if player == com:
    print("あいこ")

