__author__ = 'WSY'
import os

class Song():
    def __init__(self, song_id, publish_time, song_init_plays, language, gender):
        self.song_id = song_id
        self.publish_time = publish_time
        self.song_init_plays = song_init_plays
        self.language = language
        self.gender = gender
        self.action = []

    def getSong_id(self):
        return self.song_id

    def getInfo(self):
        return self.song_id, self.publish_time, self.song_init_plays, self.language, self.gender

    def setAction(self, action):
        self.action.append(action)

class Action():
    def __init__(self, song_id, user_id, gmt_create, action_type, ds):
        self.song_id = song_id
        self.user_id = user_id
        self.gmt_create = gmt_create
        self.action_type = action_type
        self.ds = ds


def process_songs():

    artist_dic ={}
    song_map = {}

    with open("../../231531/mars_tianchi_songs_new.csv") as f:
        content = f.read().strip().split('\n')

        for line in content:
            temp = line.split(',')
            song_id = temp[0]
            artist_id = temp[1]
            publish_time = temp[2]
            song_init_plays = temp[3]
            language = temp[4]
            gender = temp[5]

            song_map[song_id] = artist_id

            if artist_id in artist_dic:
                song_list = artist_dic[artist_id]
                song = Song(song_id, publish_time, song_init_plays, language, gender)
                song_list[song_id] = song


            else:
                song = Song(song_id, publish_time, song_init_plays, language, gender)
                song_list = {}
                song_list[song_id] = song
                artist_dic[artist_id] = song_list


        print len(artist_dic)
        return artist_dic, song_map

def process_action():

    artist_dic, song_map = process_songs()

    with open("../../231531/mars_tianchi_user_actions_new.csv") as f:
        content = f.read().strip().split('\n')

        for line in content:
            temp = line.split(',')
            user_id = temp[0]
            song_id = temp[1]
            gmt_create = temp[2]
            action_type = temp[3]
            ds = temp[4]

            song = artist_dic[song_map[song_id]][song_id]
            action = Action(song_id, user_id, gmt_create, action_type, ds)
            song.setAction(action)

    return artist_dic

def saveData():
    artist_dic = process_action()

    for artist_key in artist_dic:
        # path = ""
        artist_path = "data/"+artist_key
        os.makedirs(artist_path)

        for song_key in artist_dic[artist_key]:
            song = artist_dic[artist_key][song_key]
            song_path = artist_path+"/"+song.getSong_id()
            os.makedirs(song_path)

            info_path = song_path+"/song_info"
            action_path = song_path+"/action_info"

            with open(info_path,'w') as f:
                song_id, publish_time, song_init_plays, language, gender = song.getInfo()
                f.write(artist_key +"\t" + song_id + "\t" + publish_time + "\t" + song_init_plays+'\t'+ language +"\t" + gender +"\n")

            with open(action_path,'w') as f:
                for action in song.action:
                    f.write(action.user_id +'\t'+action.gmt_create+"\t"+action.action_type+"\t"+action.ds+"\n")



if __name__ == '__main__':
    #process_songs()
    #process_action()
    saveData()


