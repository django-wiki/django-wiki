import os
import sys
import time
from datetime import datetime
from optparse import make_option

from django_notify import settings as notify_settings

from django.contrib.sites.models import Site
from django.core import mail
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _, activate, deactivate
from django.conf import settings
from django_notify import models

import smtplib

import logging


class Command(BaseCommand):
    can_import_settings = True
    help = 'Sends notification emails to subscribed users taking into account the subscription interval' #@ReservedAssignment
    option_list = BaseCommand.option_list + (
        make_option('--daemon','-d',
        action='store_true',
        dest='daemon',
        default=False,
        help='Go to daemon mode and exit'),
        )

    def _send_user_notifications(self, context, connection):
        subject = _(notify_settings.EMAIL_SUBJECT)
        message = render_to_string(
            'emails/notification_email_message.txt',
            context
        )
        email = mail.EmailMessage(
            subject, message, notify_settings.EMAIL_SENDER,
            [context['user'].email], connection=connection
        )
        self.logger.info("Sending to: %s" % context['user'].email)
        email.send(fail_silently=False)

    def handle(self, *args, **options):
        # activate the language
        activate(settings.LANGUAGE_CODE)

        daemon = options['daemon']

        self.logger = logging.getLogger('django_notify')

        if not self.logger.handlers:
            if daemon:
                handler = logging.FileHandler(filename=notify_settings.NOTIFY_LOG)
            else:
                handler = logging.StreamHandler(self.stdout)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        self.logger.info("Starting django_notify e-mail dispatcher")

        if not notify_settings.SEND_EMAILS:
            print "E-mails disabled - quitting."
            sys.exit()



        # Run as daemon, ie. fork the process
        if daemon:
            self.logger.info("Daemon mode enabled, forking")
            try:
                fpid = os.fork()
                if fpid > 0:
                # Running as daemon now. PID is fpid
                    self.logger.info("PID: %s" % str(fpid))
                    pid_file = file(notify_settings.NOTIFY_PID, "w")
                    pid_file.write(str(fpid))
                    pid_file.close()
                    sys.exit(0)
            except OSError, e:
                sys.stderr.write("fork failed: %d (%s)\n" % (e.errno, e.strerror))
                sys.exit(1)

        try:
            self.send_loop()
        except KeyboardInterrupt:
            print "\nQuitting..."

        # deactivate the language
        deactivate()

    def send_loop(self):

        # This could be /improved by looking up the last notified person
        last_sent = None
        context = {'user': None,
                   'notifications': None,
                   'digest': None,
                   'site': Site.objects.get_current()}

        #create a connection to smtp server for reuse
        try:
            connection = mail.get_connection()
        except:
            self.logger.error("Could get a mail connection")
            raise

        while True:
            try:
                connection.open()
            except:
                self.logger.error("Could not use e-mail connection")
                raise
            started_sending_at = datetime.now()

            self.logger.info("Starting send loop at %s" % str(started_sending_at))

            if last_sent:
                settings = models.Settings.objects.filter(
                    interval__lte=((started_sending_at-last_sent).seconds // 60) // 60
                ).order_by('user')
            else:
                settings = models.Settings.objects.all().order_by('user')

            for setting in settings:
                context['user'] = setting.user
                context['notifications']= []
                #get the index of the tuple corresponding to the interval and get the string name
                context['digest'] = notify_settings.INTERVALS[[y[0] for y in notify_settings.INTERVALS].index(setting.interval)][1]
                for subscription in setting.subscription_set.filter(
                    send_emails=True,
                    latest__is_emailed=False
                ):
                    context['notifications'].append(subscription.latest)
                if len(context['notifications']) > 0:
                    try:
                        self._send_user_notifications(context, connection)
                        for n in context['notifications']:
                            n.is_emailed=True
                            n.save()
                    except smtplib.SMTPException:
                        # TODO: Only quit on certain errors, retry on others.
                        self.logger.error("You have an error with your SMTP server connection, quitting.")
                        raise

            connection.close()
            last_sent = datetime.now()
            elapsed_seconds = (last_sent - started_sending_at).seconds
            time.sleep(
                max(
                    (min(notify_settings.INTERVALS)[0] - elapsed_seconds) * 60,
                    notify_settings.NOTIFY_SLEEP_TIME,
                    0
                )
            )
