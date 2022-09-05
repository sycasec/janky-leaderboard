import requests
from datetime import datetime
import os

ape_key = "NjMxNDRmOWI1MGQ0OTQ3N2NlY2UxN2QyLnlXbGQ1MHU2M1hJR3lKdTU1aVFtZHUxMEJoVHVUdTlX"
base_url = "https://api.monkeytype.com"
headers = {'Authorization': 'ApeKey '+ape_key, 'Accept': "application/json"}

def parse_args(arg: str):
	if "player" in arg:
		return 1

	elif arg == "show lb":
		return 2

	elif arg == "help":
		return 3

	elif arg == "reinit lb":
		return 4

	elif arg == "exit":
		return 0

def reinit_lb():
	file_path = "leaderboard.txt"
	if os.path.isfile(file_path):
	 	os.remove(file_path)


def read_from_file():
	lb = {}
	with open("leaderboard.txt", "r") as f:
		for line in f:
			data = line.split("##")
			if (data[0] in lb.keys()) and (data[1] < lb[data[0]]['wpm']):
					continue
			lb[data[0]] = {'wpm': data[1], 'raw': data[2], 'acc': data[3], 'ts': data[4].strip('\n')}

	return lb

def save_to_file(name, wpm, raw, acc, ts):
	with open("leaderboard.txt", "a+") as f:
		f.write(str(name) + "##" + wpm + "##" + raw + "##" + acc + "##" + ts +'\n')

def get_score():
	with requests.Session() as s:
		r = s.get(base_url+'/results/last', headers=headers)
		wpm = r.json()['data']['wpm']
		raw_wpm = r.json()['data']['rawWpm']
		acc = r.json()['data']['acc']
		ts = r.json()['data']['timestamp']


	return [wpm, raw_wpm, acc, ts]

def get_wpm(item):
	return float(item[1]['wpm'])

def display_leaderboard():
	lb = read_from_file()
	print(f"\t------------------------------------------------------------------------")
	print(f"\t rank |  name     |   wpm      raw       acc            time          ")
	rank = 1
	ws = '  '
	for entry in sorted(lb.items(), key=get_wpm, reverse=True):
		name = entry[0]
		if len(name) < 7:
			name += " " * (7 - len(name))
		elif len(name) > 7:
			name = name[:4]
			name += "..."
		wpm = float(entry[1]['wpm'])
		raw = float(entry[1]['raw'])
		acc = float(entry[1]['acc'])
		ts = datetime.fromtimestamp(int(entry[1]['ts'])/1000)
		if rank >= 10: ws = ' '
		print(f"\t  {rank} {ws}|  {name}   :   {wpm:.2f}{' '*3 if wpm > 99.99 else ' '*4}{raw:.2f}{' '*3 if raw > 99.99 else ' '*4}{acc:.2f}%{' '*3 if acc < 100 else '  '}{ts}")
		rank = rank + 1
	print(f"\t------------------------------------------------------------------------")

def show_help():
	print("monkeytype janky leaderboard\n - type with 15 seconds first, then enter 'player PLAYER_NAME' to store score")
	print("\n - enter 'show lb' to show leaderboard\n - enter 'help' to show this message\n - enter 'exit' to end program.")
	print("\n -- IMPORTANT !!! --\n do not exit before saving your score! loss of data is not the problem of csg :D")

def main():
	print(" -- Janky Monkeytype Terminal Leaderboard [JMTL] --\n - type 'player PLAYER_NAME' to save your score!\n\n --- UPDATE!!!! ---\n4 character limit is lifted!!")
	print("\n - you can now type in a max of 15 chars for name,\nbut display is limited to 6")

	while(True):
		arg = input("Enter command\n> ")
		comm = parse_args(arg)
		if comm == 1:
			name = arg.split(" ")[1]
			if len(name) > 15:
				print("\nthat name is too long!")
				continue
			data = get_score()
			data = [str(item) for item in data]
			save_to_file(name, data[0], data[1], data[2], data[3])
			display_leaderboard()

		elif comm == 2:
			display_leaderboard()

		elif comm == 3:
			show_help()

		elif comm == 4:
			reinit_lb()

		elif comm == 0:
			return

if __name__ == '__main__':
	main()
