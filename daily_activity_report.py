# !/usr/bin/python
# -*- coding: utf-8 -*-

import redmine
import pynotify
from datetime import datetime

r = redmine.Redmine('https://redmine.domain.com', key='bb3901e74d0bb7c6e2af55b6bcc41e3cb745738f61527d')

query_date = datetime.now()

# ids - array of usernames from redmine
ids = ['user1', 'user2']

adjustment = 65

# Activity report include: ticket number, ticket description, billable time
def get_time_entries(userid):
    activity = ""
    total_time = 0
    tes = r.time_entry.filter(from_date=query_date.strftime('%Y-%m-%d'), to_date=query_date.strftime('%Y-%m-%d'), user_id=userid)
    for i in range(len(tes)):
        activity   = activity + "#" + str(r.issue.get(tes[i].issue.id).id).ljust(7) + " " + r.issue.get(tes[i].issue.id).subject.ljust(adjustment-10) + str(tes[i].hours) + "\n"
        total_time = total_time + float(tes[i].hours)

    activity = activity + "\n" + "-" * adjustment + "\n" + "Total time: ".ljust(adjustment-1) + str(total_time)
    return activity


# Creating notification using pynotify
def pynotify_notification(activity_report, user):
    if __name__ == "__main__":
        if not pynotify.init("icon-summary-body"):
            sys.exit(1)

        n = pynotify.Notification(
            "Activity report for " + user + " for " + query_date.strftime('%d.%m.%Y %H:%M:%S'),
            activity_report,
            "notification-message-im")
        n.set_timeout(20)
        n.show()
    return

# Displaying activity reports for all users in ids array on stdout and popup notification
for i in ids:
    u = r.user.filter(name=i)
    activity = get_time_entries(u[0].id)
    print "Activity report for " + u[0].login + " for " + query_date.strftime('%d.%m.%Y %H:%M:%S') + "\n" + "-" * adjustment + "\n"
    print activity
    print "=" * adjustment
    pynotify_notification(activity, u[0].login)


