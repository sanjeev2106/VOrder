import os
import cPickle
import numpy as np
import speech
from scipy.io.wavfile import read
from sklearn.mixture import GMM 
from speakerfeatures import extract_features
import warnings
warnings.filterwarnings("ignore")

class Trainer:
    #path to training data
    source   = r'C:/VOrder/sys/speaker_model/audio_clip/'
    #path where training speakers will be saved
    #dest = "speaker_models\\"
    train_file = "development_set_enroll.txt"

    def __init__(self):
        pass

    def createModel(self, destination):

        dest = destination
        file_name = dest.split('/')
        #print file_name
        file_name = file_name[-2]
        #print file_name
        wav_files = [f for f in os.listdir(Trainer.source) if f.endswith('.wav')]
        wavFileCount = len(wav_files)
        count = 1
        # Extracting features for each speaker (5 files per speakers)
        features = np.asarray(())

        for path in wav_files:
            #path = path.strip()
            #print path
            # read the audio
            sr,audio = read(Trainer.source + path)
            # extract 40 dimensional MFCC & delta MFCC features
            vector   = extract_features(audio,sr)

            if features.size == 0:
                features = vector
            else:
                features = np.vstack((features, vector))
            # when features of 5 files of speaker are concatenated, then do model training
            if count == wavFileCount:
                gmm = GMM(n_components = 16, n_iter = 200, covariance_type='diag',n_init = 3)
                gmm.fit(features)
                # dumping the trained gaussian model
                picklefile = file_name+".gmm"
                #print picklefile
                cPickle.dump(gmm,open(dest + picklefile,'w'))
                #dest = dest.split('/')
                dest = '/'.join((dest.split('/'))[-3:-1])
                with open(r"C:\VOrder\sys\speaker_model\training_models.txt", "a") as myfile:
                    myfile.write(dest+'/'+picklefile+'\n')
                for file in wav_files:
                    os.remove(Trainer.source+file)
                print 'modeling completed for speaker:',file_name
                speech.say('modeling completed for speaker:'+file_name)
                features = np.asarray(())
                count = 0
            count = count + 1

#if __name__ == '__main__':
 #   ob = Trainer()
  #  ob.createModel()
