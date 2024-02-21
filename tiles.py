import csv

from pyllist import dllist


class Tiles:
    """A class to manage tiles"""
    def __init__(self):
        self.tiles = dllist()
        self._csv_to_tiles()
        self.order_tiles()


    def _csv_to_tiles(self):
        with open("tile_structure.csv") as file:
            csv_reader = csv.reader(file, delimiter=",")
            line_count = 0
            column_count = 0

            tiles = dllist()
            for row in csv_reader:
                if line_count % 2:
                    row = reversed(row)
                for i in row:
                    tiles.appendleft({
                        "position":int(i),
                        "players_on_tile":[],
                        "on_step_move_to":0,
                        "cordinates":[],
                    })
                    column_count=column_count+1

                if column_count==10:
                    line_count=line_count+1
                    column_count=0

            self.tiles = tiles

    def order_tiles(self):
            line_count=0
            column_count=0

            for tile in reversed(self.tiles):
                if line_count % 2 == 0:
                    tile['cordinates'] = [40+column_count*45,40+line_count*45]
                    column_count=column_count+1
                else:
                    tile['cordinates'] = [40+(9-column_count)*45,40+line_count*45]
                    column_count=column_count+1

                if column_count==10:
                    line_count=line_count+1
                    column_count=0

    def order_positions(self):
        for i, tile in enumerate(self.tiles):

            tile['position'] = i+1

    def add_tile(self, pos):
        if self.tiles:
            self.tiles.insert({
                "position":f"{pos+1} *",
                "players_on_tile":[],
                "on_step_move_to":0,
                "cordinates":[],
            },self.tiles.nodeat(pos))
        else:
            self.tiles.appendright({
                "position":f"{pos+1} *",
                "players_on_tile":[],
                "on_step_move_to":0,
                "cordinates":[],
            })

    def delete_tile(self,pos):
        self.tiles.remove(self.tiles.nodeat(int(pos)))

    def clear_tiles(self):
        while self.tiles:
            self.tiles.pop()

    def add_snakes_and_ladders(self, pos1, pos2, rand=False):
        if rand==False:
            self.tiles[pos1-1]['on_step_move_to'] = self.tiles[pos2-1]['position']
        else:
            for i in range(1,int(len(self.tiles)/6)):
                self.tiles[random.randint(3,len(self.tiles)-5)]['on_step_move_to'] = random.randint(3,len(self.tiles)-2)

