import smtplib


#
# from email.message import EmailMessage
#
# file = 'some file'
# msg = EmailMessage()
# msg.set_content('Hello, Kit!')
# msg['Subject'] = f'The content of {file}'
# msg['From'] = 'audiomanagerrigister@gmail.com'
# msg['To'] = 'kitromanov@rambler.ru'
#
# s = smtplib.SMTP('localhost')
# s.send_message(msg)
# s.quit()

def send_email(message):
    sender = 'audiomanagerrigister@gmail.com'
    password = 'wrtrvtbhstlbxvls'
    receiver = 'kitromanov@rambler.ru'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender, password)
        server.sendmail(sender, receiver, f'Subject: Aloha\n{message}')

        return 'The message was sent successfully!'
    except Exception as _ex:
        return f'{_ex}\n check your login or password please!'


def main():
    print(send_email('Hi, man! \nIt\'s Kit.'))


if __name__ == '__main__':
    main()
