import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, TimeDistributed#, CuDNNLSTM
import numpy as np
def get_trackvec(t2v, al2v, ar2v):
    """for each track it concatenates track, album and artist embeddings to get 300dim vector"""
    trackvec = {}
    for tid in t2v:
        trackvec[tid] = np.concatenate((t2v[tid], al2v[tid], ar2v[tid]), axis=None)
    return trackvec

def train_generator(t2v, al2v, ar2v, dataset):
    """
    returns a generator object that returns train and output of dim (n_tracks-1)*300 for each playlist
    """
    gen = dataset.playlist_gen()
    trackvec = get_trackvec(t2v, al2v, ar2v)
    for playlist in gen:
        x_train = np.array([trackvec[tid] for tid in playlist['tracks'][:-1]])
        y_train = np.array([trackvec[tid] for tid in playlist['tracks'][1:]])
        yield x_train, y_train

def rnn():
    """
    compiles and returns rnn model
    """
    model = Sequential()

    model.add(LSTM(128, return_sequences=True, input_shape=(None,300)))
#    model.add(Dropout(0.2))


    model.add(TimeDistributed(Dense(32,activation='relu')))
 #   model.add(Dropout(0.2))

    model.add(TimeDistributed(Dense(1, activation='softmax')))

    opt = tf.keras.optimizers.Adam(lr=0.001)#, decay=1e-6)

    # Compile model
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=opt
    )
    return model

def recommender(seed_playlist, model):
    """
    Adds tracks to playlists till there are 500 tracks. 
    """
    while len(seed_playlist['tracks']) < 500:
        next_track_id = max([track for track in tracks if track not in seed_playlist['tracks']], key=lambda x: model.get_logits(x))
        seed_playlist['tracks'].append(next_track_id)
    return seed_playlist


