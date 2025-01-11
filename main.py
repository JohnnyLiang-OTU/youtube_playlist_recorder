from yt_dlp import YoutubeDL
import json
import sys

# Class that represents a VideoEntry by the index, title and idd (id of video)
class VideoEntry():
    def __init__(self, index, title, idd):
        self.index = index
        self.title = title
        
        # idd instead of id because id is already a python function. 
        # I want to avoid any problems with naming in the future
        self.idd = idd 

    def dict_form(self):
        return {
            'index': self.index,
            'title': self.title,
            'idd': self.idd
        }

    def __str__(self):
        return f"{self.index}. {self.title};{self.idd}"
    
    def get_index(self):
        return self.index
    
    def get_title(self):
        return self.title
    
    def get_idd(self):
        return self.idd


def get_playlist_title(playlist_url):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        return info.get('title', 'Title Not Found')


def get_playlist_entries(playlist_url):
    yld_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    
    with YoutubeDL(yld_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if 'entries' in info:
            return [
                {
                    'title': entry['title'],
                    'idd': entry['id'],
                }
                for entry in info['entries']]
            
        return []

'''
Core function of the code.

Arguments: 
    url : The url of the playlist

Returns:
    Nothing.

Uses yt-dlp to "scrap" the metadata of a playlist. 
Takes the entries of the playlist and makes VideoEntry objects.
Dictionary-fies the VideoEntry objects.
Creates a Json with title and an arary of Dictionary-fied VideoEntrys
Dumps into a txt file.
'''
def record_playlist(url):
    title_of_playlist = get_playlist_title(url)
    title_of_playlist = title_of_playlist.replace(' ', '') # Remove spaces
    
    video_titles = get_playlist_entries(url)
    
    
    # Make dict for every index, title
    '''
    Example:
        {
            'index': 2,
            'title': 'Li Bai',
            'id': 'xbwqkqv5ljo'
        }
    '''
    video_titles = [VideoEntry(index, title_idd['title'], title_idd['idd']).dict_form() for index, title_idd in enumerate(video_titles, 1)]
    
    json_body = {
        'playlist_title': title_of_playlist,
        'videos': video_titles
    }
    
    
    
    with open(file=f'{title_of_playlist}.json', mode='w', encoding='utf-8') as f:
        json.dump(json_body, f, ensure_ascii=False, indent=4)
    
    return

def workspace():
    url = "url.example"
    try:
        title_of_playlist = get_playlist_title(url)
    except:
        print("Not a valid youtube URL. Exiting...")
        sys.exit(1)
    
    title_of_playlist = title_of_playlist.replace(' ', '') # Remove spaces
    video_titles = get_playlist_entries(url)
    
    
    # Make dict for every index, title
    '''
    Example:
        {
            'index': 2,
            'title': 'Li Bai',
            'id': 'xbwqkqv5ljo'
        }
    '''
    video_titles = [VideoEntry(index, title_idd['title'], title_idd['idd']).dict_form() for index, title_idd in enumerate(video_titles, 1)]
    
    json_body = {
        'playlist_title': title_of_playlist,
        'videos': video_titles[:5]
    }
    
    print(json_body)
    
    return



'''
Core function of the code.

Arguments:
    url : The url of the playlist.
    
Returns:
    ...
    
Uses yt-dlp to "scrap" the title and entries of the playlist.
For every entry:
    scrap the title and id.
Make 


Check for titles == '[Private video]'

Check for idds not found in the current but are recorded.

'''
def compare_playlist(url):
    playlist_title = get_playlist_title(url)        
    playlist_entries = get_playlist_entries(url)
    
    file = open(f'{playlist_title}.json', 'r', encoding='utf-8')

    data = json.load(file)
    file.close()
    
    recorded_idds = {item['idd'] for item in data['videos']}
    current_idds = {item['idd'] for item in playlist_entries}
    
    # Based on missing IDS
    missing_idds = recorded_idds - current_idds
    missing_videos = [item['title'] for item in data['videos'] if item['idd'] in missing_idds]
    
    if missing_videos:
        print("\nThe missing videos are:")
        for title in missing_videos:
            print(title)
    else:
        print("\nThe Playlist has no missing videos.")
        
    # Based on Private Video
    private_idds = [item['idd'] for item in playlist_entries if item['title'] == '[Private video]']
    private_videos = missing_videos = [item['title'] for item in data['videos'] if item['idd'] in private_idds]
    if private_videos:
        print("\nThe Private Videos' idds are: ")
        for title in private_videos:
            print(title)
    else:
        print("\nNo Private'd video")
    
    
    
    

def main():
    options = [
        "1. Record a Playlist into json.",
        "2. Compare Playlists."
        
    ]
    
    print("------------------------------------------------------------")
    print("JohnL welcomes you.")
    
    url = input("\nEnter the URL: ")
    
    try:
        playlist_title = get_playlist_title(url)
    except:
        print("Not a valid youtube URL. Exiting...")
        sys.exit(1)
    
    for option in options:
        print(option)
        
    user_choice = input("Select your option: ")
    
    match user_choice:
        case '1': # Record
            record_playlist(url)
        
        case '2': # Compare
            compare_playlist(url)

if __name__ == '__main__':
    main()
    # workspace()

