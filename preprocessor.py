import re
import pandas as pd


# it takes a string data (all the info in chat) and converts
# it into a pandas dataframe and returns it
def preprocess(data):

    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern,data)[1:]
    date = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': message, 'message_date': date})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ', errors='coerce')
    # date_time() function is used to convert a column to customized defined date_time format
    df.rename(columns={'message_date': 'date'})

    user = []
    messages = []

    for message in df['user_message']:
        pattern = '([\w\W]+?):\s'
        entry = re.split(pattern, message)
        # will give the user_message and name split on the basis of :\s
        if entry[1:]:  # [1:] to skip the "" empty string
            # if it is a valid message (split on the basis of :\s)
            user.append(entry[1])
            messages.append(entry[2])
        else:
            # if invalid message like "the media file has been omitted"
            user.append('group notification')
            messages.append(entry[0])

    df['user'] = user
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute
    # df.drop(columns=['message_date'], inplace=True)

    return df
