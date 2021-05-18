from TikTokApi import TikTokApi
import pandas as pd
import datetime


api = TikTokApi.get_instance()
# If playwright doesn't work for you try to use selenium
# api = TikTokApi.get_instance(use_selenium=True)

results = 100000
search_term = "mlb"

# Since TikTok changed their API you need to use the custom_verifyFp option.
# In your web browser you will need to go to TikTok, Log in and get the s_v_web_id value.

#trending = api.trending(count=results, custom_verifyFp="")
#trending = api.by_hashtag(search_term, count=results, custom_verifyFp="")
trending = api.by_username(search_term, count=results, custom_verifyFp="")

def simple_dict(tiktok_dict):
  to_return = {}
  to_return['user_name'] = tiktok_dict['author']['uniqueId']
  to_return['user_id'] = tiktok_dict['author']['id']
  to_return['video_id'] = tiktok_dict['id']
  to_return['video_desc'] = tiktok_dict['desc']
  to_return['video_time'] = tiktok_dict['createTime']
  to_return['video_length'] = tiktok_dict['video']['duration']
  to_return['video_link'] = 'https://www.tiktok.com/@{}/video/{}?lang=en'.format(to_return['user_name'], to_return['video_id'])
  to_return['n_likes'] = tiktok_dict['stats']['diggCount']
  to_return['n_shares'] = tiktok_dict['stats']['shareCount']
  to_return['n_comments'] = tiktok_dict['stats']['commentCount']
  to_return['n_plays'] = tiktok_dict['stats']['playCount']
  return to_return


output = pd.DataFrame()

for tiktok in trending:
    tiktok_clean = simple_dict(tiktok)
    output = output.append(tiktok_clean, ignore_index=True)

#Get Time
caption_created_time = []
i = 0
for i in output['video_time']:
    value = datetime.datetime.fromtimestamp(int(i)).strftime('%Y-%m-%d %H:%M:%S')
    caption_created_time.append(value)
    i = i + 1

output['date'] = caption_created_time


writer = pd.ExcelWriter("TikTok_{}_user.xlsx".format(search_term), engine='xlsxwriter')
output.to_excel(writer, index=False)
writer.save()
