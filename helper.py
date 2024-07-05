from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selected_user, df, extractor=None):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # if we are analyzing a specific user then we need to update out dataframe to only messages sent by that user

    # 1. fetch total no of messages
    num_messages = df.shape[0]

    # 2. fetch total no. of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. fetch no. of media messages
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. fetch no. of links
    extractor = URLExtract()
    cnt_links = 0

    for message in df['message']:
        url_list = extractor.find_urls(message)
        if not url_list:
            cnt_links += 1

    return num_messages, len(words), num_media, cnt_links


def most_busy_users(df):
    x = df['user'].value_counts().head()
    percentage = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    percentage.rename(columns={'count': 'percentage'})
    return x, percentage


def remove_stop_words(message):
    f = open('stop_hinglish_words.txt', 'r')
    stop_words = f.read()
    y = []
    for word in message.lower().split():
        if word not in stop_words:
            y.append(word)
    return " ".join(y)  # this will again form the message from the words in y


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    new_df = df[df['user'] != 'group notification']
    new_df = df[df['message'] != '<Media omitted>\n']

    new_df['message'] = new_df['message'].apply(remove_stop_words)
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(new_df['message'].str.cat(sep=" "))
    # df_wc will be an image generated from df['message']
    # .str.cat(sep=" ") will break massages into words and place them in the image
    return df_wc


# abusive_lang = ['gandu', 'lund', 'loda', 'lodu', 'bc', 'bhenchod', 'bhnchod', 'lawde', 'chutiyap', 'aad', 'aand',
#                 'bahenchod', 'behenchod',
#                 'bhenchod', 'bhenchodd', 'b.c.', 'bc', 'bakchod', 'bakchodd', 'bakchodi', 'bevda', 'bewda', 'bevdey',
#                 'bewday', 'bevakoof',
#                 'bevkoof', 'bevkuf', 'bewakoof', 'bewkoof', 'bewkuf', 'bhadua', 'bhaduaa', 'bhadva', 'bhadvaa',
#                 'bhadwa', 'bhadwaa', 'bhosada',
#                 'bhosda', 'bhosdaa', 'bhosdike', 'bhonsdike', 'bsdk', 'bhosdiki', 'bhosdiwala', 'bhosdiwale',
#                 'bhosadchodal', 'bhosadchod',
#                 'bhosadchodal', 'bhosadchod', 'babbe', 'babbey', 'bube', 'bubey', 'bur', 'burr', 'buurr', 'buur',
#                 'charsi', 'chooche', 'choochi',
#                 'chuchi', 'chod', 'chodd', 'chudne', 'chudney', 'chudwa', 'chudwaa', 'chudwane', 'chudwaane',
#                 'choot', 'chut', 'chute',
#                 'chutia', 'chutiya', 'chutiye', 'chuttad', 'chutad', 'dalaal', 'dalal', 'dalle', 'dalley', 'fattu',
#                 'gadha', 'gadhe', 'gadhalund',
#                 'gaand', 'gand', 'gandu', 'gandfat', 'gandfut', 'gandiya', 'gandiye', 'goo', 'gu', 'gote', 'gotey',
#                 'gotte', 'hag', 'haggu',
#                 'hagne', 'hagney', 'harami', 'haramjada', 'haraamjaada', 'haramzyada', 'haraamzyaada', 'haraamjaade',
#                 'haraamzaade',
#                 'haraamkhor', 'haramkhor', 'jhat', 'jhaat', 'jhaatu', 'jhatu', 'kutta', 'kutte', 'kuttey', 'kutia',
#                 'kutiya', 'kuttiya', 'kutti',
#                 'landi', 'landy', 'laude', 'laudey', 'laura', 'lora', 'lauda', 'ling', 'loda', 'lode', 'lund',
#                 'laundi', 'loundi', 'laundiya', 'loundiya', 'lulli', 'madarchod',
#                 'madarchodd', 'madarchood',
#                 'madarchoot', 'madarchut', 'mc', 'mamme', 'mammey', 'moot', 'mut', 'mootne', 'mutne', 'mooth', 'muth',
#                 'nunni', 'nunnu', 'paaji',
#                 'paji', 'pesaab', 'pesab', 'peshaab', 'peshab', 'pilla', 'pillay', 'pille', 'pilley', 'pisaab', 'pisab',
#                 'pkmkb', 'porkistan',
#                 'raand', 'rand', 'randi', 'randy', 'suar', 'tatte', 'tatti', 'tatty', 'ullu','bandi']


# def abusive(df):
#     temp = df[df['user'] != 'group notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']
#
#     temp['message'] = temp['message'].apply(remove_stop_words)
#
#     my_dict = {user: 0 for user in temp['user'].unique()}
#
#     for index, data in temp.iterrows():
#         msg = data['message']
#         user = data['user']
#
#         # Check if any word in the message is in the gaali list
#         for word in msg.split():
#             if word.lower() in abusive_lang:
#                 my_dict[user] += 1

    # Convert the dictionary to a DataFrame
    # Dataframe needs list t=so we have to convert the dictionary values to list
    # new_df = pd.DataFrame({'user': list(my_dict.keys()), 'count': list(my_dict.values())})
    #
    # return new_df


# def individual_abusive(selected_user, df):
#     df = df[df['user'] == selected_user]
#
#     temp = df[df['user'] != 'group notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']
#
#     temp['message'] = temp['message'].apply(remove_stop_words)
#
#     indiv_abusive = {}
#
#     for message in temp['message']:
#         for word in message.split():
#             if word in abusive_lang:
#                 indiv_abusive[word] = indiv_abusive.get(word, 0) + 1
#                 # if the word is in dictionary then .get will return
#                 # its count otherwise it will return 0
#
#     df_abusive = pd.DataFrame(list(indiv_abusive.items()), columns=['word', 'count'])
#
#     return df_abusive


def most_common_words(selected_user, df):
    f = open('stop_hinglish_words.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    temp['message'] = temp['message'].apply(remove_stop_words)
    words = []
    del_word_list = ['<this', 'edited>', 'message', 'deleted']
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and len(word) > 3 and word[0] != '@' and word not in del_word_list:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        for ch in message:
            if emoji.is_emoji(ch):
                emojis.extend(ch)

    df_emoji = pd.DataFrame(Counter(emojis).most_common())

    return df_emoji


def timeline_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['month_num'] = df['message_date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for index, val in timeline.iterrows():
        time.append(val['month'] + "-" + str(val['year']))

    timeline['time'] = time

    return timeline

def word_search(word,df):

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    temp['message'] = temp['message'].apply(remove_stop_words)

    my_dict = {}

    for index, row in temp.iterrows():
        if word.lower() in row['message'].lower().split():
            user = row['user']
            my_dict[user] = my_dict.get(user, 0) + 1

    search_df = pd.DataFrame(list(my_dict.items()),columns=['user','count'])
    return search_df
