import constants as API
import requests
import json
import update_github

def connect():
    try:
        respone = requests.get(API.RADIO_URL)
        if(respone.ok):
            data = respone.json()
            return data['data']
        else:
            return {'list':[]}
    except:
        return {'list':[]}

def get_india(list_array):
    output_dict = [item for item in list_array if item['country'] == 'India' or item['country'] == 'Sri Lanka']
    output_json = json.dumps({'list':output_dict}, indent=4, sort_keys=True)
    return output_json

if __name__ == "__main__":
    response = connect()
    radio_list = response['list']
    if radio_list.__len__() > 0:
        india_list = get_india(radio_list)
        update = update_github.UpdateGithub()
        update.update_github(india_list)
        print('File updated...')
    else:
        print('Empty Response')
    