import predictions.predictions as pre
pred = pre.PREVISOES()
import json

def get_data():
    with open('./backend_info/file_info/indices_by_temp.json') as user_file:
        return json.loads(user_file.read())


def get_severity(city):
    for district in get_data():
        if city == district["district"]:
            data_to_send = district["data"]
            data_to_send.append(pred.vegetacao(district["district"]))
            return pred.static_previsoes(data_to_send)
    return 0
