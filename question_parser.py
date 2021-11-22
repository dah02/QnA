import os
import sys

def question_data(q_db):
    file = open(q_db, 'r')
    lines = file.readlines()
    file.close()

    data=[]
    for i in range(8):
        data.append({"category":"", "thresh":0, "question":[], "res":[]})

    for l in lines:
        ch = l.rstrip("\n").split("\t")
        category = ch[0]
        num = int(ch[1])
        if category == 'T':
            data[num]["category"] = ch[2]
            data[num]["thresh"] = int(ch[3])
        elif category == "Q":
            data[num]["question"].append(ch[2])
        elif category == "C":
            data[num]["res"].append(ch[3])
    return data

if __name__=="__main__":
    file = "questions.txt"
    data = question_data(file)

    for d in data:
        category = d["category"]
        thresh = d["thresh"]
        question = d["question"]
        pos, neg = d["res"]

        points = 0

        for q in question:
            print(q)
            points += 3
        if points >= thresh:
            print(pos)
        else:
            print(neg)
