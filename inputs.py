import gensim
import numpy as np
from sklearn.cluster import KMeans
import fasttext

path = '/content/drive/MyDrive/workspace/PlaylistCompletion/'

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
                yield self.fn(track_id).split(" ")
            
def word2vectors(dataset):
    tracks = Corpus(dataset, 'track')
    tracksmodel = gensim.models.Word2Vec(sentences=tracks, sg=1, min_count = 1, size=100, window=5, alpha=0.025 , min_alpha=0.0001 ,workers=2)
    gen = dataset.playlist_gen()
    track2vec = {}
    for playlist in gen:
        for track_id in playlist['tracks']:
            if track_id not in track2vec:
                track2vec[track_id] = sum([tracksmodel.wv[word] for word in dataset.trackName4tid(track_id).split(" ")])

                
    artists = Corpus(dataset, 'artist')
    artistsmodel = gensim.models.Word2Vec(sentences=artists, sg=1, min_count=1, size=100, window=5, alpha=0.025, min_alpha=0.0001, workers=2)
    gen = dataset.playlist_gen()
    artist2vec = {}

    for playlist in gen:
        for track_id in playlist['tracks']:
            if track_id not in artist2vec:
                artist2vec[track_id] = sum([artistsmodel.wv[word] for word in dataset.artistName4tid(track_id).split(" ")])


    albums = Corpus(dataset, 'album')
    albumsmodel = gensim.models.Word2Vec(sentences=albums, sg=1, min_count=1, size=100, window=5, alpha=0.025, min_alpha=0.0001, workers=2)
    gen = dataset.playlist_gen()
    album2vec = {}
    for playlist in gen:
        for track_id in playlist['tracks']:
            if track_id not in album2vec:
                album2vec[track_id] = sum([albumsmodel.wv[word] for word in dataset.albumName4tid(track_id).split(" ")])
                

    return track2vec, album2vec, artist2vec


def textfast(file_path):
    fastmodel = fasttext.train_unsupervised(file_path, model='skipgram', lr=0.1, epoch=5, loss='softmax', ws=5)
    return fastmodel
    

def title2rec(track2vec, dataset, n_clusters=500,load=False):
    if not load:
        gen = dataset.playlist_gen()
        playlist2vec = {}
        for playlist in gen:
            playlist2vec[playlist['pid']] = [playlist['title'], np.mean([track2vec[track_id] for track_id in playlist['tracks']],axis=0)]
        X = np.array([playlist2vec[pid][1] for pid in playlist2vec])
        kmeans = KMeans(n_clusters=10, random_state=0).fit(X)
        clusters = kmeans.predict(X)
        clstr = iter(clusters)
        for pid in playlist2vec:
            playlist2vec[pid].append(next(clstr))
        clustertext = {c:'' for c in set(clusters)}
        for pid in playlist2vec:
            clustertext[playlist2vec[pid][2]] += (" "+ playlist2vec[pid][0])
        f = open(f"{path}/text.txt", 'w')
        for id in clustertext:
            print(clustertext[id])
            f.write(clustertext[id]+ "\n")
        f.close()
    model = textfast(f"{path}/text.txt")
    
        
    return model
     


    
    
    

        
    
