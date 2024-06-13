import infra, building

import pandas


network_df = pandas.read_csv("./data/reseau_en_arbre.csv").drop_duplicates()

def prepare_data(network_df):
    network_df = network_df[network_df["infra_type"] != "infra_intacte"]

    infra_subdfs = network_df.groupby(by="infra_id")
    dict_infras = {}
    for infra_id, infra_subdf in infra_subdfs:
        length = infra_subdf["longueur"].iloc[0]
        infra_type = infra_subdf["infra_type"].iloc[0]
        nb_houses = sum(infra_subdf["nb_maisons"].values)
        dict_infras[infra_id] = infra.Infra(infra_id, length, infra_type, nb_houses)

    building_subdfs = network_df.groupby(by= "id_batiment")
    list_buildings = []
    for building_id, building_subdf in building_subdfs:
        list_infras = [dict_infras[infra_id] for infra_id in building_subdf["infra_id"].values]
        list_buildings.append(building.Building(building_id, list_infras))

    return dict_infras, list_buildings

 
def plannification(dict_infra, list_building):
    list_sorted_buildings = []
    
    while list_buildings:
        easiest_building = min(list_buildings)
        list_sorted_buildings.append(easiest_building)
        for infra in easiest_building.list_infras:
            infra.repair_infra()
        list_buildings.remove(easiest_building)
    
    return list_sorted_buildings

if __name__ == "__main__":
    dict_infras, list_buildings = prepare_data(network_df)

    list_sorted_buildings = plannification(dict_infras, list_buildings)

    priority_list, building_ids = [], []
    for index, building in enumerate(list_sorted_buildings):
        priority_list.append(index)
        building_ids.append(building.id_building)

    pandas.DataFrame({"priority" : priority_list, "id_bat": building_ids}).to_excel("./priorities_restructred.xlsx", index=False)