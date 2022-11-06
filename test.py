import csv
from pyllist import dllist

def csv_to_tiles(src):
	with open(src) as file:
		csv_reader = csv.reader(file, delimiter=",")
		line_count = 0
		column_count = 0

		

		tiles = dllist()
		for row in csv_reader:
			if line_count % 2 or line_count==0:
				row = reversed(row)
			for i in row:
				tiles.appendleft({
					"position":i,
					"players_on_tile":[],
					"on_step_move_to":False,
					"cordinates":[40+column_count*45,40+line_count*45],
				})
				column_count=column_count+1
			
			if column_count==10:
				line_count=line_count+1
				column_count=0
	

		return tiles

tiles = dllist()
tiles.appendleft({
	"position":1,
	"players_on_tile":[],
	"on_step_move_to":False,
	"cordinates":[40*45,4*45],
})
tiles.appendleft({
	"position":2,
	"players_on_tile":[],
	"on_step_move_to":23,
	"cordinates":[40*45,4*45],
})
tiles.appendleft({
	"position":3,
	"players_on_tile":[],
	"on_step_move_to":24,
	"cordinates":[40*45,4*45],
})


tiles[2]['players_on_tile'].append('player1')
print(tiles[2])

print(tiles[2].index)