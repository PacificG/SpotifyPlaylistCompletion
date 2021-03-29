
import os
import json
import pandas as pd
import csv
class Dataset:
    track_uri2id = {}
    track_id2uri = {}
    track_id2aa = {}
    albums_uri2id = {}
    artists_uri2id = {}
    
    def __init__(self, playlistPath):
        dirs = os.listdir(playlistPath)
        self.files = {}
        trackid, albumid, artistid = 0,0,0
        for file in dirs:
            with open(f'{playlistPath}/{file}') as f:
                self.files[file] = json.load(f)
                for playlist in self.files[file]['playlists']:
                    
    def playlistCSV(self, csvpath):
        with open(f'{csvpath}/playlist.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            names = ['name', 'collaborative','num_tracks','num_artists',
                 'num_albums','num_followers','num_edits','modified_at','duration_ms']
            writer.writerow(names)
            for file in self.files:
                for playlist in self.files[file]['playlists']:
                    writer.writerow([playlist[name] for name in names])
    def trackCSV(self, csvpath):
        with open(f'{csvpath}/track.csv','w', newline='') as f:
            writer = csv.writer(f)
            names = ['pid', 'pos','track_uri']
            writer.writerow(names)
            for file in self.files:
                for playlist in self.files[file]['playlists']:
                    for track in playlist['tracks']:
                        writer.writerow([playlist['pid'], track['pos'], track['track_uri']])
    def reader(self):
        for file in self.files:
            for playlist
            
    
