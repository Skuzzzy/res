
import glob
import re
import json
import pickle


def cmp(name1, name2):
    name1_split = re.split(r'_|\.', name1)
    name2_split = re.split(r'_|\.', name2)
    diff = int(name1_split[2]) - int(name2_split[2])
    if diff != 0:
        return diff
    else:
        minor_diff = int(name1_split[3]) - int(name2_split[3])
        return minor_diff

def group(inline_groups):
    groups = []
    current_group = []

    name = inline_groups[0]
    split_name = re.split(r'_|\.', name)
    doc_id = split_name[2]
    current_id = doc_id
    current_group.append(name)

    for name in inline_groups[1:]:
        split_name = re.split(r'_|\.', name)
        doc_id = split_name[2]
        if doc_id != current_id:
            groups.append(current_group)
            current_group = []
            current_id = doc_id

        current_group.append(name)

    groups.append(current_group)
    return groups

def load_multi_groups(groups):
    # return [load_file_group(group) for group in groups]
    multi_group = []
    debug = 0
    for group in groups:
        multi_group.append(load_file_group(group))
        print debug, len(groups)
        debug+=1
    return multi_group


def load_file_group(group):
    users_list = []
    for doc in group:
        with open(doc) as data_f:
            data = json.load(data_f)
            users = [user_doc.get('name') for user_doc in data.get(u'users')]
            users_list.extend(users)
    return users_list

print "Globbing files..."
files = glob.glob('./dumps/*.json')
print "Sorting files..."
sorted_files = sorted(files, cmp=cmp)
print "Grouping files..."
grouped_files = group(sorted_files)
print "Loading groups...({0})".format(len(grouped_files))
loaded_groups = load_multi_groups(grouped_files)
print loaded_groups
print len(loaded_groups)
GROUP_PICKEL = 'groups.pickle'
with open(GROUP_PICKEL, 'wb') as group_file:
    pickle.dump(loaded_groups, group_file)
print "Done!"

