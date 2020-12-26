def save_top(top,filename):
    s = ""
    for i in top:
        user_id = i
        record = top[user_id]
        s += str(user_id) +';' + str(record) + '\n'
    with open(filename,'w') as f:
        f.write(s)
    print(s)

def load_top(filename):
    top = dict()
    succes = False
    try:
        with open(filename,'r') as f:
            s = f.read()
        succes = True
    except:
        return(dict())
    igroki = s.split('\n')
    for gamer in igroki:
        if gamer != '':
            name, score = gamer.split(';')
            top.update({int(name): int(score)})
    return(top)
#if main
top = {122:1337,12:2131243241}
save_top(top,'top_file.txt')

print("ПРОБЛЕМА")
print("при запуске этого файла, это сообщение должно выводится")
print("а при запуске бота, это сообщение выводится не должно")

top = load_top('top_file.txt')
print('результат',top)


