import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.test.utils import datapath
from gensim import utils
from gensim.parsing.preprocessing import preprocess_string, preprocess_documents

class Corpus:
    def __init__(self, dataset, vec2get):
        self.dataset = dataset
        if vec2get == "track":
            self.fn = self.dataset.trackName4tid
        elif vec2get == "album":
            self.fn = self.dataset.albumName4tid
        elif vec2get == "artist":
            self.fn = self.dataset.artistName4tid

    def __iter__(self):
        play_gen = self.dataset.playlist_gen()
        for playlist in play_gen:
            for track_id in playlist['tracks']:
                self.fn(track_id).split(" ")
            
def word2vectors(dataset):
    tracks = Corpus(dataset, 'track')
    tracksmodel = gensim.models.Word2Vec(sentences=tracks, sg=1, min_count = 1, size=100, window=5,
                                       alpha=0.025 , min_alpha=0.0001 ,workers=2)
    gen = dataset.playlist_gen()
    track2vec = {track_id: sum([tracksmodel.wv[word] for word in dataset.trackName4tid(track_id).split(" ")]) for track_id in playlist['tracks'] for playlist in gen}

    artists = Corpus(dataset, 'artist')
    artistsmodel = gensim.models.Word2Vec(sentences=artists, sg=1, min_count=1, size=100, window=5, alpha=0.025, min_alpha=0.0001, workers=2)
    gen = dataset.playlist_gen()
    artist2vec = {track_id: sum([artistsmodel.wv[word] for word in dataset.trackName4tid(track_id).split(" ")]) for track_id in playlist['tracks'] for playlist in gen}

    albums = Corpus(dataset, 'album')
    albumsmodel = gensim.models.Word2Vec(sentences=albums, sg=1, min_count=1, size=100, window=5, alpha=0.025, min_alpha=0.0001, workers=2)
    gen = dataset.playlist_gen()
    album2vec = {track_id: sum([albumsmodel.wv[word] for word in dataset.trackName4tid(track_id).split(" ")]) for track_id in playlist['tracks'] for playlist in gen}

    return track2vec, album2vec, artist2vec


def title2rec(track2vec):
    pass
    
