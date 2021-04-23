import sqlite3
from collections import deque
with open('./patients.txt','r',encoding='utf-8')as f:
    patient_data = f.readlines()

conn = sqlite3.connect('nhi_drug_data.db')
cur = conn.cursor()
for data in patient_data:
    patient_name = data.strip().split('|')[0]
    drug_list = data.strip().split('|')[1:]
    # <這段要for迴圈，先把這個人的所有用藥成份都記錄到tmp_dict>
    drug_name_dict = {}
    for drug_code in drug_list:
        sel = "select compare_use from nhi_drug_data where drug_code = '{}';".format(drug_code.lower())
        cur.execute(sel)
        tmp = cur.fetchone()
        if tmp:
            tmp = tmp[0].split('|')
        else:
            continue
        for index, check in enumerate(tmp):
            if '#' in check:
                check = check.split('#')[0]
                tmp[index] = check
            drug_name_dict[check] = 0
        # print(drug_name_dict.keys())
    # </這段要for迴圈，先把這個人的所有用藥成份都記錄到tmp_dict>

    deq = deque(drug_name_dict.keys())
    # print(deq)
    print('=====')
    while deq:
        tmp = deq.popleft()
        try:
            sel = "select ingredient from {};".format(tmp)
            cur.execute(sel)
            check_list = cur.fetchall()
            check_list = [content[0] for content in check_list]
            for q in deq:
                if q in check_list:
                    print(patient_name,'的',tmp,' 與 ',q,' 有交互作用')
        except:
            print('no this drug data')

cur.close()
conn.close()
