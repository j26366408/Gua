"""Achievement grading: the first four booleans award 20 points each."""
import json

def grade(results, system_works=True):
    if len(results)!=4 or any(type(v) is not bool for v in results):
        raise ValueError('Exactly four boolean results are required.')
    points=[20 if value else 0 for value in results]
    return {'questions_1_to_4':points,'question_5':20 if system_works else 0,'total':sum(points)+(20 if system_works else 0)}

if __name__=='__main__':
    outcomes=[]
    for i in range(1,5):
        while True:
            raw=input(f'Question {i} achieved? (y/n): ').strip().lower()
            if raw in ('y','n'):
                outcomes.append(raw=='y'); break
            print('Please enter y or n.')
    print(json.dumps(grade(outcomes),indent=2))
