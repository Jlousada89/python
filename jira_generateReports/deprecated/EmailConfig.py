import smtplib
import DefaultConfig as default
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(sender=None, password=None, receiver=None, subject=None, body=None, files=None, smtp=None, port=None):
    if sender is None:
        sender = default.sender

    if password is None:
        password = default.password

    if receiver is None:
        receiver = default.receivers[0]

    if subject is None:
        subject = default.subject

    if body is None:
        body = default.body

    if smtp is None:
        smtp = default.smtp

    if port is None:
        port = default.port

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg['Cc'] = sender
    msg.attach(MIMEText(body, 'plain'))
    for file in files or []:
        with open(file, "rb") as f:
            part = MIMEApplication(
                f.read(),
                Name=basename(file)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        msg.attach(part)
        # socks.set_default_proxy(socks.SOCKS5, default.proxy_host, default.proxy_port)
        # socks.wrapmodule(smtplib)
        server = smtplib.SMTP(smtp, port)
        #if smtp != default.smtp:
        #server.ehlo()
        server.starttls()
        #server.ehlo()

        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        #server.close()
        server.quit()

    print("END")
