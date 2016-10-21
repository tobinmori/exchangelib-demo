from exchangelib import DELEGATE, IMPERSONATION, Account, Credentials, \
    EWSDateTime, EWSTimeZone, Configuration, NTLM, CalendarItem, Q

credentials = Credentials(username='', password='')

account = Account(primary_smtp_address='', credentials=credentials,
                  autodiscover=True, access_type=DELEGATE)

WHITELIST_FOLDERS = ['','',]

def print_account_folders():
    """
    Mainly, for debug purposes so that you can see you folder hierarchy and
    whether there are any children.

    INTERESTINGLY, Inbox and others have no subfolders or subitems.

    :return:
    """
    for k,v in account.folders.items():
        print(k,v)

def print_all_root_folders():
    """
    Prints ALL folders under Root.

    :return:
    """
    print(account.root.get_folders())

def get_all_root_folders():
    """
    An unelegant way to get a list of the Root folder
    (by getting the ONLY folder that has children)
    """
    for folder in account.folders.keys():
        if len(account.folders[folder]) > 0:
            return account.folders[folder]
    return None

def get_root_folders_by_name():
    """
    Returns a list of the 1st generation of folders under root.
    """
    return [str(folder) for folder in get_all_root_folders()]

def print_emails(folder):
    if (folder.all().count() > 1):
        for m in folder.all():
            print(m)
    else:
        item = folder.get()
        print(item)

def extract_folder(folder):
    """
    Returns a list of emails, given a folder
    """
    emails = []
    if (folder.all().count() > 1):
        for m in folder.all():
            emails.append(m)
    else:
        item = folder.get()
        emails.append(item)
    return emails

def get_whitelisted_folders():
    """
    Returns a list of whitelisted folders as objects
    """
    whitelisted = []
    for folder in get_all_root_folders():
        if str(folder) in WHITELIST_FOLDERS:
            whitelisted.append(folder)
    return whitelisted

def get_emails():
    """
    Returns a list of emails, in the WHITELISTED list.
    :return:
    """
    items = []
    for folder in get_all_root_folders():
        if str(folder) in WHITELIST_FOLDERS:
            items.extend(extract_folder(folder))
        else: continue
    return items

def get_email_by_subject(folder, subject):
    """
    Return Queryset that matches subject
    """
    return folder.filter(subject__contains=subject)

def search_by_subject(subject):
    """
    Return a list of emails, that match the subject
    :param subject:
    :return:
    """
    emails = []
    for folder in get_whitelisted_folders():
        if folder is None: continue
        for email in get_email_by_subject(folder, subject):
            emails.append(email)
    return emails
