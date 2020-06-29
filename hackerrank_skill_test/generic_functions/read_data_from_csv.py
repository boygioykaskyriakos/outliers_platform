def read_data_from_csv(path):
    raw_data = []

    with open(path) as infile:
        csv_reader = csv.reader(infile)
        for row in csv_reader:
            row = row[0]
            if " " in row:
                row_data = row.split()
                raw_data.append([int(row_data[0]), int(row_data[1])])
            else:
                raw_data.append(int(row))

    data_indexes = raw_data[1:raw_data[0]+1]
    data_queries = raw_data[raw_data[0]+2:]

    return data_indexes, data_queries