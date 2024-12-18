import PyInstaller.__main__

PyInstaller.__main__.run([
    'youtube_downloader.pyw',
    '--name=YouTube下载器',
    '--onefile',
    '--noconsole',
    '--icon=youtube.ico',
    '--add-data=yt-dlp.exe;.',
    '--add-data=ffmpeg.exe;.',
    '--clean',
    '--version-file=version.txt'
]) 