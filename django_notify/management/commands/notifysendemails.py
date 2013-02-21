import os
import sys
import time
from datetime import datetime
from optparse import make_option

from django.contrib.sites.models import Site
from django.core import mail
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django_notify import models
from django_notify.settings import INTERVALS, DEFAULT_EMAIL,NOTIFY_SLEEP_TIME,EMAIL_SUBJECT


class Command(BaseCommand):
    help = 'Sends Notification emails to subscribed users taking into account the subscription interval'
    option_list = BaseCommand.option_list + (
        make_option('--daemon','-d',
        action='store_true',
        dest='daemon',
        default=True,
        help='Go to daemon mode and exit'),
        )


    def _send_user_notifications(self,context,connection):
        subject = _(EMAIL_SUBJECT) 
        message = render_to_string('emails/notification_email_message.txt',
                                   context)
        email = mail.EmailMessage(subject, message, DEFAULT_EMAIL,
                          [context['user'].email], connection=connection)
        email.send()



    def handle(self, *args, **options):
        daemon = options['daemon']
    
        # Run as daemon, ie. fork the process
        if daemon:
            try:
                fpid = os.fork()
                if fpid > 0:
                # Running as daemon now. PID is fpid
                    pid_file = file('/tmp/daemon-example.pid', "w")
                    pid_file.write(str(fpid))
                    pid_file.close()
                    sys.exit(0) 
            except OSError, e:
                sys.stderr.write("fork failed: %d (%s)\n" % (e.errno, e.strerror))
                sys.exit(1)        

        # This could be /improved by looking up the last notified person
        last_sent = None            
        context = {'user': None,
                   'notifications': None,
                   'digest': None,
                   'site': Site.objects.get_current()}

        #create a connection to smtp server for reuse
        connection = mail.get_connection()

        while True:    
            connection.open()
            started_sending_at = datetime.now()

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
                context['digest'] = INTERVALS[[y[0] for y in INTERVALS].index(setting.interval)][1]
                for subscription in setting.subscription_set.filter(send_emails=True,latest__is_emailed=False):  
                    context['notifications'].append(subscription.latest)  
                    subscription.latest.is_emailed=True
                    subscription.latest.save()
                if len(context['notifications']) > 0:
                    self._send_user_notifications(context,connection)
            
            connection.close()
            last_sent = datetime.now()
            elapsed_minutes = ((last_sent - started_sending_at).seconds) // 60
            time.sleep(max((min(INTERVALS)[0]*60-elapsed_minutes)*60,NOTIFY_SLEEP_TIME))
