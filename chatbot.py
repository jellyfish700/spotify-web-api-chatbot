import tkinter as tk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from janome.tokenizer import Tokenizer

client_id = '8ac1304334c94e0c93e2816fd71ce211'
client_secret = 'a2a9031ad96c49a093bf8206463ea9f5'
client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

baseGround = tk.Tk()
baseGround.geometry('400x600')
baseGround.configure(bg='#c1d1e0')
baseGround.title('アーティストチャットボット')
 
# テキストボックス
fonts = ("源ノ角ゴシック", 15)
textBox1 = tk.Entry(width=40,font=fonts)
textBox1.place(x=10, y=550,width=290,height=40)

#ユーザー側のラベル
label1=tk.Label(text="",font=("源ノ角ゴシック", "13"),bg="#efe5cb")
label1.place(x=390,y=40,anchor=tk.E)

#チャットボット側のラベル
label2=tk.Label(text="",font=("源ノ角ゴシック", "13"),bg="#bfc9bd")
label2.place(x=10,y=90)

count=0
def val():
    global count
    if count>0:
      label1["text"]=""
      label2["text"]=""
    label1["text"]=textBox1.get()
    spo(textBox1.get())
    textBox1.delete(0,tk.END)
    count=count+1
    
def spo(name):
    data1 = name
    t = Tokenizer("project.csv", udic_enc="utf8")
    n_line = []
    for token in t.tokenize(data1):
        if token.part_of_speech.startswith("名詞,固有名詞"):
            n_line.append(token.surface)

    #入力にアーティスト名が無い
    if(len(n_line) == 0): 
        label2["text"]="アーティスト名が含まれていません。"
        
    else:
        info=[]  
        same=["似", "にている", "にてる"]
        for i in range(3):
            #入力に似ているという意味の単語があった場合
            if(same[i] in data1):
                ans = sp.search(q=n_line[0], type='artist')
                artists_id=(ans["artists"]["items"][0]["id"])
                result = sp.artist_related_artists(artists_id)
                count=0
                for artist in result['artists']:
                    count=count+1;
                    if count==6:
                        break
                    artist_name = artist['name']
                    info.append('{0} '.format(artist_name)) 
                mystring='似ているアーティストは\n'
                for x in info:
                    mystring=mystring+x+"\n"
                label2["text"]=mystring
                break
            #入力に似ているという意味の単語が無かった場合
            else:
                mylist = []
                results = sp.search(q=n_line[0],limit=20)
                for track in results['tracks']['items']:
                    mylist.append(track['name'])
                song=[]
                mylist = sorted(set(mylist), key=mylist.index)
                for i in range(10):
                    song.append('%d : %s' % (i+1, mylist[i]))
                mystring=f'{n_line[0]}の有名な曲は\n'
                for x in song:
                    mystring=mystring+x+"\n"
                mystring=mystring+"です。"
                label2["text"]=mystring
    
button = tk.Button(baseGround,text = '送信',command = val).place(x=310, y=550,width=80,height=40)
baseGround.mainloop()
