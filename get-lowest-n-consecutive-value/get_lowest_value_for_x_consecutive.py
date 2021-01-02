# Configuration
entity_id = data.get("entity_id")
target    = data.get("target_entity_id")
today     = data.get("today")
tomorrow  = data.get("tomorrow")
hours     = data.get("hours")
# Price data for today and tomorrow
prices    = hass.states.get(entity_id)
today     = prices.as_dict()['attributes'][today]
tomorrow  = prices.as_dict()['attributes'][tomorrow]

def minSum(arr, n, d):
    subset = []
    for (k) in range(n):
        if k+hours < n:
          addTogether = []
          for i in range(k,k+hours):
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

today    = minSum(today,len(today), 'today')
today    = removeTimesPassed(today)
tomorrow = minSum(tomorrow,len(tomorrow), 'tomorrow')
subsets  = today + tomorrow
subsets  = sorted(subsets, key=lambda k: k.get('sum', 0))
state    = str(subsets[0]['hour']) +' '+ subsets[0]['day']
hass.states.set(target, state, subsets[0])
