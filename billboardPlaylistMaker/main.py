import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date=input("Which year do you want to travel to? Type te date in this format YYYY-MM-DD: ")
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
}
url=f"https://www.billboard.com/charts/hot-100/{date}"
response=requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find all <h3> tags with id="title-of-a-story"
# titles = soup.find_all("h3", {
#     "id": "title-of-a-story",
#     "class": "c-title"
# })
# new_titles=[]
# values_to_remove = [
#     'Songwriter(s):',
#     'Producer(s):',
#     'Imprint/Promotion Label:',
#     'Gains in Weekly Performance',
#     'Additional Awards'
# ]
# for i in range(len(titles)):
#     new_titles.append(titles[i].text.strip())
#
#
# new_titles1=[item for item in new_titles if item not in values_to_remove]
#
# print(new_titles1)

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
print(song_names)
print("\n")
print("Started processing songs....")


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="4e85c381fb584b059e36c3b736c101e7",
    client_secret="1a531a06b46b4d9aa607a3dbcfd33b72",
    redirect_uri="https://example.com",
    scope="playlist-modify-public"
))

user_id = sp.current_user()['id']
# print(user_id)  # Your Spotify username (unique ID, not display name)
# track_name=song_names[0]
# results = sp.search(q=track_name, type="track", limit=1)
# track_uri = results["tracks"]["items"][0]["uri"]
spotify_uris=[]
unfound_tracks=[]
c=0
for name in song_names:
    # c=c+1
    # if c==10:
    #     break
    try:
        q1=(f"track:{name} year:{date[0:4]}")
        result=sp.search(q=name, type="track", limit=1)
        track_uri=result["tracks"]["items"][0]["uri"]
        spotify_uris.append(track_uri)
    except:
        unfound_tracks.append((name))
        print("Not found:"+ " "+ name)

playlist = sp.user_playlist_create(user=user_id, name=f"Billboard {date}", public=True, collaborative=False, description="")
sp.playlist_add_items(playlist_id=playlist['id'], items=spotify_uris)

print("Playlist Created with the name Billboard "+date)
if len(unfound_tracks)!=0:
    print(f"Following Playlists were not found:\n")
    for name in unfound_tracks:
        print(name + "\n")

