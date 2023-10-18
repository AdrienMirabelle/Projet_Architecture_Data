from googleapiclient.discovery import build

# Remplacez ces valeurs par les vôtres
API_KEY = "AIzaSyA-u35TFgqq6kNfy5-CdJ3Pzt_zQgLnq2w"

# Créez une instance de l'API YouTube Data
youtube = build("youtube", "v3", developerKey=API_KEY)

# Utilisez la méthode search.list pour obtenir les dernières vidéos
search_response = youtube.search().list(
    q="",
    type="video",
    part="id",
    maxResults=10,
    order="date"  # Triez par date pour obtenir les vidéos les plus récentes
).execute()
print(search_response)


# Parcourez les résultats et imprimez les titres des vidéos
for search_result in search_response.get("items", []):
    if 'videoId' in search_result['id']:
        video_id = search_result['id']['videoId']
        video_info = youtube.videos().list(part="snippet", id=video_id).execute()
        if 'items' in video_info:
            video = video_info['items'][0]
            title = video['snippet']['title']
            print("Titre de la vidéo :", title)

