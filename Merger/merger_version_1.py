import pandas as pd
import re
import csv
import sys
from sys import getsizeof
import os

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 25)
pd.set_option('display.width', 1000)

# getting input for number of csv files to merge
def get_file_quantity():
    while True:
        try:
            nfiles = int(input("Please enter number of files to be merged: "))
        except ValueError:
            return False
            # continue
        else:
            return nfiles

# getting files names from user
def get_file_names(nfiles):
     files=[]
     for x in range(nfiles):

        try:
            filename=str(input("Please enter file name: "))
            filename=filename+".csv"
            if re.search("(\w+)+\.csv", filename):
                files.append(filename)

        except ValueError:
            return False

     return files

# loading files in to pandas dataFrames and finding common columns and interactive with user
def common_columns(files,nfiles):
    a=[]
    p=[]
    y=1
    # loading files in dataframs
    for i in range(nfiles):
            a.append(pd.read_csv(files[i], dtype='object', quotechar='"', encoding='utf8'))
            p.append(pd.read_csv(files[i], dtype='object', nrows=1, quotechar='"', encoding='utf8').columns)

    for u in p:
        print("\n Columns from file:", y,"\n")
        y = y + 1
        for k in u:
            print(k,sep=' ', end=' ', flush=True)
        print("\n")

    intersect=set(p[0]).intersection(*p)
    print("Common Columns are :- ")
    print(intersect)
    print("\n")
    x= str (input("Type the column name from the above list on which you want to merge \n OR...Type 'NO' to choose a different column name \n "))
    for i in intersect:

        if x==i:
         # print(x,i)
         return i, a
    #if user wants to merge on a column that he thinks is same
    if re.search("nO|NO|No|no",x):
        # for pdd in a:
        #   print(pdd)
        nextstep = str(input("OK Type another possible column name on which you want to merge ?"))
        itis=re.search("\.?(\w+)\_?",nextstep)
        # print(nextstep)
        if itis:
            user_column=re.split(r"[._]",itis.group())
            setter=True
            match=0
            print(user_column)
            for u in p:
                for k in u:
                    if setter:
                        q = re.search(user_column[0], k)
                        intersect = user_column[0]
                    else:
                        q = re.search(nextstep, k)

                        if q:
                            match = match + 1
                            print(q)

                        if match == nfiles:
                            print(match)

            change_c_names_and_merge(user_column, a, p, nextstep,nfiles,files)


        return nextstep, a

# if user choose a column that apparently is not the same forexample(firstfiles has: n.node_id, 2nd file has: node)
def change_c_names_and_merge(user_column,a,p,nextstep,nfiles,files):
    k=0
    w=0
    j=[]
    m=0

    for i in a:
        i.columns = i.columns.astype(str).str.replace(r".*("+nextstep+")[\_.*]?.*", nextstep,regex=True)
        a[k].columns=i.columns
        k=k+1

    filess = []
    for s in a:
        file_temp= "myfiles%s.csv" % w
        filess.append(file_temp)
        m=m+1
        s.to_csv(file_temp, index=False)
        w=w+1


    for i in range(nfiles):
        j.append(pd.read_csv(filess[i],dtype='object',quotechar='"',encoding='utf8'))

        os.remove(filess[i])
    merge_files_on_column(nextstep, j)

# merging files on the column selected by user
def merge_files_on_column(on_column,a):
    df = a[0]
    if on_column:

        # looping though dataFrames to merge files as 'outer join'
        for df_ in a[1:]:
             df=pd.merge(left=df,right=df_ , how='outer', on=on_column)

    else:

         print("Something went wrong")

    df.to_csv('Merged.csv', index=False, encoding='utf8')



def main():
    print("=====Welcome to the merging module======= ")

    number_of_Files=get_file_quantity()
    if number_of_Files:
       files=get_file_names(number_of_Files)
       if files:
        col,a=common_columns(files,number_of_Files)
        if col:
         merge_files_on_column(col,a)
    if number_of_Files==False:
         print("Wronge Input!!, Input a valid NUMBER")
         sys.exit()



if __name__ == "__main__":
    main()
