import json

def dump_data(file, path, target):
    data = {
        'path': path,
        'target': target
    }

    with open(file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def main():
    path = str(input("Please enter the path to the directory to download attachments: \n"))
    if (path[-1] != '\\' or path[-1] != '/'):
        path += '\\'

    target = str(input("Please enter the email address of the sender: \n"))

    dump_data('paths.json', path, target)

    print("Sucess!\n")

if __name__ == '__main__':
    main()