from datetime import datetime, timedelta

def solve():
    moments = []
    for _ in range(2):
        line = input().strip()
        
        parts = line.split(' ')
        date_str = parts[0]
        offset_str = parts[1].replace('UTC', '')
        
        
        local_time = datetime.strptime(date_str, "%Y-%m-%d")
        
       
        sign = 1 if offset_str[0] == '+' else -1
        h, m = map(int, offset_str[1:].split(':'))
        offset_delta = timedelta(hours=h, minutes=m)
        
        if sign == 1:
            utc_moment = local_time - offset_delta
        else:
            utc_moment = local_time + offset_delta
            
        moments.append(utc_moment)

    diff = abs((moments[1] - moments[0]).total_seconds())
    print(int(diff // 86400))

solve()