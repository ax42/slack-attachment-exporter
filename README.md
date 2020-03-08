# Slack attachment exporter
Export all attachments from a Slack channel.

Usage:
`export SLACK_TOKEN=xoxo-..... ; slack-attachment-export CHANNEL`

 * CHANNEL is the channel name visible in Slack (the script will find the channel ID)
 * Files will be stored in `./downloads/channel-name` 
 * Filenames will be in the format `<date+time> - <username of poster> - <filename.ext>`.  This should mean no duplicate filenames and it should be easy to link back to your Slack channel's history.
 
 # Caveats
  * Requires at least Python 3.6
  * Requires Slacker https://github.com/os/slacker
  * Doesn't paginate its calls (so if your channel has > 1000 files it won't download them all)

PRs welcome if you would like to improve this.
