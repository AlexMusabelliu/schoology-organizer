import os, json, re, sys, time
from itertools import chain

def load(file):
    r = {}
    if os.path.isfile(file):
        with open(file) as f:
            t = f.readlines()
            r.update({x[:x.find(":")]:x[x.find(":") + 1:x.rfind(",")] for x in t})
    else:
        print(f"{file} not found! It may have been deleted if this is not the first setup.")
    return r

def is_list(d):
    return d.count(",") > 0

def write_schedule(d, list=False):
    f = open("schedule.sched")
    if list:
        for i in d.split(","):
            ti = re.search(r"\d:+\d*", i)
            cl = re.search(r"[a-zA-Z ]+\s(?!\n)", i)
            li = re.search(r"https*://.*/.*\w", i)

            tiw = i[ti.start():ti.end()].strip()
            clw = i[cl.start():cl.end()].strip()
            liw = i[li.start():li.end()].strip()

            f.write(f"{tiw}\n{clw}\n{liw}\n\n")

    f.close()

def write_settings(args):
    f = open("settings.txt")
    f.write("user:{0},\n" % args.get("user"))
    f.write("alternate:{0},\n" % args.get("alternate"))
    f.close()


def setup():
    settings = {}
    print("Welcome to the schoology commandline organizer.")
    print("You will be guided for a first-time setup of your schoology schedule.")
    print("\nPress enter to continue...")
    input()

    print("Let's introduce eachother. Hi, I'm SCHEDULY, the CMD line scheduler. And you are?")
    settings.update({"user":input("Enter your username:    ")})
    print("Hi, {0}!" % settings.get("user"))
    while True:
        print("Do you go by an alternating schedule?")
        alt = input("Yes/[No]:    ")
        if alt[0].lower() == "y":
            alt = True
        else:
            alt = False
        print(("You have an alternating schedule." if alt else "You don't have an alternating schedule.") + " Is this correct?")
        cont = input("Yes/[No]:    ")
        if cont[0].lower() == "y":
            break
        print("Canceled the operation.")
    settings.update({"alternate":str(alt)})
    write_settings(settings)

    print("Let's start by getting the schedule together.")
    print("You can either enter your classes one-by-one, e.g.:")
    print("    Study Hall 9:26: https://g.co/meet/your-link-here")
    print("\nOr you can enter them all at once, e.g.:")
    print("    Study Hall 9:26: https://zoom.us/meeting/your-link-here, History 10:54: [link], Econ 1:07: [link], etc.")
    print("\nWhen you want to quit, just type 'quit' or 'q'")
    
    sched = input("\nPlease enter your schedule:\n")
    l = is_list(sched)

    write_schedule(sched, l)

    print("Thank you for setting up your user. You can now proceed with the program.")
    input("\nPress Enter to continue...")

def setting():
    pass

def load_sched():
    f = open("schedule.sched")
    t = f.read()
    b = t.split("\n\n")
    sched = {}
    for i in range(len(b)):
        d = b[i]
        ti = re.search(r"\d:+\d*", d)
        cl = re.search(r"[a-zA-Z ]+\s(?!\n)", d)
        li = re.search(r"https*://.*/.*\w", d)

        tiw = d[ti.start():ti.end()].strip()
        clw = d[cl.start():cl.end()].strip()
        liw = d[li.start():li.end()].strip()

        # f.write(f"{tiw}\n{clw}\n{liw}\n\n")
        
        sched.update({i:(clw, tiw, liw)})

    return sched

def run():
    s = load_sched()
    sett = load("settings.txt")
    day = int(time.strftime("%w"))
    if day == 1:
        print("Sorry, no synchronous classes today! Enjoy your Monday!")
        return
    day = day > 1 and day < 4 

    if day:
        offset = 0
    else:
        offset = 4

    # offset = 4

    debounce = True
    old_time = None
    print(s)
    while True:
        s = load_sched()
        t = time.time()

        days = t // 86400
        hours = t // 3600 % 12 - 4
        minutes = t // 60 % 60
        seconds = t % 60

        if not debounce and minutes != old_time:
            debounce = True

        for i in chain(range(0, 1), range(1 + offset, offset + 5)):
            # print(i)
            tim = s[i][1]
            h = int(tim[:tim.rfind(":")])
            m = int(tim[tim.rfind(":") + 1:])

            if hours == h and minutes == m and debounce:
                print("joining")
                os.system(f"start chrome.exe {s[i][2]} -incognito")
                debounce = False
                old_time = m
        # break

def start():
    # print('started')
    while True:
        menu = {1:"Run", 2:"Settings", 3:"Quit"}
        func = {1:run, 2:setting, 3:sys.exit}

        print("\n".join([str(i) + ":" + str(menu.get(i)) for i in menu]))
        c = input("Enter a number:    ")

        func.get(int(c), (lambda: None))()

def main():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    os.system("cls")
    
    settings = load("settings.txt")

    # print(settings)

    user = settings.get("user", "user")

    print(f"Hello {user}!")

    if settings == {}:
        setup()
        
    start()

if __name__ == "__main__":
    main()