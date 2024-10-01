import random
import json
import csv
from sklearn.model_selection import train_test_split

def preprocess_categories(categories, labels_set):
    categories = categories.split(' ')
    res = []
    for category in categories:
        if category in labels_set.keys():
            res.append(category)
    return res

def balance_dataset(data, labels_set, class_limit=15000, num_labels=None):
    # Balancing utils
    data_distribution = {}
    for key in labels_set.keys():
        data_distribution[key] = {
            'count': 0,
            'entries': []
        }
    
    if num_labels is not None and not isinstance(num_labels, (list, tuple)):
        num_labels = [num_labels]
    
    # Process the data
    for entry in data:
        temp = {}
        temp["id"] = entry["id"]
        temp["title"] = entry["title"]
        temp["abstract"] = entry["abstract"]
        temp["authors"] = [f"{author[0]}, {author[1]}" for author in entry["authors_parsed"]]
        temp['categories'] = preprocess_categories(entry['categories'], labels_set)
        temp['primary_category'] = temp['categories'][0] if len(temp['categories']) > 0 else 'UNKNOWN'
        
        
        # Make sure number of entries in certain class does not exceed the limit for balancing purposes
        if temp['primary_category'] != 'UNKNOWN' and data_distribution[temp['primary_category']]['count'] < class_limit:
            if not num_labels or len(temp['categories']) in num_labels:
                data_distribution[temp['primary_category']]['entries'].append(temp)
                data_distribution[temp['primary_category']]['count'] += 1
            
    # Clear classes with zero entries
    del_keys = []
    for key in data_distribution:
        if data_distribution[key]['count'] == 0:
            del_keys.append(key)
    for key in del_keys:
        del data_distribution[key]
        
    # Return data distributed across classes (for further stratification)
    return data_distribution

def split_dataset(data_distribution, test_size=0.15, val_size=0, random_state=42):
    for key in data_distribution:
        train_split, test_split = train_test_split(data_distribution[key]['entries'], test_size=test_size, random_state=random_state)
        if val_size > 0 and val_size < 1:
            test_split, val_split = train_test_split(test_split, test_size=val_size, random_state=random_state)
        data_distribution[key]['train'] = train_split
        data_distribution[key]['test'] = test_split
        if val_size > 0 and val_size < 1:
            data_distribution[key]['val'] = val_split
    
    res = {
        'train': [],
        'test': []
    }
    if val_size > 0 and val_size < 1:
        res['val'] = []

    for key in data_distribution:
        for d_set in res:
            res[d_set] += data_distribution[key][d_set]
    random.seed(42)
    for d_set in res:
        random.shuffle(res[d_set])

    return (res[d_set] for d_set in res)

def write_to_csv(data, output_file):
    with open(output_file, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['id', 'title', 'abstract', 'authors', 'categories', 'primary_category'])
        for entry in data:
            csv_writer.writerow([entry['id'], entry['title'], entry['abstract'], str(entry['authors']), str(entry['categories']), entry['primary_category']])

if __name__ == '__main__':
    with open('./data/arxiv-metadata-oai-snapshot.json', 'r') as file:
        lines = file.readlines()
        data = [json.loads(line) for line in lines]

    with open('./data/labels.json', 'r') as file:
        labels_set = json.load(file)

    balanced_distribution = balance_dataset(data, labels_set, num_labels=(2,3), class_limit=15000)
    train_set, test_set = split_dataset(balanced_distribution)
    write_to_csv(train_set, 'arxiv_balanced_twothreelabel_train.csv')
    write_to_csv(test_set, 'arxiv_balanced_twothreelabel_test.csv')