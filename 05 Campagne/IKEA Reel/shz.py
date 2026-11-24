import asyncio, sys
from shazamio import Shazam
async def main():
    s = Shazam()
    for off in [0, 15, 30]:
        import subprocess
        subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",str(off),"-t","12","-i",sys.argv[1],"-vn",f"seg{off}.mp3"])
        r = await s.recognize(f"seg{off}.mp3")
        t = r.get("track")
        print(off, (t or {}).get("title"), "-", (t or {}).get("subtitle"), (t or {}).get("url"))
asyncio.run(main())
