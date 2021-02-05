__author__ = "Trenton R. Rothwell"
__copyright__ = "Copyright 2021, Trenton R. Rothwell"
__version__ = "1.0.0"

import os
import time

gallery_files = []
for file in os.listdir("gallery"):
    gallery_files.append(file)


class Message:
    def find(self, regex):
        return str(self.data[1][self.data[0].index(regex)])

    def __init__(self, string_in):
        self.data = [[], []]
        level = 0
        in_quote = False
        store = None
        for char in string_in:
            if char == '[' or char == '{':
                level += 1
            elif char == ']' or char == '}':
                level -= 1
            elif char == '\"':
                if in_quote:
                    level -= 1
                else:
                    level += 1
                in_quote = not in_quote
            elif char == ':' and level == 0:
                self.data[0].append(store)
                store = ""
            elif char == ',' and level == 0:
                self.data[1].append(store)
                store = ""
            else:  # Not a container or special Char
                if store is None:
                    store = char
                else:
                    store += char

    def img_finder(self):
        tem = self.find("attachments")

        if tem is None or tem == '':
            return None
        x = tem.split("/")[-1].split(".")
        if len(x) != 3:
            return None
        x = str(x[0] + "." + x[2] + "." + x[1])
        global gallery_files
        for line in gallery_files:
            if line[-len(x):] == x:
                return str(os.path.dirname(__file__))+"\\gallery\\"+line
        return x

    def __str__(self):
        txt = self.find("text")
        atc = self.img_finder()

        creation_time = time.strftime("%Y/%b/%d %a %H:%M:%S", time.localtime(int(self.find("created_at"))))
        out = self.find("name") + "\t(" + str(creation_time) + ")" + ":\t"

        if atc is not None:
            out += "Img[" + atc + "]\t"
        if txt != "null":
            out += txt
        return out





def do():
    file = open("message.json", "r", encoding='utf-8')
    openSquare = 0
    openSquiggle = 0
    x = []
    newLine = False
    # Reads The Conversation.json File
    while True:
        # Gets the Current Char
        temp = file.read(1)

        # Bracket manager
        if temp == '{':
            if openSquiggle < 1:
                newLine = True
            openSquiggle += 1
        elif temp == '}':
            openSquiggle -= 1
        elif temp == '[':
            openSquare += 1
        elif temp == ']':
            openSquare -= 1

        # Break Conditions
        if openSquare == 0:
            print("Clean Exit")
            break
        elif not temp:
            SystemError("Failed Exit! Was the File Modified?")
            break

        # Adds clean Line to a List
        if openSquiggle >= 1:
            if newLine:
                x.append("")
                newLine = False
            else:
                x[-1] += temp
    file.close()
    output = []
    for msg in x:
        v = Message(msg)
        output.append(v)

    output.reverse()

    file = open("out.log", "w", encoding='utf-8')
    for i in output:
        file.write(str(i)+"\n")
    file.close()


do()
