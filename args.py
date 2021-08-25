import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Analyse git project')

parser.add_argument('--dir', type=str, default=".",
                    help='A directory with a git repository')

parser.add_argument('--branch', type=str, default="master",
                    help='The branch to analyse')

parser.add_argument('-n', type=int, default=20,
                    help='Data points to generate')

parser.add_argument("--command", type=str, default="bash -c \"git ls-files | wc -l\"",
                    help="The command to execute for each relevant commit.")


# Required positional argument
#parser.add_argument('pos_arg', type=int,
#                    help='A required integer positional argument')

# Optional positional argument
#parser.add_argument('opt_pos_arg', type=int, nargs='?',
#                    help='An optional integer positional argument')

# Optional argument
#parser.add_argument('--opt_arg', type=int,
#                    help='An optional integer argument')

# Switch
#parser.add_argument('--switch', action='store_true',
#                    help='A boolean switch')

args = parser.parse_args()


def get_args():
    return args
