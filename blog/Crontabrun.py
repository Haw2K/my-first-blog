from crontab import CronTab
#cron = CronTab(user='deeplearning')
cron = CronTab(user=True)


# list all cron jobs (including disabled ones)
cron.remove_all()
#for job in cron:
#    cron.remove(job)

job = cron.new(command='python3.5 /home/deeplearning/djangogirls/blog/TestCrontab.py')
job.minute.every(1)
job.enable()
#job_standard_output = job.run()


cron.write()