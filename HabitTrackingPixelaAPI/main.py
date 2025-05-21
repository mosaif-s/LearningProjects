import requests
import datetime as dt
pixela_endpoint="https://pixe.la/v1/users"
today=dt.datetime.today()

params={
    "token":"",
    "username":"mosaif",
    "agreeTermsOfService":"yes",
    "notMinor":"yes",
}
username=params["username"]
token=params['token']
graph_endpoint=f"{pixela_endpoint}/{username}/graphs"
graph_config={
    "id":"graph1",
    "name":"Reading Graph",
    "unit":"minutes",
    "type":"float",
    "color":"sora",
}
headers={
    "X-USER-TOKEN": token
}
add_pixel_endpoint=f"{pixela_endpoint}/{username}/graphs/{graph_config['id']}"

#Adding a pixel every day its run
pixel_config={
    "date":today.strftime("%Y%m%d"),
    "quantity":input("How many minutes did you read today? "),
}
response=requests.post(url=add_pixel_endpoint, json=pixel_config, headers=headers)
print(response.text)


#Adding A Graph
# response=requests.post(url=graph_endpoint, json=graph_config, headers=headers)


#Updating Pixel
# response=requests.put(url=add_pixel_endpoint+"/"+pixel_config['date'],json={"quantity":str(75),}, headers=headers)
# print(response.text)
