import wave


if __name__ == '__main__':
    d = wave.open("/Users/bjhl/2355205682_syxuaose.mp3").getnchannels()
    print(d)
