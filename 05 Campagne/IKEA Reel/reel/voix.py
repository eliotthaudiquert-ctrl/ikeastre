import asyncio, edge_tts, subprocess, json, sys
sys.stdout.reconfigure(encoding="utf-8")
L = {
 "l1": ("fr-FR-DeniseNeural", "Je pars chez ma mère.", "+0%", "+0Hz"),
 "l2": ("fr-FR-HenriNeural", "Attends, c'est pas ce que tu crois !", "+12%", "+0Hz"),
 "l3": ("fr-FR-VivienneMultilingualNeural", "Il y a... quelqu'un ?", "-15%", "-2Hz"),
 "l4": ("fr-FR-RemyMultilingualNeural", "Non, non, non ! Pas comme ça !", "+18%", "+6Hz"),
 "l5": ("fr-FR-VivienneMultilingualNeural", "Tu m'as piqué la couette toute la nuit !", "+10%", "+4Hz"),
 "l6": ("fr-FR-RemyMultilingualNeural", "J'ai eu mon permis !", "+8%", "+8Hz"),
 "l7": ("fr-FR-DeniseNeural", "L'armoire est montée !", "+8%", "+4Hz"),
 "l8": ("fr-FR-HenriNeural", "Il reste une vis.", "-10%", "-4Hz"),
}
async def main():
    out={}
    for k,(v,t,r,p) in L.items():
        await edge_tts.Communicate(t, v, rate=r, pitch=p).save(f"public/voix/{k}.mp3")
        subprocess.run(["ffmpeg","-loglevel","error","-y","-i",f"public/voix/{k}.mp3","-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse","-ar","48000",f"public/voix/{k}.wav"])
        d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"public/voix/{k}.wav"]))
        out[k]=round(d,3); print(k,d,t)
    json.dump(out,open("src/voix.json","w"))
asyncio.run(main())
