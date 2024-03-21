import os
import sys
import re
import json
import datetime
from datetime import date, timedelta, datetime

def jsonreader():

    home = os.path.expanduser("~")
    with open(f"{home}/.jafr/user-settings.json", "r") as user_settings:
        sample_user_settings = json.load(user_settings)

    home_dir = sample_user_settings["master"]

    if os.path.exists(home_dir):
        return home_dir
    else:
        sys.stderr.write("Jafr's chosen master directory does not exist.\n")
        sys.exit(0)

def taskreader(home_dir):
    task_file_path = home_dir + "/" + "tasks.md"
    if os.path.isfile(task_file_path):
        task_file = open(task_file_path, "r")

        tasks = []

        for line in task_file:
            match = re.search(r"\b\d{2}/\d{2}/\d{2}\b", line)
            if match and "Due" in line and "-" in line: 
                parts = line.strip().split(' Due: ') 
                
                desc = parts[0][2:]
                dates_and_status = parts[1].split(' ')
                
                dates = (datetime.strptime(dates_and_status[0], "%d/%m/%y")).date()
                
                status = ' '.join(dates_and_status[1:])

                if status == "complete" or status == "not complete":
                    tasks.append((desc, dates, status))
                else:
                    continue

        return tasks
    else:
        sys.stderr.write("Missing tasks.md or meetings.md file.\n")
        sys.exit(0)

def taskdisplayer(tasks):

    tasks_today = []
    tasks_3_days_later = []

    today = datetime.now().date()
    three_days_later = (datetime.now() + timedelta(days=3)).date()
   
    for t in tasks:

        if t[1] == today and t[2] == "not complete":
            tasks_today.append("- " + t[0])
        elif (t[1] > today and t[1] <= three_days_later and t[2] == "not complete"):
            tasks_3_days_later.append("- " + t[0] + " by " + t[1].strftime("%d/%m/%y"))
    

    print("Just a friendly reminder! You have these tasks to finish today.")
    for t in tasks_today:
        print(t)

    print("\nThese tasks need to be finished in the next three days!")
    for t in tasks_3_days_later:
        print(t)

def meetingsreader(home_dir):
    meetings_file_path = home_dir + "/" + "meetings.md"
    if os.path.isfile(meetings_file_path):
        meetings_file = open(meetings_file_path, "r")

        meetings = []

        for line in meetings_file:
            match = re.search(r"\b\d{2}/\d{2}/\d{2}\b", line) 
            match2 = re.search(r"\b\d{2}:\d{2}\b", line)
            if match and match2 and "-" in line and "Scheduled" in line: 
                parts = line.strip().split(' Scheduled: ') 
                
                desc = parts[0][2:]
                date_and_time = parts[1].split(' ')
                
                time = date_and_time[0]
                date = (datetime.strptime(date_and_time[1], "%d/%m/%y")).date()
                

                meetings.append((desc, time, date))
            
        return meetings, meetings_file_path

    else:
        sys.stderr.write("Missing tasks.md or meetings.md file.\n")
        sys.exit(0)

def meetingsdisplayer(meetings):

    meetings_today = []
    meetings_7_days_later = []

    today = datetime.now().date()
    seven_days_later = (datetime.now() + timedelta(days=8)).date()
   
    for m in meetings:

        if m[2] == today:
            meetings_today.append("- " + m[0] + " at " + m[1])
        elif m[2] > today and m[2] <= seven_days_later:
            meetings_7_days_later.append("- " + m[0] + " on " + m[2].strftime("%d/%m/%y") + " at " + m[1])

    print("\nYou have the following meetings today!")
    for t in meetings_today:
        print(t)

    print("\nYou have the following meetings scheduled over the next week!")
    for t in meetings_7_days_later:
        print(t)

def change_master_dir():

        new_master = input("Which directory would you like Jafr to use?\n")

        if os.path.isdir(new_master):

            with open(".jafr/user-settings.json", "r") as user_settings:
                sample_user_settings = json.load(user_settings)
                sample_user_settings["master"] = new_master

                sample_user_settings_out = open(".jafr/user-settings.json", "w")
    
                json.dump(sample_user_settings, sample_user_settings_out, indent = 6)

            print("Master directory changed to {}.".format(new_master))
        
        else:
            sys.stderr.write("Jafr's chosen master directory does not exist.")
            sys.exit(0)

def complete_task(tasks, home_dir):
    try:
        complete_task_list = []
        tasks_to_do = []

        j = 0
        for t in tasks:
            if t[2] == "not complete":
                j+=1

        if j!= 0:

            print("Which task(s) would you like to mark as completed?")

            i = 1
            for t in tasks:
                if t[2] == "not complete":
                    print("{}. ".format(i)  + t[0] + " by " + t[1].strftime("%d/%m/%y"))
                    complete_task_list.append(t[0])
                    i+=1

            def user_input():
                number_input = input("").strip()
                number_input_arr = number_input.split(" ")
                return number_input, number_input_arr
                
            right_input = True

            number_input, number_input_arr = user_input()
            def input_checker(number_input_arr):
                nonlocal right_input
                right_input = True
                for n in number_input_arr:
                    if int(n) > len(complete_task_list) + 1 or int(n) < 0:
                        right_input = False     
                return right_input

            while input_checker(number_input_arr) == False:
                print("invalid task")
                number_input, number_input_arr = user_input()
                right_input = input_checker(number_input_arr)

            if input_checker(number_input_arr) == True:
            
                for t in number_input_arr:
                    if t != "" or t!= " ":
                        t = int(t) - 1
                        tasks_to_do.append(complete_task_list[t])
                    
                with open(home_dir + "/" + "tasks.md", "r") as task_file:
                    lines = task_file.readlines()

                for idx, line in enumerate(lines):
                    for task in tasks_to_do:
                        if task in line:
                            lines[idx] = line.replace("not complete", "complete")

                with open(home_dir + "/" + "tasks.md", "w") as file:
                    file.writelines(lines)

                print("Marked as complete.")

        else:
            print("No tasks to complete!")
    
    except:
        print("invalid task")
        print("Marked as complete.")

def add_meeting(meetings_file_path):

    desc = input("Please enter a meeting description:")
    while ("Scheduled:" in desc or "Due:" in desc) or desc == " " or desc == "":
        sys.stdout.write("\ninvalid description")
        desc = input("Please enter a meeting description:")
    
    date = input("\nPlease enter a date:")

    def date_check(date):
        try:
            datetime.strptime(date, '%d/%m/%y')
            return True
        except:
            return False

    while date_check(date) == False:
        sys.stdout.write("\ninvalid date")
        date = input("Please enter a date:")

    time = input("\nPlease enter a time:")

    def time_check(time):
        try:
            datetime.strptime(time, '%H:%M')
            return True
        except:
            return False

    while time_check(time) == False:
        sys.stdout.write("\ninvalid time")
        time = input("Please enter a time:")

    date_check = re.search(r"\b\d{2}/\d{2}/\d{2}\b", date) 
    name_check = re.search(r"\b\d{2}:\d{2}\b", time)

    if name_check and date_check:
        f = open(meetings_file_path, "a")
        f.write("\n##### added by you")
        f.write(f"\n- {desc} Scheduled: {time} {date}\n")
        f.close()

    print(f"\nOk, I have added {desc} on {date} at {time}.")

    users_to_share_with = []

    y_or_n = input("Would you like to share this meeting? [y/n]: ")
    if y_or_n == "y":
        add_n_share_meeting(desc, date, time)

    else:
        next_menu()

    return desc, date, time

def add_n_share_meeting(desc, date, time):

    passwd_path = sys.argv[1]
    passwd_contents = []

    if os.path.isfile(passwd_path):
        passwd_file = open(passwd_path, "r")
        for line in passwd_file:
            passwd_contents.append(line.strip().split(":"))

        passwd_contents = [user for user in passwd_contents if user[0] != os.environ['USER']]


    print("Who would you like to share with?")
    for user in passwd_contents:
        print(user[2] + " " + user[0])

    chosen_users = input("").split(" ")

    for user in passwd_contents:
        for chosen_user in chosen_users:
            if chosen_user == user[2]:
                user_home_dir = user[5]
                user_meeting_file_path = user_home_dir 

                with open(user_meeting_file_path + "/.jafr/user-settings.json", "r") as user_json:
                    user_settings = json.load(user_json)
                    user_home_dir = user_settings["master"]

                with open(user_home_dir + "/" + "meetings.md", "w") as file2:
                        file2.write(f"\n##### shared by {os.environ['USER']}\n")
                        file2.write("- " + "{}".format(desc) + " Scheduled: " +  time + " " + date +"\n")


    print("Meeting shared.")
    next_menu()
    
def share_tasks(tasks):

    passwd_path = sys.argv[1]
    passwd_contents = []

    if os.path.isfile(passwd_path):
        passwd_file = open(passwd_path, "r")
        for line in passwd_file:
            passwd_contents.append(line.strip().split(":"))

        passwd_contents = [user for user in passwd_contents if user[0] != os.environ['USER']]

            
    print("Which task would you like to share?")

    i = 1
    for t in tasks:
        print("{}. ".format(i) + "{}".format(t[0]) + " by " + t[1].strftime("%d/%m/%y"))
        i += 1

    selection = int(input(""))

    print("Who would you like to share with?")
    for user in passwd_contents:
        print(user[2] + " " + user[0])

    chosen_users = input("").split(" ")

    for c in chosen_users:
        if len(c) != 4:
            selection = int(input("WRONG!\n"))
            print(c)

    for user in passwd_contents:
        for chosen_user in chosen_users:
            if chosen_user == user[2]:
                user_home_dir = user[5]
                user_task_file_path = user_home_dir 

                with open(user_task_file_path + "/.jafr/user-settings.json", "r") as user_json:
                    user_settings = json.load(user_json)
                    user_home_dir = user_settings["master"]

                with open(user_home_dir + "/" + "tasks.md", "w") as file2:
                        file2.write(f"\n##### shared by {os.environ['USER']}\n")
                        file2.write("- " + "{}".format(tasks[selection-1][0]) + " Due: " + tasks[selection-1][1].strftime("%d/%m/%y") + " " + tasks[selection-1][2]+"\n")


    print("Task shared.")
    next_menu()
                    
def share_meetings(meetings):

    passwd_path = sys.argv[1]
    passwd_contents = []

    if os.path.isfile(passwd_path):
        passwd_file = open(passwd_path, "r")
        for line in passwd_file:
            passwd_contents.append(line.strip().split(":"))

        passwd_contents = [user for user in passwd_contents if user[0] != os.environ['USER']]

    
    print("Which meeting would you like to share?")

    i = 1
    for m in meetings:
        print("{}. ".format(i) + m[0] + " on " + m[2].strftime("%d/%m/%y") + " at " + m[1])
        i += 1

    selection = int(input(""))

    print("Who would you like to share with?")
    for user in passwd_contents:
        print(user[2] + " " + user[0])

    chosen_users = input("").split(" ")

    for c in chosen_users:
        if len(c) != 4:
            selection = int(input("WRONG!\n"))
            print(c)


    for user in passwd_contents:
        for chosen_user in chosen_users:
            if chosen_user == user[2]:
                user_home_dir = user[5]
                user_meeting_file_path = user_home_dir 

                with open(user_meeting_file_path + "/.jafr/user-settings.json", "r") as user_json:
                    user_settings = json.load(user_json)
                    user_home_dir = user_settings["master"]

                with open(user_home_dir + "/" + "meetings.md", "w") as file2:
                        file2.write(f"\n##### shared by {os.environ['USER']}\n")
                        file2.write("- " + "{}".format(meetings[selection-1][0]) + " Scheduled: " +  meetings[selection-1][1] + " " + meetings[selection-1][2].strftime("%d/%m/%y") +"\n")


    print("Meeting shared.")
    next_menu()

def menu():
    sys.stdout.write("\nWhat would you like to do?\n")
    sys.stdout.write("1. Complete tasks\n")
    sys.stdout.write("2. Add a new meeting.\n")
    sys.stdout.write("3. Share a task.\n")
    sys.stdout.write("4. Share a meeting.\n")
    sys.stdout.write("5. Change Jafr's master directory.\n")
    sys.stdout.write("6. Exit\n")

def next_menu():
    sys.stdout.write("What would you like to do?\n")
    sys.stdout.write("1. Complete tasks\n")
    sys.stdout.write("2. Add a new meeting.\n")
    sys.stdout.write("3. Share a task.\n")
    sys.stdout.write("4. Share a meeting.\n")
    sys.stdout.write("5. Change Jafr's master directory.\n")
    sys.stdout.write("6. Exit\n")

def main():
    home_dir = jsonreader()
    tasks = taskreader(home_dir)
    meetings, meetings_file_path = meetingsreader(home_dir)
    taskdisplayer(tasks)
    meetingsdisplayer(meetings)
    menu()

    selection = input("")

    if (0 < int(selection) < 7):

        if selection == "1":
             complete_task(tasks, home_dir)
             next_menu()

        if selection == "2":
            add_meeting(meetings_file_path)

        if selection == "3":
            share_tasks(tasks)

        if selection == "4":
            share_meetings(meetings)

        elif selection == "5":
            change_master_dir()
            next_menu()

        elif selection == "6":
            sys.exit(0)

    
if __name__ == '__main__':
    main()