import math

# Function for finding euclidian distance between two entries
def euclidean(entry1, entry2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(entry1, entry2)))

# Function converting file content into tuples
def reader(lines, training):

    attributes = []
    classes = []

    for line in lines.strip().split('\n'):
        parts = line.split(',')

        if training:
            # if training data, create seperate array for the classes (yes/no)
            attributes.append(tuple(map(float, parts[:-1])))
            classes.append(parts[-1])
        else:
             attributes.append(tuple(map(float, parts)))

    return attributes, classes

def classify_nn(training_filename, testing_filename, k):
    training_file = open(training_filename, "r")
    training_lines = training_file.read()
    training_attributes, training_classes = reader(training_lines, True)

    testing_file = open(testing_filename, "r")
    testing_lines = testing_file.read()
    testing_attributes, _ = reader(testing_lines, False)

    est_classes = []
    for test_entry in testing_attributes:
        distances = []
        # for each test entry, find the euclidian distance from a training entry
        for train_entry, train_class in zip(training_attributes, training_classes):
            distance = euclidean(test_entry, train_entry)
            # append distance + class to distances array
            distances.append((distance, train_class))

        # sort the distances, and choose the k smallest distances
        distances.sort()  
        k_nearest = distances[:k] 

        # find most common class, append to est_classes
        freq = {}
        for _, _class in k_nearest:
            freq[_class] = freq.get(_class, 0) + 1
        
        if 'yes' in freq and 'no' in freq and freq['yes'] == freq['no']:
            est_classes.append('yes')
        else:
            est_classes.append(max(freq, key=freq.get))

    return est_classes

# def main():
#     lol = classify_nn("training_file", "testing_file", 3)
#     print(lol)

# if __name__ == "__main__":
#     main()