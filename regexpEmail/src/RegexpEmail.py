# Make a regular expression
# for validating an Email
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regexDomain = r'\b[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def check(email):

    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regex, email):
        return True
    else:
       return False

def checkDomain(domain):

    # pass the regular expression
    # and the string into the fullmatch() method
    if re.fullmatch(regexDomain, domain):
        return True
    else:
        return False

listDomains = []

with open('DomainsList.out', 'w') as out:
    with open('Emails.txt', encoding='utf8') as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip('\n')
            line = line.strip(' ')

            emails = line.split(';')
            domain = emails[0];

            if checkDomain(domain) is True:
                if domain not in listDomains:
                    listDomains.append(domain)
                    print(domain)
                    out.write(domain)
                    out.write('\n')

            for email in emails:
                if check(email) is True:
                    domain = email[email.index('@') + 1 : ]

                    if checkDomain(domain) is True:
                        if domain not in listDomains:
                            listDomains.append(domain)
                            print(domain)
                            out.write(domain)
                            out.write('\n')

f.close()
out.close()

with open('DomainsListSorted.out', 'w') as l:
    print("==============================================================")
    print("sorting...")
    listDomains.sort()
    print("sorted..")
    print("==============================================================")
    print()
    print("LIST:")
    print(listDomains)
    l.write(str(listDomains))
l.close()

