import sqlite3
import random
import time

mspeed = 0.6 # 会話スピード
meslst = {
	"11":[
		"%name%さんが好き"
	],
	"12":[
		"%name%さんが嫌い"
	],
	"21":[
		"%name%が食べたい"
	],
	"22":[
		"%name%が食べたくない"
	],
}

def message_main(r):
	res = random.choice(meslst[ str(r[2]) + str(r[3]) ])
	return res.replace("%name%", r[1])

conn = sqlite3.connect('words.sqlite3')
c = conn.cursor()
c.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='words'")
if c.fetchone()[0] == 0:
	c.execute('create table words(id integer primary key, word text, type integer, like integer)')

while(1):
	# 言葉を覚えるフェイズ
	print("言葉をおしえて！（人、食べ物、場所がいいなぁ…）")
	str1 = input()
	time.sleep(mspeed)

	while(1):
		print("それは、'人'？、'食べ物'？、それとも'場所'？")
		str2 = input()
		time.sleep(mspeed)
		if(str2 not in {"人", "食べ物", "場所"}):
			print("言っていることが分かりません。")
			time.sleep(mspeed)
			print("もう一回たずねるよ？")
			time.sleep(mspeed)
			continue
		break

	while(1):
		print("あなたは、それが'好き'？、それとも'嫌い'？")
		str3 = input()
		time.sleep(mspeed)
		if(str3 not in {"好き", "嫌い"}):
			print("言っていることが分かりません。")
			time.sleep(mspeed)
			print("もう一回たずねるよ？")
			time.sleep(mspeed)
			continue
		break

	print("そうなんだ。言葉を教えてくれてありがとう！")
	time.sleep(mspeed)

	isql = 'insert into words (word, type, like) values (?, ?, ?)'
	p3 = 1 # 好き
	if str3 == "嫌い": p3 = 2
	p2 = 1 # 人
	if str2 == "食べ物": p2 = 2
	if str2 == "場所": p2 = 3
	#print(p2)
	#print(p3)
	para = [(str1, p2, p3)]
	c.executemany(isql, para)
	conn.commit()
	print("----") # ひと区切り

	# 会話をするフェイズ
	time.sleep(mspeed)
	sql = 'SELECT count(*) FROM ' + 'words'
	#SQLを実行し、レコード数を得る
	c.execute(sql)
	res = c.fetchall()
	if(res[0][0] > 0):
		sql = 'SELECT * FROM words ORDER BY RANDOM() LIMIT 1'
		c.execute(sql)
		res = c.fetchall()
		mes = message_main(res[0])
		print(mes)


