try:
    with open("../new.md", 'r') as f:
        f.write("this is a line")
except Exception as e:
    print("Error here", e)
