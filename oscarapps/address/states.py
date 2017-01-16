from .models import States

states=States.objects.all()
stateList=[]
dict={}
for state in states:
    #stateStr="{'key':" + str(state.id) + "," + "value :" + state.state + "}"
    dict["key"]=state.id
    dict["value"]=state.state
    stateList.append(dict)
    dict={}





###  list of states in the United States Of America   ###
# statesList = [
#        'Alaska',
#        'Alabama',
#        'Arkansas',
#        'American Samoa',
#        'Arizona',
#        'California',
#        'Colorado',
#        'Connecticut',
#        'District of Columbia',
#        'Delaware',
#        'Florida',
#        'Georgia',
#        'Guam',
#        'Hawaii',
#        'Iowa',
#        'Idaho',
#        'Illinois',
#        'Indiana',
#        'Kansas',
#        'Kentucky',
#        'Louisiana',
#        'Massachusetts',
#        'Maryland',
#        'Maine',
#        'Michigan',
#        'Minnesota',
#        'Missouri',
#        'Northern Mariana Islands',
#        'Mississippi',
#        'Montana',
#        'National',
#        'North Carolina',
#        'North Dakota',
#        'Nebraska',
#        'New Hampshire',
#        'New Jersey',
#        'New Mexico',
#        'Nevada',
#        'New York',
#        'Ohio',
#        'Oklahoma',
#        'Oregon',
#        'Pennsylvania',
#        'Puerto Rico',
#        'Rhode Island',
#        'South Carolina',
#        'South Dakota',
#        'Tennessee',
#        'Texas',
#        'Utah',
#        'Virginia',
#        'Virgin Islands',
#        'Vermont',
#        'Washington',
#        'Wisconsin',
#        'West Virginia',
#        'Wyoming'
# ]


