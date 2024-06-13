class Building:
    def __init__(self, id_building, list_infras):
        self.id_building = id_building
        self.list_infras = list_infras

    def get_building_difficulty(self):

        return sum(self.list_infras)

    def __lt__(self, other_building):

        return self.get_building_difficulty() < other_building.get_building_difficulty()

    def __repr__(self):
        return f"object Building - id : {self.id_building}"