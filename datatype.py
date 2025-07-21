a = input("University roll number. :")

if a.isdigit():
    value = int(a)

elif a.replace('.', '', 1).isdigit() and a.count('.') < 2:
    value = float(a)

elif a.lower() == "true":
    value = True

elif a.lower() == "false":
    value = False

else:
    value = a

print(value,type(value))
