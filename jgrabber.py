import hashlib
import json
import re

from jenkinsapi.jenkins import Jenkins


def get_jobs(server):
    j = Jenkins(server)
    jobs = []
    for job in j.get_jobs():
        jobs.append(job[0])
    return jobs


def get_job_tests(server, job_name):
    j = Jenkins(server)

    job = j[job_name]
    builds = job.get_build_ids()

    tests = set()
    crap = {}

    for build_num in builds:
        build = job.get_build(build_num)

        if build.is_good():
            continue

        try:
            resultset = build.get_resultset()
            results = resultset.items()
        except Exception, e:
            print 'Exception build #%s' % build_num
            continue

        for result in results:
            if result[1].status == 'FAILED':
                tests.add(result[0])
                try:
                    crap[result[0]].append(build_num)
                except KeyError:
                    crap[result[0]] = [build_num]

    return list(tests)


def get_test_data(server, job_name, test):
    j = Jenkins(server)

    job = j[job_name]
    builds = job.get_build_ids()

    ret_val = {
        'name': job_name,
        'total': 0,
        'passed': 0,
        'failed': 0,
        'errors': {},
    }

    for build_num in builds:
        build = job.get_build(build_num)
        ret_val['total'] += 1

        if not build.is_good():
            ret_val['failed'] += 1
            try:
                resultset = build.get_resultset()
                for result in resultset.items():
                    if result[0] == test and (result[1].status == 'FAILED' or 'REGRESSION'):
                        error = normalize(result[1].errorStackTrace)

                        md5 = hashlib.md5(error)
                        key = md5.hexdigest()
                        try:
                            ret_val['errors'][key]['count'] += 1
                            ret_val['errors'][key]['builds'].append(build_num)
                        except:
                            ret_val['errors'][key] = {
                                'stacktrace': error,
                                'count': 1,
                                'builds': [build_num],
                            }
                        break
                else:
                    import pdb; pdb.set_trace()
                    error = 'Stupid Error %s' % build_num
                    print error
            except Exception, e:
                error = 'Stupid Error'
        else:
            ret_val['passed'] += 1

    return ret_val


def normalize(stack):
    stack = re.sub(r' (line )(\d+),', r' \1xxx,', stack)
    return stack


def main():
    """
    digboi --server [SERVER] --job [JOB]
    """
    pass


if __name__ == '__main__':
    main()
