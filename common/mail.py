from flask_mail import Mail, Message
from flask import render_template

app = None
mail = None

def init_mail(App):
    global mail
    app = App
    if mail == None:
        mail = Mail(app)
    return mail


def get_mail():
    return mail


def send_email(to, subject, template, url, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs, base_url=url)
    msg.html = render_template(template + '.html', **kwargs, base_url=url)
    mail.send(msg)
