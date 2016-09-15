import pickle
GROUP_PICKEL = 'test.pickle'
aaa = ['TEST']
with open(GROUP_PICKEL, 'wb') as group_file:
    pickle.dump(aaa, group_file)
with open(GROUP_PICKEL) as f:
    print pickle.load(f)
