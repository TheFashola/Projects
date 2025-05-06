import math

def reader(filename, testing):
    # Reset file pointer to the beginning (in case it's a StringIO object)
    filename.seek(0)
    lines = filename.read().strip().splitlines()

    if testing:
        # Skip the last column for testing
        lines = [",".join(line.split(",")[:-1]) for line in lines]

    return lines


def data_classes(ls):
    yes_ls = []
    no_ls = []

    i = 0
    while i < len(ls):
        all_elements = ls[i].split(',')
        yes_or_no = all_elements[len(all_elements)-1].strip()

        if yes_or_no == 'yes':
            yes_ls.append(all_elements[:-1])

        elif yes_or_no == 'no':
            no_ls.append(all_elements[:-1])

        i += 1

    return yes_ls, no_ls


def get_mean(ls):
    all_means = []

    for i in range(len(ls[0])):
        column_sum = sum(float(row[i]) for row in ls)
        average = column_sum / len(ls)
        all_means.append(average)

    return all_means


def get_sd(ls, means):
    all_sds = []

    for i in range(len(ls[0])):
        numerator = sum(math.pow(float(row[i]) - means[i], 2) for row in ls)
        stdev = math.sqrt(numerator/(len(ls) - 1))
        all_sds.append(stdev)

    return all_sds

def probability_density(x, mean, stdev):
    if stdev == 0:
        return 1
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1/(math.sqrt(2 * math.pi) * stdev)) * exponent


def classify_nb(training_filename, testing_filename):
    file_lines = reader(training_filename, False)
    yes_class_ls, no_class = data_classes(file_lines)
    mean_yes_ls = get_mean(yes_class_ls)
    sd_yes_ls = get_sd(yes_class_ls, mean_yes_ls)
    mean_no_ls = get_mean(no_class)
    sd_no = get_sd(no_class, mean_no_ls)
    testing_data = reader(testing_filename, True)

    predicted_classes = []

    for instance in testing_data:

        instance_features = instance.strip().split(',')

        prob_yes = 1
        for i, feature in enumerate(instance_features):
            prob_yes *= probability_density(float(feature), mean_yes_ls[i], sd_yes_ls[i])
        prob_yes *= len(yes_class_ls) / (len(yes_class_ls) + len(no_class))  

        prob_no = 1
        for i, feature in enumerate(instance_features):
            prob_no *= probability_density(float(feature), mean_no_ls[i], sd_no[i])
        prob_no *= len(no_class) / (len(yes_class_ls) + len(no_class))

        predicted_class = "yes" if prob_yes >= prob_no else "no"
        predicted_classes.append(predicted_class)
        
    return predicted_classes