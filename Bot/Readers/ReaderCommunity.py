from Bot.Readers.misc import change_dir
from Bot.Readers.readerCard import find_card
# Working


class ReaderCommunity:
    def __init__(self, ID):

        self.Flop = []
        self.Turn = []
        self.River = []

        if ID == 0:
            self.com1region = (342, 260, 30, 40)
            self.com2region = (400, 260, 30, 40)
            self.com3region = (459, 260, 30, 40)
            self.com4region = (517, 260, 30, 40)
            self.com5region = (576, 260, 30, 40)

            self.com1suitRegion = (367, 261, 50, 50)
            self.com2suitRegion = (424, 261, 50, 50)
            self.com3suitRegion = (484, 261, 50, 50)
            self.com4suitRegion = (540, 261, 50, 50)
            self.com5suitRegion = (600, 261, 50, 50)

        elif ID == 1:

            self.com1region = (342, 260, 30, 40)
            self.com2region = (400, 260, 30, 40)
            self.com3region = (459, 260, 30, 40)
            self.com4region = (517, 260, 30, 40)
            self.com5region = (576, 260, 30, 40)

            self.com1suitRegion = (367, 261, 50, 50)
            self.com2suitRegion = (424, 261, 50, 50)
            self.com3suitRegion = (484, 261, 50, 50)
            self.com4suitRegion = (540, 261, 50, 50)
            self.com5suitRegion = (600, 261, 50, 50)




    def ReadFlop(self):
        change_dir("cards")

        _, card = find_card(self.com1region, self.com1suitRegion)
        self.Flop.append(card)
        _, card = find_card(self.com2region, self.com2suitRegion)
        self.Flop.append(card)
        _, card = find_card(self.com3region, self.com3suitRegion)
        self.Flop.append(card)
        st = ""
        for c in self.Flop:
            st += str(c) + " "
        print("Flop: " + str(st))

    def ReadTurn(self):
        change_dir("cards")

        print("Finding turn card")
        _, card = find_card(self.com4region, self.com4suitRegion)
        self.Turn.append(card)
        print("Turn: " + str(card))



    def ReadRiver(self):
        change_dir("cards")

        print("finding river card")
        _, card = find_card(self.com5region, self.com5suitRegion)
        self.River.append(card)
        print("River: " + str(card))


if __name__ == "__main__":
    import time
    time.sleep(1)
    R = ReaderCommunity(ID=0)
    R.ReadRiver()

