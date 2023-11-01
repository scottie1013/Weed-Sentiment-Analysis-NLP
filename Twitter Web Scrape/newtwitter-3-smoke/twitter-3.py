import base64
import datetime
import json
import os
import random
import re
import time
import copyheaders
import pandas
import pymongo
import requests

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"



class Gtwitter():

    search_api = 'https://twitter.com/i/api/graphql/NA567V_8AFwu0cZEkAAKcw/SearchTimeline'
    resulst = []
    def __init__(self,max_page):
        self.max_page = max_page


    def getblog(self,params):



        while 1:

            try:

                cookie =random.choice(cookies)

                sctoken = ''.join(re.findall(r'ct0=(.*?);', cookie)[:1])
                print(sctoken)
                headers = {
                    'Accept': '*/*',
                    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                    'Content-Type': 'application/json',
                    'Cookie': cookie,
                    'Referer': 'https://twitter.com/search?f=live&q=%22blackberry%22%20until%3A2023-06-29%20since%3A2018-06-23&src=typed_query',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
                    'X-Csrf-Token': sctoken,
                    'X-Twitter-Active-User': 'yes',
                    'X-Twitter-Auth-Type': 'OAuth2Session',
                    'X-Twitter-Client-Language': 'en'
                }

                res = requests.get(
                    self.search_api,
                    headers=headers,
                    params=params,
                    timeout=(3,4)
                )
                if 'Rate limit exceeded' in res.text:
                    print(f'Rate limit exceeded')
                    time.sleep(2)
                    continue
                if 'Authorization: Denied by access control' in res.text:
                    print(cookie)
                    print(f'Authorization: Denied by access control')
                    time.sleep(2)
                    cookies.remove(cookie)
                    continue
                if res.status_code != 200:
                    print(res.status_code, res.text)
                    time.sleep(1)
                    continue
                return res.json()

            except Exception as e:

                print(f">>> parse error: {e}")
                time.sleep(1)




    def parse(self,data,keyword,page,find_options):
        try:
            tweets = data.get("data").get("search_by_raw_query").get("search_timeline").get("timeline").get("instructions")[0].get("entries")
        except Exception as e:
            print(f">>> error: {e}")
            time.sleep(1)
            print(data)
            return []
        if tweets is None:
            tweets = []
        print(page,len(tweets[:-2]))
        for it in tweets[:-2]:
            try:
                dic = {}
                dic['关键词'] = keyword
                dt_obj = datetime.datetime.strptime(
                    it['content']['itemContent']['tweet_results']['result']['legacy']['created_at'],
                    '%a %b %d %H:%M:%S %z %Y')
                dic['发表日期'] = dt_obj.astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')
                dic['用户名'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    'name']
                dic['账号id'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    'screen_name']
                a = it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    'screen_name']
                dic['个人主页'] = f'https://twitter.com/{a}'
                dic['发表内容'] = it['content']['itemContent']['tweet_results']['result']['legacy']['full_text']
                sub_content = dic['发表内容'].split("https://")[0]

                if  keyword not in sub_content and f'#{keyword}' in dic['发表内容']:
                    continue
                dic['博文id'] = it['content']['itemContent']['tweet_results']['result']['legacy']['id_str']
                dic['回复数量'] = it['content']['itemContent']['tweet_results']['result']['legacy']["reply_count"]
                dic['转发数量'] = it['content']['itemContent']['tweet_results']['result']['legacy']["retweet_count"]
                dic['点赞数'] = it['content']['itemContent']['tweet_results']['result']['legacy']["favorite_count"]
                dic['引用数量'] = it['content']['itemContent']['tweet_results']['result']['legacy']["quote_count"]
                try:
                    dic['浏览量'] = it['content']['itemContent']['tweet_results']['result']['views']["count"]
                except:
                    dic['浏览量'] = 0
                idd = it['content']['itemContent']['tweet_results']['result']['legacy']['id_str']
                dic['推文链接'] = f'https://twitter.com/Olympics/status/{idd}'
                dic['粉丝数量'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    "followers_count"]
                dic['关注数量'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    "friends_count"]
                dic['地理位置'] = \
                it['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy'][
                    "location"]
                if 'California'.lower() in str(dic['地理位置']).lower():
                    print(page, dic)
                    while 1:
                        try:
                            with open("tepm.txt",'a',encoding='utf-8') as f:
                                f.write(json.dumps(dic))
                                f.write('\n')
                            break
                        except Exception as e:
                            print(f"mongo errro:{e}")
                            time.sleep(1)
            except:
                pass
        return tweets




    def changev(self,text):
        try:
            dt_obj = datetime.datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')
            return dt_obj.astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')

        except Exception as e:
            print(f">>> 时间格式异常： {text}")
            return text

    def blockdata(self,find_options):
        print(date1,date2,find_options)
        cursor = {"p":''}
        # if os.path.exists("nextpage.txt"):
        #     with open("nextpage.txt",'r',encoding='utf-8') as f:
        #         cursor["p"] = f.read().strip()


        for page in range(1,self.max_page):

            try:
                params = {
                    "fieldToggles": '{"withArticleRichContentState":false}',
                    "features": '{"rweb_lists_timeline_redesign_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":false,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_media_download_video_enabled":false,"responsive_web_enhance_cards_enabled":false}',
                    "variables": '{"rawQuery":"'+str(find_options)+' until:'+str(date2)+' since:'+str(date1)+'","cursor":"'+cursor["p"]+'","count":20,"querySource":"typed_query","product":"Latest"}'
                }
                blogInfo = self.getblog(params)

                tweets = self.parse(blogInfo, find_options, page,find_options)
                pagelength = len(tweets)-2
                if 1:
                    if page == 1 and cursor["p"] == "":

                        cursor["p"] = tweets[-1].get("content").get("value")
                    else:
                        instructions = blogInfo.get("data").get("search_by_raw_query").get("search_timeline").get("timeline").get("instructions")[-1]
                        cursor["p"] = instructions.get("entry").get("content").get("value")
                    print(f"下一页：{cursor['p']}")
                if cursor["p"] is None:
                    print('暂无下一页：')
                    break
            except Exception as e:
                print(f"eroro{e}")
                break



def getdaterange(starttime,endtime):
    time_str = []
    start_samp = time.mktime(time.strptime(starttime, '%Y-%m-%d'))
    while True:
        time_str.append(
            (time.strftime('%Y-%m-%d', time.localtime(start_samp)),
             time.strftime('%Y-%m-%d', time.localtime(start_samp+24*60*60)))
        )
        start_samp += 24 * 60 * 60
        if start_samp > time.mktime(time.strptime(endtime, '%Y-%m-%d')):
            break
    return time_str


if  __name__ == "__main__":

    """
    weed/ cannabis/ smoke/ joint/ blunt/ pot/ THC/ CBD/ stoned/ stoner/ bong/ edibles/ marijuana
    """
    cookies_ = """
    AnalleliLa81292----qdgn5305.----grbesatjibaer@hotmail.com----BJzGum60----90ab2e45dcad4788f145de14d33718416520ecf0----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiIyMmYzMzNiY2M0ZGE3ZWVmNTc1ZWRhZGFkY2NlNjYwNzIxYjAzOTA5In1dfQ==
    TarriP16599----zjxcxw593099.----inglishej2@outlook.com----pyGUcR61----d4a17d8b7bed052873e1679259d406b63a5a12bd----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiJkNGExN2Q4YjdiZWQwNTI4NzNlMTY3OTI1OWQ0MDZiNjNhNWExMmJkIn1dfQ==
    EvanaRodge29611----wizbpnc7213166.----muzamasegardx@outlook.com----HXMsVQ75----e1f3400d25309e128548e5836381536fd2968850----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiJlMWYzNDAwZDI1MzA5ZTEyODU0OGU1ODM2MzgxNTM2ZmQyOTY4ODUwIn1dfQ==
    KerriganPa97586----vuwtq39280.----uchiwaelyzw@outlook.com----HiS8Y086----411791804562d704efe47e62f91a18b7e157d7c0----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiI0MTE3OTE4MDQ1NjJkNzA0ZWZlNDdlNjJmOTFhMThiN2UxNTdkN2MwIn1dfQ==
    BuckleyLil21348----hjlok36300.----enajiaphiwe9@hotmail.com----zM67UQ38----b48f7b1fb9548b9805a94321a1be0b66ebda9fce----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiJiNDhmN2IxZmI5NTQ4Yjk4MDVhOTQzMjFhMWJlMGI2NmViZGE5ZmNlIn1dfQ==
    LabertaLam99643----vkztbj880528.----vipiwannerj@hotmail.com----HNcJP562----0ef8f81cdf9474275b3e4389df9052063bbd804b----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiIwZWY4ZjgxY2RmOTQ3NDI3NWIzZTQzODlkZjkwNTIwNjNiYmQ4MDRiIn1dfQ==
    GunterRonn90451----dzmrjmx0088779.----okogwuziobern@outlook.com----C3BSaA60----5f27974ec8f74aabf66a3efed7e599a1595dff65----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiI1ZjI3OTc0ZWM4Zjc0YWFiZjY2YTNlZmVkN2U1OTlhMTU5NWRmZjY1In1dfQ==
    ChyenneKas83270----qdsyayo3807664.----ovilidhiyabu@hotmail.com----4MpxQZ38----e1deb13a11d9e579d37477a3518ff45d43bb5101----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiJlMWRlYjEzYTExZDllNTc5ZDM3NDc3YTM1MThmZjQ1ZDQzYmI1MTAxIn1dfQ==
    DavidDonle13252----ujvjdcb1138719.----ujkebdilr@hotmail.com----bJCQVq29----4d78e4d86ec8381ae5056266863a1b335a803874----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiI0ZDc4ZTRkODZlYzgzODFhZTUwNTYyNjY4NjNhMWIzMzVhODAzODc0In1dfQ==
    MarceyFish18878----zzztdj418275.----samrahleepsr@hotmail.com----9aahqX80----b2751ddb2bde018649faf4f8222a848c0fe73919----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiJiMjc1MWRkYjJiZGUwMTg2NDlmYWY0ZjgyMjJhODQ4YzBmZTczOTE5In1dfQ==
    FilkinsTai47854----zycr5734.----motanahoyer2@hotmail.com----HHggrX22----26678a85553915051712d5210b871e6522fbbdf1----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiIyNjY3OGE4NTU1MzkxNTA1MTcxMmQ1MjEwYjg3MWU2NTIyZmJiZGYxIn1dfQ==
    LaureeNick58784----jrbwg82641.----attaieasbln@hotmail.com----5oCSqt10----4154df091d3470d167f66ef9ebb0785c1cb8c9a7----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiI0MTU0ZGYwOTFkMzQ3MGQxNjdmNjZlZjllYmIwNzg1YzFjYjhjOWE3In1dfQ==
    delaney_ha58807----erwyafu4887149.----jeejafedah3@hotmail.com----MhXcmL10----221e00e6bdbf1424a698d7a2ec5bc95880fa7021----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiIyMjFlMDBlNmJkYmYxNDI0YTY5OGQ3YTJlYzViYzk1ODgwZmE3MDIxIn1dfQ==
    AdelaidaZa9559----eaqku86912.----livematadou@hotmail.com----chUrzx14----8f108f45c8e7ce64edf7ef5cdb4b2556a05ab1b0----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiI4ZjEwOGY0NWM4ZTdjZTY0ZWRmN2VmNWNkYjRiMjU1NmEwNWFiMWIwIn1dfQ==
    DarchelleG13424----ogqmbsj7316200.----dheerubulfinv@hotmail.com----vQMoMp53----79c7f81e2b621ce31b0bb0ad423d7ba9187297ea----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiI3OWM3ZjgxZTJiNjIxY2UzMWIwYmIwYWQ0MjNkN2JhOTE4NzI5N2VhIn1dfQ==
    5Catori4232----ebphj50042.----aizaankalovax@outlook.com----AZKAG639----54c193394dd6e65525272631d87b3b59078507a8----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiI1NGMxOTMzOTRkZDZlNjU1MjUyNzI2MzFkODdiM2I1OTA3ODUwN2E4In1dfQ==
    ChantalFio10364----saakgvu6580025.----kobeakivancp@hotmail.com----1eB1v945----5e7029561a087d25cee416b5a8183e3e7b48f3fb----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiIwNDgzNWIwNDdhYmNkNDJmNDY2ZWJmNWExY2Q0MzdkMzM2OWJlNmI2In1dfQ==
    ChealseaTa66620----oldd7927.----rochdysreijo@hotmail.com----43K8Px99----e71f1b370e883eb2a115da1828a498526764ea83----eyJjb29raWVzIjpbeyJkb21haW4iOiIudHdpdHRlci5jb20iLCJleHBpcmVzIjoxODM4NDQyNDI4LjY4OTk3NjksImh0dHBPbmx5Ijp0cnVlLCJuYW1lIjoiYXV0aF90b2tlbiIsInBhdGgiOiJcLyIsInByaW9yaXR5IjoiTWVkaXVtIiwic2FtZVBhcnR5IjpmYWxzZSwic2FtZVNpdGUiOiJOb25lIiwic2VjdXJlIjp0cnVlLCJzZXNzaW9uIjpmYWxzZSwic2l6ZSI6NTAsInNvdXJjZVBvcnQiOjQ0Mywic291cmNlU2NoZW1lIjoiU2VjdXJlIiwidmFsdWUiOiJlNzFmMWIzNzBlODgzZWIyYTExNWRhMTgyOGE0OTg1MjY3NjRlYTgzIn1dfQ==
    """


    cookies = [i.split("----")[-2] for i in cookies_.split('\n') if i.strip() != ""]

    print(cookies)
    cookies = [
        f'auth_token={ij};ct0=751625f00f47931b5028562249417d78;'
         for ij in cookies
    ]
    daets = getdaterange("2018-03-18",'2023-07-01')[::-1]
    for date1,date2 in daets:
        tt = Gtwitter(500)
        tt.blockdata("smoke")


#
