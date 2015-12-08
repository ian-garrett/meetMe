import main
import nose
import arrow
import datetime




def testCase1():
    entry1 = {'start':arrow.get('2015-12-04T10:00:00-08:00'), 'end':arrow.get('2015-12-04T11:00:00-08:00')}
        
    # data = [entry1,entry2,entry3,entry4]
    data = [entry1]
    startDate = arrow.get('2015-12-04T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(data,startDate,endDate))
    
    print(resultingFreeTimes)
    assert freeTimes == expected

