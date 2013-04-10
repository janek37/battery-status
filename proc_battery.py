#!/usr/bin/env python3
import sys
from time import sleep

BATTERY_STATUS_FILE = "/proc/acpi/battery/BAT0/state"
BATTERY_INFO_FILE = "/proc/acpi/battery/BAT0/info"

def parse_file(input_file, keys):
  res = {}
  for line in input_file:
    key = line.split(":")[0]
    data = line.split(":")[1].strip().split(" ")[0]
    if key in keys:
      res[key] = data
  return tuple(res[key] for key in keys)

def battery_capacity():
  capacity, = parse_file(open(BATTERY_INFO_FILE), ('last full capacity',))
  return int(capacity)

def battery_state():
  rate, remaining, state = parse_file(open(BATTERY_STATUS_FILE),
    ('present rate', 'remaining capacity', 'charging state'))
  try:
    rate = int(rate)
  except ValueError:
    rate = 0
  remaining =  int(remaining)
  if state != "discharging" or not rate:
    return state, remaining, None
  else:
    return state, remaining, rate

def state():
  return battery_state()[0]

def time_left():
  state, remaining, rate = battery_state()
  if rate:
    return float(remaining) / rate

def time_left_hm():
  return hours_minutes(time_left())

def hours_minutes(hours):
  if hours:
    full_hours = int(hours)
    minutes = int((hours - full_hours) * 60)
    return full_hours, minutes
  else:
    return 0, 0

def percent_full():
  state, remaining, rate = battery_state()
  capacity = battery_capacity()
  return remaining * 100. / capacity
