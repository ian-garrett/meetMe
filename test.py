import main
import nose
import arrow
import datetime


##### NOSE TEST SUITE INCLUDES:
# - 1 one-event test
# - 7 two-event tests to check all base cases for two events with various types of overlap
# - 2 complete distaster tests
#####



def testCase1():
	# test case to test one event
    entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T11:00:00-08:00')}
    entryList = [entry1]
    startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

    expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T11:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

    expected = ''.join(expected)
    assert resultingFreeTimes == expected


def testCase2():
	# test case to check easiest two-event system: two non-overlapping events
    entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T11:00:00-08:00')}
    entry2 = {'start':arrow.get('2015-12-10T14:00:00-08:00'), 'end':arrow.get('2015-12-10T15:00:00-08:00')}
        
    entryList = [entry1,entry2]
    startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

    expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T11:00:00-08:00]>, <Arrow [2015-12-10T14:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T15:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

    expected = ''.join(expected)
    assert resultingFreeTimes == expected


def testCase3():
	# test case to check two-event system where both entries have the same start and the second event ends before the first event ends
    entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T12:00:00-08:00')}
    entry2 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T15:00:00-08:00')}
        
    entryList = [entry1,entry2]
    startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

    print("RESULTING")
    print(resultingFreeTimes)

    expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T15:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

    expected = ''.join(expected)
    assert resultingFreeTimes == expected

def testCase4():
	# test case to check two-event system where both entries have the same start and the first event ends before the second event ends
    entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T18:00:00-08:00')}
    entry2 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T11:00:00-08:00')}
        
    entryList = [entry1,entry2]
    startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

    print("RESULTING")
    print(resultingFreeTimes)

    expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T18:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

    expected = ''.join(expected)
    assert resultingFreeTimes == expected

def testCase5():
	# test case to check two-event system where the second entry is engulfed in the first entry
    entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T18:00:00-08:00')}
    entry2 = {'start':arrow.get('2015-12-10T12:00:00-08:00'), 'end':arrow.get('2015-12-10T15:00:00-08:00')}
        
    entryList = [entry1,entry2]
    startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

    print("RESULTING")
    print(resultingFreeTimes)

    expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T18:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

    expected = ''.join(expected)
    assert resultingFreeTimes == expected

def testCase6():
	# test case to check two-event system where first event end is equal to second event start
    entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T14:00:00-08:00')}
    entry2 = {'start':arrow.get('2015-12-10T14:00:00-08:00'), 'end':arrow.get('2015-12-10T18:00:00-08:00')}
        
    entryList = [entry1,entry2]
    startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

    print("RESULTING")
    print(resultingFreeTimes)

    expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T18:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

    expected = ''.join(expected)
    assert resultingFreeTimes == expected

def testCase7():
	# test case to check two-event system where two events have the same start and end
    entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T14:00:00-08:00')}
    entry2 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T14:00:00-08:00')}
        
    entryList = [entry1,entry2]
    startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

    print("RESULTING")
    print(resultingFreeTimes)

    expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T14:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

    expected = ''.join(expected)
    assert resultingFreeTimes == expected

def testCase8():
	# test case to check two-event system where the first event start is before the second end start and both events have the same end
    entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T14:00:00-08:00')}
    entry2 = {'start':arrow.get('2015-12-10T12:00:00-08:00'), 'end':arrow.get('2015-12-10T14:00:00-08:00')}
        
    entryList = [entry1,entry2]
    startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
    resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

    print("RESULTING")
    print(resultingFreeTimes)

    expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
    			"[<Arrow [2015-12-10T14:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

    expected = ''.join(expected)
    assert resultingFreeTimes == expected


def testCase9():
	# cluster f*ck test # 1: creates cluster f*ck within single day
	entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T12:00:00-08:00')}
	entry2 = {'start':arrow.get('2015-12-10T11:00:00-08:00'), 'end':arrow.get('2015-12-10T14:00:00-08:00')}
	entry3 = {'start':arrow.get('2015-12-10T09:00:00-08:00'), 'end':arrow.get('2015-12-10T11:00:00-08:00')}
	entry4 = {'start':arrow.get('2015-12-10T15:00:00-08:00'), 'end':arrow.get('2015-12-10T16:00:00-08:00')}
	entry5 = {'start':arrow.get('2015-12-10T14:00:00-08:00'), 'end':arrow.get('2015-12-10T18:00:00-08:00')}
	    
	entryList = [entry1,entry2,entry3,entry4,entry5]
	startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
	endDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
	resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

	print("RESULTING")
	print(resultingFreeTimes)

	expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T09:00:00-08:00]>], ",
				"[<Arrow [2015-12-10T18:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>]]"]

	expected = ''.join(expected)
	assert resultingFreeTimes == expected


def testCase10():
	# cluster f*ck test # 1: creates cluster f*ck over several days
	entry1 = {'start':arrow.get('2015-12-10T10:00:00-08:00'), 'end':arrow.get('2015-12-10T12:00:00-08:00')}
	entry2 = {'start':arrow.get('2015-12-10T11:00:00-08:00'), 'end':arrow.get('2015-12-10T14:00:00-08:00')}
	entry3 = {'start':arrow.get('2015-12-11T09:00:00-08:00'), 'end':arrow.get('2015-12-11T11:00:00-08:00')}
	entry4 = {'start':arrow.get('2015-12-11T15:00:00-08:00'), 'end':arrow.get('2015-12-11T16:00:00-08:00')}
	entry5 = {'start':arrow.get('2015-12-13T14:00:00-08:00'), 'end':arrow.get('2015-12-13T18:00:00-08:00')}
	entry6 = {'start':arrow.get('2015-12-13T09:00:00-08:00'), 'end':arrow.get('2015-12-13T12:00:00-08:00')}
	    
	# entryList = [entry1,entry2,entry3,entry4,entry5]
	entryList = [entry1,entry2,entry3,entry4,entry5]
	startDate = arrow.get('2015-12-10T00:00:00-08:00').isoformat()
	endDate = arrow.get('2015-12-13T00:00:00-08:00').isoformat()
	resultingFreeTimes = str(main.generateFreeTimes(entryList,startDate,endDate))

	print("RESULTING")
	print(resultingFreeTimes)

	expected = ["[[<Arrow [2015-12-10T07:00:00-08:00]>, <Arrow [2015-12-10T10:00:00-08:00]>], ",
				"[<Arrow [2015-12-10T14:00:00-08:00]>, <Arrow [2015-12-10T21:00:00-08:00]>], ",
				"[<Arrow [2015-12-11T07:00:00-08:00]>, <Arrow [2015-12-11T09:00:00-08:00]>], ",
				"[<Arrow [2015-12-11T11:00:00-08:00]>, <Arrow [2015-12-11T15:00:00-08:00]>], ",
				"[<Arrow [2015-12-11T16:00:00-08:00]>, <Arrow [2015-12-11T21:00:00-08:00]>], ",
				"[<Arrow [2015-12-12T07:00:00-08:00]>, <Arrow [2015-12-12T21:00:00-08:00]>], ",
				"[<Arrow [2015-12-13T07:00:00-08:00]>, <Arrow [2015-12-13T14:00:00-08:00]>], ",
				"[<Arrow [2015-12-13T18:00:00-08:00]>, <Arrow [2015-12-13T21:00:00-08:00]>]]"]

	expected = ''.join(expected)
	assert resultingFreeTimes == expected
