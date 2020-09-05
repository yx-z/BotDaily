#! /usr/bin/python2

import json
import os
import sqlite3

playlist_name = "soft"

database_path = "/Library/Containers/com.netease.163music/Data/Documents/storage/sqlite_storage.sqlite3"

cx = sqlite3.connect(os.path.expanduser('~') + database_path)
cx.row_factory = sqlite3.Row


def getPlaylistNameFromJson(jsonStr):
    playlistDetail = json.loads(jsonStr)
    # return playlistDetail["name"].encode("GBK", 'ignore');
    return playlistDetail["name"].encode("utf-8", 'ignore');


def getMusicNameFromJson(jsonStr):
    musicDetail = json.loads(jsonStr)
    return musicDetail["name"];


def getArtistNameFromJson(jsonStr):
    load = json.loads(jsonStr)
    ret = []
    for artist in load["artists"]:
        ret.append(artist["name"].encode("utf-8", 'ignore'))
    return ret


def getPlaylist():
    cu = cx.cursor()
    cu.execute("select * from web_playlist")
    playlists = []
    for item in cu.fetchall():
        playlist = (item["pid"], getPlaylistNameFromJson(item["playlist"]))
        playlists.append(playlist)
    return playlists


def getPlayListMusic(pid):
    cu = cx.cursor()
    cu.execute("select * from web_playlist_track where pid=?", [pid])
    musics = []
    for item in cu.fetchall():
        musics.append(item["tid"]);
    return musics


def getMusicDetail(tid):
    cu = cx.cursor()
    cu.execute("select * from web_track where tid=?", [tid])
    music = cu.fetchone()
    if music is None:
        return None
    # detail = (getMusicNameFromJson(music["detail"]), music["relative_path"])
    musicName = getMusicNameFromJson(music["track"])
    musicArtists = getArtistNameFromJson(music["track"])
    return (musicName, musicArtists)


def main():
    playlists = getPlaylist()
    for item in playlists:
        playlistID = item[0]
        playlistName = item[1]

        if playlistName != playlist_name:
            continue

        output = open(os.getcwd() + "/resource/favorite_music.json", 'w')
        output.write("[\n")
        musicIds = getPlayListMusic(playlistID)
        for tid in musicIds:
            if tid is not None:
                musicInfo = getMusicDetail(tid)
                if musicInfo is not None:
                    musicName, musicArtists = musicInfo
                    if musicName is not None:
                        output.write(
                                "[\"" + musicName.encode("utf-8", 'ignore'))
                        output.write(
                                "\",\"" + ','.join(musicArtists) + "\", \"\"")
                        output.write("],\n")
        output.write("[]]\n")
    cx.close()


if __name__ == '__main__':
    main()
