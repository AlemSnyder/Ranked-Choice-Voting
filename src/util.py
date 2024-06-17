def save_to_csv(data : dict, path: str) -> None:

    keys = [x for x in data] # keys to sort
    keys.sort(key=lambda x : data[x])

    with open(path, "w+") as f:
        for key in keys:
            f.write(f"{key}, {data[key]}\n")
        