# pulling emails
import imaplib
import email

# notifications
from win10toast import ToastNotifier

# for save() and load()
from os.path import exists
from json import dumps, loads

# so people on github dont hack me
from os import environ

# so i can keep running this forever
from time import sleep

SMTP_SERVER = "imap.gmail.com" 
SMTP_PORT = 993

# customize these before running
EMAIL_ADDRESS = environ.get('EMAIL_ADDRESS')
EMAIL_PASS = environ.get('EMAIL_PASS')
DEPTH = 100
TARGETS = []
NOTIFS = 'all'

def load(filename):
  if exists(filename):
    with open(filename, 'r') as f:
      savedData = f.read()
      if savedData != '':
        return loads(savedData)

      else:
        with open(filename, 'w') as f:
          return []
  else:
    with open(filename, 'w') as f:
      f.write('')
      return []

def save(filename, savedData):
  with open(filename, 'w') as f:
    f.write(dumps(savedData))

def notify(info):
  subject, from_ = info['subject'], info['from']
  try:
    toaster.show_toast(subject, 
      from_, 
      threaded = False, 
      icon_path = None, 
      duration = 4
    )
  except NameError:
    toaster = ToastNotifier()
    toaster.show_toast(subject, 
      from_, 
      threaded = False, 
      icon_path = None, 
      duration = 4
    )

def main():
  # grab 50 emails from my gmail account
  mail = imaplib.IMAP4_SSL(SMTP_SERVER)
  mail.login(EMAIL_ADDRESS,EMAIL_PASS)
  mail.select('inbox')

  data = mail.search(None, 'ALL')
  mail_ids = data[1]
  id_list = mail_ids[0].split()   
  first_email_id = int(id_list[-DEPTH])
  latest_email_id = int(id_list[-1])

  current_emails = []

  for i in range(latest_email_id,first_email_id, -1):
    data = mail.fetch(str(i), '(RFC822)')
    for response_part in data:
      arr = response_part[0]
      if isinstance(arr, tuple):
        msg = email.message_from_string(str(arr[1],
                                        'utf-8'))
        info = {'subject': msg['subject'],
                'from': msg['from']}

        for parameter in [('>', ')'), ('<', '(')]:
          info['from'] = info['from'].replace(parameter[0],
                                              parameter[1]
                                            )
        
        current_emails.append(info)


  # compare old and new email lists to find the difference
  old_emails = load('emails.json')
  ageIndicator = old_emails[0]
  try:
    newEmailCount = current_emails.index(ageIndicator)
  except ValueError:
    newEmailCount = DEPTH
    print('''Email Notifier has not been run for awhile, 
so there is no telling how many emails have arrived since. 
Scanning depth is {}.'''.format(DEPTH))

  # send a notification for every new email
  for new_email in current_emails[0:newEmailCount]:
    if NOTIFS == 'all':
      notify(new_email)
    if NOTIFS == 'targets_only':
      for target in TARGETS:
        if target in new_email['from']:
          notify(new_email)
  
  # save new emails if any
  if newEmailCount != 0:
   save('emails.json', current_emails)

if __name__ == '__main__':
  while True:
    main()
    sleep(30*60)