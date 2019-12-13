str1 = "test"

file1 = open("dataTest.txt","a")
for i in range(5):
    file1.write(str1 + '\n')
file1.close()