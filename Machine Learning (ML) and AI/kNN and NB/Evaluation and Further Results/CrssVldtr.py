import pandas as pd
import io
from knearestneighbour import classify_nn, reader
from naive_bayes import classify_nb

# coacenate 9 csv files into training data
def concatenate(filenames):
    concatenated_df = pd.concat((pd.read_csv(f, header=None) for f in filenames), ignore_index=True)
    return concatenated_df

def generate_combinations(i, dataset):
    # Generate the ith file, the testing file.
    fold_files = [f"pima-{i}.csv" for i in range(1, 11)]
    occupancy_files = [f"occupancy-{i}.csv" for i in range(1, 11)]

    # Exclude the i-th element, so all files other than the ith are training files
    train_pima = fold_files[:i - 1] + fold_files[i:]
    test_pima = [fold_files[i - 1]]

    train_occupancy = occupancy_files[:i - 1] + occupancy_files[i:]
    test_occupancy = [occupancy_files[i - 1]]
    
    # Concatenate training files into single file
    if dataset == "pima":
        return concatenate(train_pima), concatenate(test_pima)
     
    if dataset == "occupancy":
        return concatenate(train_occupancy), concatenate(test_occupancy)

def cssvldtr(k, algo):
    # k (above) = k value
    percentages = []

    for i in range(11):
        # generate all 10 combinations of trainiing/testing files
        train, test = generate_combinations(i, "pima")

        train = io.StringIO(train.to_csv(index=False, header=False))
        test = io.StringIO(test.to_csv(index=False, header=False))

        # run knn on files
        estimate, actual = classify_nn(train, test, k)

        # find accuracy of classifications
        if algo == "knb":
            bactual = classify_nb(train, test)
            matches = sum(e == a for e, a in zip(estimate, bactual))
            accuracy_percentage = (matches / len(bactual)) * 100
            percentages.append(accuracy_percentage)

        else:
            matches = sum(e == a for e, a in zip(estimate, actual))
            accuracy_percentage = (matches / len(actual)) * 100
            percentages.append(accuracy_percentage)
    
    # return mean accuracy
    return f"Accuracy: {sum(percentages)/len(percentages):.2f} "

def main():
    print(cssvldtr(5, "knb"))

if __name__ == "__main__":
    main()
