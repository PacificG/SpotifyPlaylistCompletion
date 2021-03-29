
import os
import json
import pandas as pd
import csv
class Dataset:
    track_uri2id = {}
    track_id2uri = {}
    track_id2aauri = {}
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
                    for track in playlist['tracks']:
                        track_uri, album_uri, artist_uri = track['track_uri'], track['album_uri'], track['artist_uri']
                        if track_uri not in self.track_uri2id:
                            trackid += 1
                            self.track_uri2id[track_uri] = trackid
                            self.track_id2uri[trackid] = (track_uri, track['track_name'])
                            if album_uri not in self.albums_uri2id:
                                albumid += 1
                                self.albums_uri2id[album_uri] = (albumid, track['album_name'])
                            
                            if artist_uri not in self.artists_uri2id:
                                artistid += 1
                                self.artists_uri2id[artist_uri] = (artistid, track['artist_name'])

                        self.track_id2aauri[self.track_uri2id[track_uri]] = (album_uri, artist_uri)

    def playlist_gen(self):
        for file in self.files:
            for playlist in self.files[file]['playlists']:
                this_playlist = {}
                this_playlist['pid'] = playlist['pid']
                this_playlist['tracks'] = [self.track_uri2id[track['track_uri']] for track in playlist['tracks']]

                yield this_playlist

    
    def trackName4tid(self, track_id):
        return self.track_id2uri[track_id][1]

    def albumName4tid(self, track_id):
        return self.albums_uri2id[self.track_id2aauri[track_id][0]][1]

    def artistName4tid(self, track_id):
        return self.artists_uri2id[self.track_id2aauri[track_id][1]][1]
                    
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
    
    
