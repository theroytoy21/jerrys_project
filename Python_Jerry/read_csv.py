import csv

def read_csv():
    filename = "esg.csv"

    # key: value
    esg_scores = {}

    with open(filename, 'r') as file:
        csvFile = csv.reader(file)
        i = 0

        for lines in csvFile:
            if i != 0:
                if lines[7] == '':
                    esg_scores[lines[0]] = 0       
                else:    
                    esg_scores[lines[0]] = lines[7]
            i = 1
        
    return esg_scores