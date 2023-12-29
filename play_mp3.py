
# from playsound import soundplayer


filepath = "E:\\assets\\audio\\少妇白洁\\少妇白洁011.mp3"
# print(f"播放文件: {filepath}")
# soundplayer(filepath)
# print(f"播放文件: {filepath} 结束")

text_file = open(filepath , "rb")
content = text_file.read(4)
text_file.close()

print(content)





