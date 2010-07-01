import gdata.youtube.service
arguments = ["self", "info", "args"]
helpstring = "youtube <entry> <url> Availible entries are: title, pubdate, desc, category, tags, and duration"
minlevel = 1

def main(connection, info, args) :
    vid = args[2].split("&", 1)[0].split("?v=", 1)[1]
    x = gdata.youtube.service.YouTubeService()
    y = x.GetYouTubeVideoEntry(video_id=vid)
    z = y.media
    a = {"title":z.title.text, "pubdate":y.published.text, "desc":z.description.text, "category":z.category[0].text, "tags":z.keywords.text, "duration":z.duration.seconds}
    connection.msg(info["channel"], a[args[1]])
