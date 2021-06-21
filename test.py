def append_file(name, append_data):
    with open(name, "a+") as f:

        f.seek(0)
        data = f.read(100)

        if len(data) > 0:
            f.write("\n")

        f.write(append_data)

append_file("/etc/locale.gen", "en_US.UTF-8 UTF-8")
os.system("locale-gen")
