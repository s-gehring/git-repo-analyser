import logging
from math import floor
from subprocess import Popen, PIPE
from typing import List

import git
from git import Repo, Commit

import args


def get_datapoints(all_commits: List[Commit], n: int) -> List[Commit]:
    if n >= len(all_commits):
        return all_commits
    if n < 1:
        return []
    every = len(all_commits) / n
    result = []
    for i in range(n):
        result.append(all_commits[floor(i * every)])
    return result


def analyse_commit(command: str, directory: str) -> str:
    process = Popen(command, stdout=PIPE, stderr=PIPE, cwd=directory)
    process.wait()
    stdout, stderr = process.communicate()

    if len(stderr) > 0:
        logging.error("Foreign process threw error: %s", stderr)

    return stdout.decode("utf-8")


def main():
    logging.basicConfig(level=logging.DEBUG, force=True)

    arguments = args.get_args()
    branch: str = arguments.branch
    directory: str = arguments.dir
    num_data_points: int = arguments.n
    command: str = arguments.command

    repo = Repo(directory)

    if repo.is_dirty():
        raise Exception("Target repository is dirty. Please discard or commit your changes first.")
    logging.debug("Repository is not dirty. Proceeding to analyse branch %s", branch)

    all_commits = [commit for commit in repo.iter_commits(rev=branch)]
    logging.info("Found %d commits.", len(all_commits))
    datapoints: List[Commit] = get_datapoints(all_commits, num_data_points)
    logging.info("Found %d out of requested %d relevant datapoints.", len(datapoints), num_data_points)

    results = []
    for commit in datapoints:
        repo.git.checkout(commit.hexsha)
        stdout = analyse_commit(command, directory).strip()
        results.append({
            "commit": commit.hexsha,
            "message": commit.message.strip(),
            "result": stdout
        })
    results.reverse()

    logging.info("Results: %s", results)


if __name__ == '__main__':
    main()
