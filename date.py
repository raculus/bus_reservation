from datetime import datetime, timedelta

def getBusDays():
    today = datetime.today()
    week = today.weekday()
    if(week == 4 or week == 6):
        today += timedelta(days=1)
    
    dateList = []
    date = today
    for i in range(8):        
        date += timedelta(days=1) #1일씩 증가
        year = date.year
        month = date.month
        day = date.day
        week = date.weekday()

        if(week == 4 or week == 6):
            strDate = '{}-{:02d}-{:02d}'.format(year, month, day)
            dateList.append(strDate)
        if(len(dateList) >= 2):
            break
    return dateList