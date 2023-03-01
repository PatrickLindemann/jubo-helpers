import argparse
from typing import List

from src.routines.routine import Routine
from src.routines.fee_mails.prepare import FeeMailsPrepareRoutine
from src.routines.fee_mails.send import FeeMailsSendRoutine

routines: List[Routine] = [
    FeeMailsPrepareRoutine,
    FeeMailsSendRoutine
]

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'routine',
        choices=[r.get_name() for r in routines]
    )
    parser.add_argument(
        'routine_args',
        nargs=argparse.REMAINDER
    )
    return parser

if __name__ == 'main':
    # Read the arguments and validate them
    parser = get_parser()
    args = parser.parse_args()
    # Get the specified routine and execute it with the other arguments
    routine = next(r for r in routines if r.get_name() == args.routine)
    routine_args = routine.get_parser().parse_args(args.routine_args)
    routine.run(routine_args)