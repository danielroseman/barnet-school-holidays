import csv
import datetime

def open_data():
  return open('data.csv')

def get_dates():
  with open_data() as f:
    reader = csv.reader(f)
    return [(l[0], datetime.datetime.strptime(l[1], '%Y-%m-%d').date())
            for l in reader if len(l) >= 2]

def get_today():
  return datetime.date.today()

def get_next_event(target_date):
  dates = get_dates()
  for desc, dt in dates:
    if dt > target_date:
      return desc, dt

def find_next(date=None):
  target_date = date or get_today()
  event = get_next_event(target_date)
  if event:
    days = (event[1] - target_date).days
    plural = 's' if days > 1 else ''
    response =  '{} starts in {} day{}'.format(event[0], days, plural)
    if date:
      response += ' from {}'.format(date.strftime('%A %B %-d'))
  else:
    response = 'Sorry, there are no upcoming events'
  return response
