# Configuration
entity_id       = data.get("entity_id")
target          = data.get("target_entity_id")
today_target    = data.get("today_entity_id")
tomorrow_target = data.get("tomorrow_entity_id")
today           = data.get("today")
tomorrow        = data.get("tomorrow")
hours           = data.get("hours")
# Price data for today and tomorrow
prices    = hass.states.get(entity_id)
today     = prices.as_dict()['attributes'][today]
tomorrow  = prices.as_dict()['attributes'][tomorrow]

def minSum(arr, n, d):
    subset = []
    for (k) in range(n):
        if k+hours <= n:
          addTogether = []
          for i in range(k,k+hours-1):
            addTogether.append(arr[i])
          value = sum(addTogether)
          subset.append({'hour': k, 'sum': value, 'day': d})
    return subset

def removeTimesPassed(items):
    hourOfDay   = int(time.strftime("%H"))
    removeItems = []
    for i in items:
        if hourOfDay >= i["hour"]:
            removeItems.append(i)
    for i in removeItems:
        items.remove(i)

    return items

def formatState(time, day):
    h = str(time)
    if time < 10:
        h = "0" + h

    return h +' '+ day

today    = minSum(today,len(today), 'today')
today    = removeTimesPassed(today)

if (tomorrow):
    tomorrow = minSum(tomorrow,len(tomorrow), 'tomorrow')
    tomorrow = sorted(tomorrow, key=lambda k: k.get('sum', 0))
    state3   = formatState(tomorrow[0]['hour'], tomorrow[0]['day'])
    hass.states.set(tomorrow_target, state3, tomorrow[0])

    subsets  = today + tomorrow
else:
    subsets  = today
subsets  = sorted(subsets, key=lambda k: k.get('sum', 0))
state    = formatState(subsets[0]['hour'], subsets[0]['day'])
hass.states.set(target, state, subsets[0])

subsets  = sorted(today, key=lambda k: k.get('sum', 0))
state2    = formatState(subsets[0]['hour'], subsets[0]['day'])
hass.states.set(today_target, state2, subsets[0])
