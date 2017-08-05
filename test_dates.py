import dates
import pytest 
import datetime
from io import StringIO

DATES = """
Autumn term,2017-09-04
Half term,2017-10-21
Second half of autumn term,2017-10-30
End of autumn term,2017-12-20
"""

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
  def fake_open():
    return StringIO(DATES)
  monkeypatch.setattr('dates.open_data', fake_open)

@pytest.fixture()
def october(monkeypatch):
  return datetime.date(2017,10,31)

@pytest.fixture()
def december(monkeypatch):
  return datetime.date(2017,12,31)

def test_get_dates():
  data = dates.get_dates()
  assert len(data) == 4
  for row in data:
    assert len(row) == 2
    assert isinstance(row[1], datetime.date)

def test_get_next_event(october):
  event = dates.get_next_event(october)
  assert event[0] == 'End of autumn term'

def test_get_next_event_no_data(december):
  assert dates.get_next_event(december) is None

def test_find_next_no_date(monkeypatch, october):
  monkeypatch.setattr('dates.get_today', lambda: october)
  assert dates.find_next() == 'End of autumn term starts in 50 days'

def test_find_next_with_date(october):
  assert dates.find_next(october) == 'End of autumn term starts in 50 days from Tuesday October 31'
