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
            return 0
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



    def generXlsx(self):
        try:
            with open("temp_first2.txt", 'r', encoding='utf-8') as f:
                resulst = [json.loads(i.strip()) for i in f.readlines()]

            pandas.DataFrame(resulst).to_excel(f"result2-{int(time.time())}.xlsx",index=False)
        except Exception as e:
            print(f">>> 拉取数据库 error:{e}")

    def changev(self,text):
        try:
            dt_obj = datetime.datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')
            return dt_obj.astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S')

        except Exception as e:
            print(f">>> 时间格式异常： {text}")
            return text

    def blockdata(self,find_options):
        print(date1, date2, find_options)
        cursor = {"p":''}


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
                    with open("nextpage.txt",'w',encoding='utf-8') as f:
                        f.write(cursor["p"])
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
    cookies = [
        '_ga=GA1.2.2001245201.1696121387; kdt=rSVZPNi76RnCpYJ6XHsFr4mHus3Dnfk7kQWtexwk; dnt=1; _gid=GA1.2.805936431.1696667554; auth_multi="1687314223993417728:90ab2e45dcad4788f145de14d33718416520ecf0|1687317782394724352:5e7029561a087d25cee416b5a8183e3e7b48f3fb"; auth_token=ce320b29d04769ef0ba65c782288c36e3c27d21d; guest_id=v1%3A169666874386661403; ct0=49b5ca2d82a386c4c8b3ae8752428a38430813cdbd1808cf2b87f8ab815e43600e5978e9c0e3caa4b1f6c5f699f6e784d7d0bc76c0b462d08c6e8fc91340713a72280b8c3ddb8f1206e037b3125a0728; guest_id_ads=v1%3A169666874386661403; guest_id_marketing=v1%3A169666874386661403; twid=u%3D1706097779951718400; personalization_id="v1_H4Ck5oHiQ8ABhtdhg0Z2lA=="',
        '_ga=GA1.2.2001245201.1696121387; kdt=rSVZPNi76RnCpYJ6XHsFr4mHus3Dnfk7kQWtexwk; lang=en; _gid=GA1.2.805936431.1696667554; dnt=1; auth_multi="1706097779951718400:ce320b29d04769ef0ba65c782288c36e3c27d21d|1687314223993417728:90ab2e45dcad4788f145de14d33718416520ecf0|1687317782394724352:5e7029561a087d25cee416b5a8183e3e7b48f3fb"; auth_token=59edced0a2e0aeff6639c8ddefcd35a57b322f06; guest_id=v1%3A169666884389909009; ct0=d51bfd797c3b7dfdb5a141af3d994726d985dbae8dbdb6c7daceb4303ddb71a85a63c59d8e7d9081b8eb5c3e2efb2c3047b5e46b0dd74b875cc353692f31c03aff90710b7c4a78763998f343d720b5ff; guest_id_ads=v1%3A169666884389909009; guest_id_marketing=v1%3A169666884389909009; twid=u%3D1706099101279076352; personalization_id="v1_izMR3ujDGn+//S8IMNCMRQ=="',
        '_ga=GA1.2.2001245201.1696121387; kdt=rSVZPNi76RnCpYJ6XHsFr4mHus3Dnfk7kQWtexwk; lang=en; _gid=GA1.2.805936431.1696667554; dnt=1; auth_multi="1706099101279076352:59edced0a2e0aeff6639c8ddefcd35a57b322f06|1706097779951718400:ce320b29d04769ef0ba65c782288c36e3c27d21d|1687314223993417728:90ab2e45dcad4788f145de14d33718416520ecf0|1687317782394724352:5e7029561a087d25cee416b5a8183e3e7b48f3fb"; auth_token=3768386c2e7114e1d83e17a626005ed1b0feb084; guest_id=v1%3A169666900048772979; ct0=a67a55e9dffc37ff15d159e5803643e3eaa63b585bac0028dae7d22bd99222176f497b4f0b8858b40e35b902aaeb5e9ead1c0b11fb807b4f12c4bbb840f50679c3ab45688e41ff1f1d416adb09779809; guest_id_ads=v1%3A169666900048772979; guest_id_marketing=v1%3A169666900048772979; personalization_id="v1_iPLOR6QU2SCudt3ShFKdYA=="; twid=u%3D1708403691794173952',
        'guest_id=v1%3A169666906924749250; _ga=GA1.2.1485958329.1696669070; _gid=GA1.2.2037767557.1696669070; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCCx%252BWwmLAToMY3NyZl9p%250AZCIlM2U3NmNhZGRmYjNmZjkxOTdjNjAwMTA2Y2Q2ODAzYzM6B2lkIiU0NTUw%250AODYzZmIzMDAyNGEzM2QxOGFkODBkYThhMWVmMw%253D%253D--7439d0d8586fcf498eb032c92914d8eb532ee617; kdt=WPWphveELWLH8bHoQt0RiHe8HnnUDFSwpDYDGOnd; auth_token=d455bdb1e943c768dd00148cc5feeb643db9e051; ct0=cd4f7eebcc886a4c7d0e12b7cfdbf739dc692d99620794eebdbca1746fd08e71203c434d5fa6f54e53a92985b296a26d8d629881d488a56c76a19f230ec2eba3593416c020bd1c6e6f691acbb5a77624; guest_id_ads=v1%3A169666906924749250; guest_id_marketing=v1%3A169666906924749250; lang=en; personalization_id="v1_t5YyELb6QnJiQ1Nz6tu1vA=="; twid=u%3D1706148813155762176',
        '_ga=GA1.2.1485958329.1696669070; _gid=GA1.2.2037767557.1696669070; kdt=WPWphveELWLH8bHoQt0RiHe8HnnUDFSwpDYDGOnd; lang=en; dnt=1; auth_multi="1706148813155762176:d455bdb1e943c768dd00148cc5feeb643db9e051"; auth_token=1e1ba37364a69f519de25944798d223192ccdf48; guest_id=v1%3A169666921455541788; ct0=a7cc61bb9a629335da7b873c530650b563e0f8b2d41f83d628e35a77257bee9c4cd9361ef23d1fe82f484a7480710353911601d6fa264201cc9bc8211e23437eecbb21dfdfdcbc7274ea234f2537bb34; guest_id_ads=v1%3A169666921429046044; guest_id_marketing=v1%3A169666921429046044; personalization_id="v1_YHxPKNY2fgUQitAD7H6lPQ=="; twid=u%3D1708460456044789760'
    ]
    cookies = [
        ij
         for ij in cookies
    ]

    daets = getdaterange("2020-01-01",'2020-09-28')[::-1]
    for date1,date2 in daets:
        tt = Gtwitter(500)
        tt.blockdata("marijuana")

#
