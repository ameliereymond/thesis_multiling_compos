import re

string = 'IN: walk opposite right thrice after run opposite right OUT: I_TURN_RIGHT I_TURN_RIGHT I_RUN I_TURN_RIGHT I_TURN_RIGHT I_WALK I_TURN_RIGHT I_TURN_RIGHT I_WALK I_TURN_RIGHT I_TURN_RIGHT I_WALK'

output = re.split(' OUT: ', string)
print(output)