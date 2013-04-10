#!/usr/bin/env python3
import sys
from time import sleep
import subprocess
import re

ACPI_CMD = 'acpi'

def battery_state():
  info_text = subprocess.check_output(
    ACPI_CMD).split('\n')[0].split(':', 1)[1].strip()
  parts = [part.strip() for part in info_text.split(',')]
  state = parts[0].lower()
  percent = float(parts[1].strip('%'))
  if len(parts) > 2:
    hours, minutes = (int(part) for part in parts[2].split(':', 2)[:2])
  else:
    hours = minutes = 0
  return state, percent, hours, minutes

def state():
  return battery_state()[0]

def percent_full():
  return battery_state()[1]

def time_left_hm():
  return battery_state()[2:]
