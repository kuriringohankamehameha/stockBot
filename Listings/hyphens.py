with open("nyse.csv", "r") as rfile:
    with open("new.csv", "w") as wfile:
        for line in rfile:
            if "-" in line.split(",")[1]:
                line = line.replace("-", " ")
            if " " in line.split(",")[0]:
                line = line.replace(" ", "-")
            wfile.write(line)
