import dates

import datetime
import json

def get_event(event, context):
  text = None
  slots = event['request']['intent']['slots']
  if slots:
    datestr = slots['Date']['value']
    try:
      date = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
    except ValueError:
      text = "Sorry, I didn't understand that date"
  else:
    date = None

  if not text:
    next_event = dates.find_next(date)

  response = {
    'version': '1.0',
    'response': {
      'outputSpeech': {
        'type': 'PlainText',
        'text': next_event,
      }
    }
  }

  return response

