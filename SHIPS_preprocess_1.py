import csv
import itertools

def concat_split(x,width=5):
    result=''
    start=0
    while True:
        s=str(x)[start:start+width]
        if s:
            result =result + s + '&'
        else:
            break
        start=start+width
    return result[:-1]
def split_string(s, widths):
    points = [0] + list(itertools.accumulate(widths))
    return [s[points[i]:points[i+1]] for i in range(len(widths))]

# run only one times
fo = open("\outputwp.csv", 'a',newline='')
writer = csv.writer(fo)
widths = [5,7,3,5,7,7,5,9,4,4,4,4,4,4,5,5,5,5,5,5,5,5,4,4,5,5,5,5,5]
with open(r"\WP_1982_2019.dat", "r") as f: # data from ships
    all_data = f.readlines()
    for i in range(0,len(all_data)):# len(all_data)
        if (all_data[i][1].isupper() == True) or (all_data[i][0].isupper() == True):
            row = split_string(all_data[i], widths)
        else:
            row1 = concat_split(all_data[i])
            row = row1.split("&") 
        finalrow = []
        for i in range(0,len(row)):
            try:
                res = row[i].split()[0]
            except:
                res = -999
            finalrow.append(res)
        writer.writerow(finalrow)
fo.close()