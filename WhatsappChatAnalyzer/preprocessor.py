import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APap][Mm])?\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    # Reconstruct messages to ensure alignment with dates
    matches = list(re.finditer(pattern, data))

    messages_aligned = []
    for i in range(len(matches)):
        start_index_of_message = matches[i].end()
        if i + 1 < len(matches):
            end_index_of_message = matches[i + 1].start()
        else:
            end_index_of_message = len(data)  # Last message goes to the end of the data

        message_content = data[start_index_of_message:end_index_of_message]
        messages_aligned.append(message_content)

    # Now `messages_aligned` and `dates` should have the same length.
    df = pd.DataFrame({'user_message': messages_aligned, 'message_date': dates})
    # message ke date time ko convert karenge
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    # Check if 'user_message' column exists before processing
    if 'user_message' in df.columns:
        for message in df['user_message']:
            entry = re.split(r'([\w\W]+?):\s', message)

            if entry[1:]:
                users.append(entry[1])
                messages.append(entry[2])
            else:
                users.append('group_notification')
                messages.append(entry[0])

        df['user'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        return df