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

def save_to_file(name, wpm, raw, acc, ts):
	with open("leaderboard.txt", "a") as f:
		f.write(str(name) + "##" + wpm + "##" + raw + "##" + acc + "##" + ts +'\n')

def read_from_file():
	lb = {}
	with open("leaderboard.txt", "r") as f:
		for line in f:
			data = line.split("##")
			# print(data)
			lb[data[0]] = {'wpm': data[1], 'raw': data[2], 'acc': data[3], 'ts': data[4].strip('\n')}

	return lb

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
	print(f"\t--------------------------------------------------------------------")
	print(f"\t#|  name     |   wpm      raw       acc            time          ")
	rank = 1
	for entry in sorted(lb.items(), key=get_wpm, reverse=True):
		name = entry[0]
		wpm = entry[1]['wpm']
		raw = entry[1]['raw']
		acc = entry[1]['acc']
		ts = datetime.fromtimestamp(int(entry[1]['ts'])/1000)
		print(f"\t{rank}|  {name}     :   {wpm}   {raw}   {acc}%   {ts}")
		rank = rank + 1
	print(f"\t-----------------------------------------------------------------")

def show_help():
	print("monkeytype janky leaderboard\n - type with 15 seconds first, then enter 'player PLAYER_NAME' to store score")
	print("\n - enter 'show lb' to show leaderboard\n - enter 'help' to show this message\n - enter 'exit' to end program.")
	print("\n -- IMPORTANT !!! --\n do not exit before saving your score! loss of data is not the problem of csg :D")

def main():
	print(" -- Janky Monkeytype Terminal Leaderboard [JMTL] --\n - type 'player PLAYER_NAME' to save your score!\n - name must be of 4 characters!! >:(")

	while(True):
		arg = input("Enter command\n> ")
		comm = parse_args(arg)
		if comm == 1:
			name = arg.split(" ")[1]
			if len(name) != 4:
				print("\nmust be 4 chars only!!! >:(\n")
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
