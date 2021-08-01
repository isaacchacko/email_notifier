# email notifier

Gmail won't notify me when I get a new email, almost costing me my first job. It's fine, I just have to do it myself.

### requirements:

- imaplib and email, to pull your email

- win10toast, to send windows notifications

- os and json, to save/load emails

### things to change before running:

- from email address and email pass: self-explanatory

- depth (optional): how many emails does the bot download

- targets (optional): which emails have a higher priority and will send a push notification when allowed

- notifs (optional): change either to "none", "all", or "targets_only" for the desired result

- this isn't in the code itself, but you have to allow the "less secure apps access". this project doesn't use the Gmail API (because it was a headache to try to get runnning, and the docs aren't easy to access because I can't find them, was relying on the "dir()" and "help()" commands until i gave up), hence Google won't like what I'm doing. Without the setting turned off, Google will deny your access




