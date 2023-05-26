#!/usr/local/bin/python
"""#############################################################################

Date
	26 May 2023
 
Author(s)
	Dan Erickson (dan@danerick.com)

Description
	Copies playlists between Apple Music and Spotify

Project URL
	https://github.com/derickson2402/basically-apple-music
 
License
	GNU GPLv3

	Copyright (C) 2023 Dan Erickson

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <https://www.gnu.org/licenses/>.

#############################################################################"""

import spotify
import asyncio
from math import ceil
from creds import *

playlistID = input("Source playlist ID: ")

async def spotGetAllTracks(client: spotify.HTTPClient, playlistID: str) -> list:
	# Get the number of tracks in the playlist so we can iterate
	response = await client.get_playlist_tracks(playlistID, fields='total')
	numTracks = response['total']
	# Poll API to get full list of elements
	playlist = [{}]
	for i in range(ceil(numTracks / 100)):
		response = await client.get_playlist_tracks(playlistID, limit=100, offset=(100*i),fields='items(track(name,album(name),artists))')
		for item in response['items']:
			playlist.append({
				'name': item['track']['name'],
				'album': item['track']['album']['name'],
				'artist': item['track']['artists'][0]['name']
			})
		playlist += response
	return playlist

async def main():
	cli = spotify.HTTPClient(credClientID, credClientSecret)
	playlist = await spotGetAllTracks(cli, playlistID)
	for elmt in playlist:
		print(elmt)
	await cli.close()

if __name__ == '__main__':
	asyncio.run(main())
else:
	print("This is a script, not a library")
	exit(1)
