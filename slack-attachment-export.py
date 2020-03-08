#!/usr/bin/env python3
"""List items in slack."""

# https://github.com/os/slacker
# https://api.slack.com/methods

import os
import argparse
import requests
from datetime import datetime
from slacker import Slacker

def findChannel(slack, channelName):
 
  response = slack.conversations.list(limit = 1000, types=('private_channel','public_channel'))
  channels = response.body['channels']
  print("There are {0} public and private channels".format(len(channels)))

  try:
    return [x for x in channels if x['name'] == args.channel][0]
  except:
    return None

def findFiles(slack, channelID):
  response = slack.files.list(count = 1000, channel=channelID)
  files = response.body['files']
  print(f"Found {len(files)} files in the channel.")
  for f in files:
    print(f"{f['name']}: {datetime.fromtimestamp(f['created']).strftime('%Y%m%d-%H%M%S')} by {f['user']}")
  return files

def getUsers(slack, fileList):
  userMap = {}
  userIDs = list(set([f['user'] for f in fileList])) # deduplicated list
  print(f"Fetching usernames for {len(userIDs)} users who posted files.")
  for u in userIDs:
    response = slack.users.info(user = u)
    user = response.body['user']
    userMap[user['id']] = user['name']
  
  return userMap

def downloadFiles(token, dirName, fileList, userList):
  targetDir = os.path.join("./downloads", dirName)
  try:
    os.makedirs(targetDir)
    print(f"Created {targetDir}")
  except FileExistsError:
    print(f"{targetDir} already exists, will overwrite existing files.")
  except:
    print(f"Could not create {targetDir} - exiting")
    return None
  # for file in fileList

  headers = {"Authorization": f"Bearer {token}"}
  for file in fileList:
    url = file['url_private']
    try:
      r = requests.post(url, headers=headers)
    except:
      print(f"Could not download {file['name']}.")
    targetFilename = os.path.join(targetDir, f"{datetime.fromtimestamp(file['created']).strftime('%Y%m%d-%H%M%S')} - {userList[file['user']]} - {file['name']}")
    try:
      open(targetFilename, 'wb').write(r.content)
      print(f"Wrote {targetFilename}")
    except:
      print(f"Error writing {targetFilename}")


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Export Attachments from a channel.  Set SLACK_TOKEN environment variable to your token.')
  parser.add_argument(
    'channel',
    default=None,
    metavar='CHANNEL_NAME',
    help="Name of channel to export file attachments from.")

  args = parser.parse_args()

  try:
    token = os.environ['SLACK_TOKEN']
    slack = Slacker(token)
  except KeyError as ex:
    print('Environment variable %s not set.' % str(ex))


  targetChannel = findChannel(slack, args.channel)
  if targetChannel:
    print(f"Found channel '{targetChannel['name']} (id {targetChannel['id']})")
  else:
    print(f"{args.channel} not found in Slack")
    exit
  
  fileList = findFiles(slack, targetChannel['id'])

  if len(fileList) > 0:
    userList = getUsers(slack, fileList)
    downloadFiles(token, args.channel, fileList, userList)

