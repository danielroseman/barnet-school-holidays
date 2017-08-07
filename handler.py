import dates

import datetime
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



def make_response(text, card_title='Thanks', should_end_session=False,
                  reprompt_text=None):
  response = {
    'version': '1.0',
    'response': {
      'outputSpeech': {
        'type': 'PlainText',
        'text': text,
      },
      'card': {
        'type': 'Simple',
        'title': card_title,
        'content': text
      },
      'shouldEndSession': should_end_session
    }
  }
  if reprompt_text:
    response['reprompt'] = {
      'outputSpeech': {
        'type': 'PlainText',
        'text': reprompt_text
      }
    }

  return response


def dispatch(event, context):
  request = event['request']

  if request['type'] == 'LaunchRequest':
    return make_response(get_event({}))
  elif request['type'] == 'IntentRequest':
    intent = request['intent']
    if intent['name'] == 'NextHoliday':
      return make_response(get_event(intent))
    elif intent['name'] == 'AMAZON.HelpIntent':
      text = ('Ask me for the next school holiday, or for the next holiday '
              'after a certain date.')
      return make_response(text, reprompt_text=text)
    elif intent['name'] in ('AMAZON.StopIntent', 'AMAZON.CancelIntent'):
      return make_response(
          'Thank you for using Barnet School Holidays',
          card_title='Goodbye',
          should_end_session=True
      )

  return make_response("Sorry, I didn't understand that request.")


def get_event(intent):
  date = None
  slots = intent.get('slots')
  if slots:
    datestr = slots['Date'].get('value')
    if datestr:
      try:
        date = datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
      except ValueError:
        return "Sorry, I didn't understand that date"

  return dates.find_next(date)

