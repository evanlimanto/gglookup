"""
Eric Bo
Parse
HackJam
9/27/2014
"""
import re
from collections import OrderedDict

# def main(): #calls parse method
#      text = open('output.txt').read()
#      dict1, dict2, dict3, stats, dist = parse(text)
#      print ("dict1: ", dict1, '\n')
#      print ("dict2: ", dict2, '\n')
#      print ("dict3: ", dict3, '\n')
#      print ("part3: ", stats,'\n', dist)

def parse(text): #parses raw data
    text = open('output.txt').read()
    parts = text.split('\n\n')
    dict1 = parse_assignment_list(parts[0])
    dict2, dict3 = parse_all_grades(parts[1])
    stats, dist = parse_stats(parts[2])
    return dict1, dict2, dict3, stats, dist

def parse_assignment_list(part1): #glookup -t
    dict1 = OrderedDict()
    lines = part1.split('\n')  # --> ['Line 1', 'Line 2', 'Line 3']
    lines = lines[2:]
    for line in lines:
        line = line.lstrip()
        numColons = line.count(':')
        if numColons == 3:
            array = line.split(':')
            assignment_name = array[0]
            submission_date = array[1] + ':' + array[2] + ':' + array[3]
            dict1[assignment_name] = submission_date
        elif numColons == 5:
            array = line.split(':')
            assignment_name = array[0]
            submission_date = array[1] + ':' + array[2] + ':' + array[3] + ':' + array[4] + ':' + array[5]
            dict1[assignment_name] = submission_date
        elif numColons == 4:
            more_submission_dates = ', '+ line.lstrip()
            last_key = list(dict1.keys())[-1]
            dict1[last_key] = dict1[last_key] + more_submission_dates
    return dict1

def parse_all_grades(part2): #glookup
    dict2 = OrderedDict()
    dict3 = OrderedDict()
    lines = part2.split('\n')
    lines = lines[3:]
    for line in lines:
        line = line.lstrip()
        assignment_name = line.split(':')[0]
        if 'Total' in assignment_name or 'total' in assignment_name:
            score = line.split(':')[1].strip()
        else:
            array = re.split('\s+', line)
            score = array[1]
            weight = array[2]
            if len(array) >= 4:
                reader = array[3]
            if len(array) >= 5:
                comments = ' '.join(array[4:])
        dict2[assignment_name] = score
        dict3[assignment_name] = weight
    return dict2, dict3

def parse_stats(part3): #glookup -s _???
    statList = []
    dist = OrderedDict()
    lines = part3.split('\n') #list by each line

    for line in lines:
        if line == '':
            lines.remove(line)

    if len(lines) == 1:
        return None, None

    statLines = lines[1:11] #cut off the first line
    distLines = lines[12:]

    # distLines = distLines[:-1]

    for line in statLines:
        line = line.replace(" ", "") #remove all spaces
        line = line.split(':') #make line a list with the stat, num
        stat = line[1].split('(')[0] #really only applies to first line
        statList.append(stat)

    for line in distLines:
        line = line.replace(" ", "") #0.0-4.1:123****
        line = line.split(':') #[a'0.0-4.1', '123****']
        line[1] = int(line[1].replace("*", "")) #[123]
        dist[line[0]] = line[1] #{'0.0-4.1': 123}

    return statList, dist

# if __name__ == '__main__': main()