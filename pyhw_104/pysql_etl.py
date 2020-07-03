import requests
from bs4 import BeautifulSoup
import os
import pymysql

host = 'localhost'
port = 3306
user = 'root'
passwd = 'Rootroot12'
db = 'homework'
charset = 'utf8mb4'

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
cookies={'over18':'1'}
k=0

while True:
    keyin_websit = input('請輸入想抓取的ptt版網址，非首頁：')
    ptt_homepage = 'https://www.ptt.cc/bbs'
    keyin_websit = keyin_websit.split('/')
    check_websit = '/'.join(keyin_websit[0:4])
    file_name = input('請輸入存放資料夾名稱：')
    if (keyin_websit[0] != 'Q') and (keyin_websit[0] != 'q'):
        if (check_websit == ptt_homepage) and (len(keyin_websit) > 4) and (keyin_websit[4] != '' and keyin_websit[4].strip() != 'index.html'):
            keyin_websit[-1]='index{}.html'
            pre_url = '/'.join(keyin_websit).strip().format('')
            pre_req = requests.post(url=pre_url,headers=headers,cookies=cookies)
            pre_soup = BeautifulSoup(pre_req.text,'html.parser')
            pre_bt = pre_soup.select('a[class="btn wide"]')[1]['href']
            total_page = int(pre_bt.replace('.html','').split('index')[1]) + 1
            input_start = '總頁數：'+ str(total_page) +'，請輸入要下載起始頁數：'
            input_end = '結束頁數：'
            k=1
            break
        else:
            print('請輸入正確網址，或Q退出程式')
    else:
        print('退出程式。')
        break

if k == 1:
    id=0
    while True:
        keyin_start=input(input_start)
        if keyin_start.isdigit() and (int(keyin_start)<=total_page):
            keyin_end=input(input_end)
            if (keyin_end) == ('q' or 'Q'):
                print('退出程式。')
                break

            elif keyin_end.isdigit() and (int(keyin_end)<=total_page):
                keyin_start = int(keyin_start)
                keyin_end = int(keyin_end)
                if (keyin_start - keyin_end) >= 0:
                    page = keyin_start
                    break
                elif (keyin_start - keyin_end) < 0:
                    page=keyin_end
                    break
            else:
                print('請輸入範圍內正整數，或Q退出程式')
        elif (keyin_start) == ('q' or 'Q'):
            print('退出程式。')
            break
        else:
            print('請輸入範圍內正整數，或Q退出程式')

    path = os.path.expanduser('~') + '\\Desktop\\' + file_name.replace('\\', '\'反斜\'').replace('/', '／').replace('?','？') \
        .replace(':', '：').replace('*', '＊').replace('\"', '＂').replace('<', '＜').replace('>', '＞').replace('|', '｜')
    if not os.path.exists(path):
        os.mkdir(path)
    path = path + '\\'
    print('存放位置：' + path)

    try:
        if keyin_start >= keyin_end:
            download_num = keyin_start - keyin_end
        else:
            download_num = keyin_end - keyin_start

        pre_url = pre_url.split('/')
        pre_url[-1] = 'index{}.html'

        for ran in range(download_num + 1):
            url = '/'.join(pre_url)
            req = requests.post(url=url.format(page), headers=headers,cookies=cookies)
            soup = BeautifulSoup(req.text, 'html.parser')
            tweety=0
            for tweety in range(20):
                try:
                    new_url = 'https://www.ptt.cc/' + soup.select('div[class="title"]')[tweety]('a')[0]['href']
                    new_req = requests.post(url=new_url, headers=headers,cookies=cookies)
                    new_soup = BeautifulSoup(new_req.text,'html.parser')


                    title = new_soup.select('div[class="article-metaline"] span')
                    author = title[0].text + ': ' + title[1].text
                    label = title[2].text + ': ' + title[3].text
                    post_time = title[4].text + ': ' + title[5].text

                    push_like = new_soup.select('div[class="push"] span')
                    j = 0;
                    push_list = []
                    for i in push_like:
                        if j % 4 == 0:
                            push_list += push_like[j].text
                        else:
                            pass
                        j += 1

                    like = push_list.count('推')
                    dislike = push_list.count('噓')

                    content = new_soup.select('div[id="main-container"]')

                    tit = str(page)+'n'+str(tweety+1) + ''.join([title.text for title in title[0:6]]).replace(':', '')

                    with open(path +'{}.txt'.format(tit), 'w', encoding='utf-8') as f:
                        f.write(
                            content[0].text.split('※ 發信站')[0] + '\n---split---' + '\n' +
                            '推： ' + str(like) + '\n' +
                            '噓： ' + str(dislike) + '\n' +
                            '分數： ' + str(like - dislike) + '\n' +
                            author + '\n' +
                            label + '\n' +
                            post_time)

                    id+=1
                    sql = 'INSERT INTO testetl (id,num,content) VALUES ({},{},"{}");'.format(id,page,content[0].text.split('※ 發信站')[0])
                    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()

                except IndexError as e:
                    tit = str(page)+'n'+str(tweety+1) + str(e)
                    with open(path +'{}.txt'.format(tit), 'w', encoding='utf-8') as f:
                        f.write(
                            content[0].text.split('※ 發信站')[0] + '\n---split---' + '\n' +
                            '推： ' + str(like) + '\n' +
                            '噓： ' + str(dislike) + '\n' +
                            '分數： ' + str(like - dislike) + '\n' +
                            author + '\n' +
                            label + '\n' +
                            post_time)

                    id += 1
                    sql = 'INSERT INTO testetl (id,num,content) VALUES ({},{},"{}");'.format(id, page,
                                                                                             content[0].text.split(
                                                                                                 '※ 發信站')[0])
                    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()

                except OSError:
                    tit=tit.replace('\\','\'反斜\'').replace('/','／').replace('?','？').replace(':','：').replace('*','＊')\
                        .replace('\"','＂').replace('<','＜').replace('>','＞').replace('|','｜')
                    with open(path +'{}.txt'.format(tit), 'w', encoding='utf-8') as f:
                        f.write(
                            content[0].text.split('※ 發信站')[0] + '\n---split---' + '\n' +
                            '推： ' + str(like) + '\n' +
                            '噓： ' + str(dislike) + '\n' +
                            '分數： ' + str(like - dislike) + '\n' +
                            author + '\n' +
                            label + '\n' +
                            post_time)

                    id += 1
                    sql = 'INSERT INTO testetl (id,num,content) VALUES ({},{},"{}");'.format(id, page,
                                                                                             content[0].text.split(
                                                                                                 '※ 發信站')[0])
                    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()

                tweety += 1
            page-=1
        print('程式結束。')

    except:
        print('程式結束。')
else:
    print('程式結束')