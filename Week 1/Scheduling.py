"""
Task1
Your task in this problem is to run the greedy algorithm that schedules jobs in decreasing order of the difference
(weight - length). Recall from lecture that this algorithm is not always optimal.
IMPORTANT: if two jobs have equal difference (weight - length), you should schedule the job with higher weight first.
Beware: if you break ties in a different way, you are likely to get the wrong answer.
You should report the sum of weighted completion times of the resulting schedule --- a positive integer ---
in the box below.
Task2
Your task now is to run the greedy algorithm that schedules jobs (optimally) in decreasing order of the ratio
(weight/length). In this algorithm, it does not matter how you break ties. You should report the sum of weighted
completion times of the resulting schedule --- a positive integer --- in the box below.
"""
from itertools import accumulate


def load_jobs(file_name):
    res = []
    # the size of the file is reasonable for this problem, can speed things up by loading the whole file
    with open(file_name) as data:
        file_contents = data.read()
    # build list of jobs
    lines = file_contents.split('\n')
    _ = lines.pop(0)
    for line in lines:
        spl = line.split()
        if spl:
            weight, length = map(int, spl)
            res.append((weight, length))
    return res


def schedule(jobs_list, sort_key):
    sorted_jobs = sorted(jobs_list, key=sort_key, reverse=True)
    acc_lengths = accumulate(job[1] for job in sorted_jobs)
    weighted_completion_times = (al * job[0] for al, job in zip(acc_lengths, sorted_jobs))
    return sum(weighted_completion_times)

if __name__ == '__main__':
    jobs = load_jobs('jobs.txt')
    print('Difference: {0}'.format(schedule(jobs, lambda t: (t[0] - t[1], t[0]))))
    print('Ratio: {0}'.format(schedule(jobs, lambda t: t[0]/t[1])))
