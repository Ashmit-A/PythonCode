from pytube import YouTube

def download_video(url, path='.'):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=path)

url = input("Enter the YouTube video URL: ")
path = input("Enter the download path (default is current directory): ")
if not path:
    path = '.'
download_video(url, path)