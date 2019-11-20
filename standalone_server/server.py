#!/usr/bin/env python3

from bottle import post, request, run, BaseRequest

quarantine_sent = False
@post("/")
def index():
    game = request.json
    berlin_data = game["cities"]["Berlin"]
    print(f'round: {game["round"]}, Berlin events: {get_quarantine_event(berlin_data)}')

    global quarantine_sent
    action = {"type": "endRound"}
    if not quarantine_sent:
      action = {"type": "putUnderQuarantine", "city": "Berlin", "rounds": 1}
      quarantine_sent = True
    return action


def get_quarantine_event(city):
    events = city.get("events", [])
    return list(filter(lambda e: e["type"] == "quarantine", events))


BaseRequest.MEMFILE_MAX = 10 * 1024 * 1024
run(host="0.0.0.0", port=50123, quiet=True)
