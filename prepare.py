
file_nakosais = eval(open(r"lv-dumpscan-nakos.txt", "r", encoding='utf-8').read())


thetext = ["* [[{}]]: {}".format(f[0],f[1]) for f in file_nakosais]


with open('dfdsfdsfsdfd.log', 'w', encoding='utf-8') as file_W:
    file_W.write('\n'.join(thetext))
