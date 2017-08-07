import csv
import datetime

def open_data():
  return open('data.csv')

def get_dates():
  with open_data() as f:
    reader = csv.reader(f)
    return [(l[0], datetime.datetime.strptime(l[1], '%Y-%m-%d').date(), l[2])
            for l in reader if len(l) >= 3]

def get_today():
  return datetime.date.today()

def get_next_event(target_date):
  dates = get_dates()
  for row in dates:
    if row[1] > target_date:
      return row

def find_next(date=None):
  target_date = date or get_today()
  event = get_next_event(target_date)
  if event:
    days = (event[1] - target_date).days
    plural = 's' if days > 1 else ''
    response =  '{} starts in {} day{}'.format(event[0], days, plural)
    if date:
      response += ' from {}'.format(date.strftime('%Y-%m-%d'))
    if event[2] == 't':
      response = "It's already the holidays. " + response
  else:
    response = 'Sorry, there are no upcoming events'
  return response
