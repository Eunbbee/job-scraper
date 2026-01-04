def save_to_file(file_name, jobs):
    file = open(f"{file_name}.csv", "w")
    file.write("Type, Title,Company,Location,Link\n")

    for job in jobs:
        file.write(
            f"{job['type']},{job['title']},{job['company_name']},{job['location']},{job['link']}\n")

    file.close()
