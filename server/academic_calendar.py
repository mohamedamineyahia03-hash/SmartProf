"""Tunisian primary-school trimester calendar, used by the session engine (Phase 3)
to know which trimester's curriculum to draw exercises from.

Dates are sourced from the Ministry of Education's official 2026-2027 school year
announcement (31 August 2026): school starts 15 Sept 2026, winter break 14-27 Dec
2026, spring break 15-28 March 2027, school year ends 30 June 2027. The Ministry
publishes new boundaries every year, so TRIMESTER_DATES must be updated at the
start of each school year — it is not a fixed rule.
"""

from datetime import date

SCHOOL_YEAR = "2026-2027"

TRIMESTER_DATES = {
    "T1": (date(2026, 9, 15), date(2026, 12, 13)),
    "T2": (date(2026, 12, 28), date(2027, 3, 14)),
    "T3": (date(2027, 3, 29), date(2027, 6, 30)),
}

TRIMESTER_ORDER = ["T1", "T2", "T3"]


def current_trimester(on_date=None):
    """Returns 'T1'/'T2'/'T3' for the given date (defaults to today). During a
    school break between two trimesters, returns whichever trimester's boundary
    is closer in time."""
    on_date = on_date or date.today()
    ordered = sorted(TRIMESTER_DATES.items(), key=lambda item: item[1][0])

    for trimester, (start, end) in ordered:
        if start <= on_date <= end:
            return trimester

    if on_date < ordered[0][1][0]:
        return ordered[0][0]
    if on_date > ordered[-1][1][1]:
        return ordered[-1][0]

    for (trimester_before, (_, end_before)), (trimester_after, (start_after, _)) in zip(ordered, ordered[1:]):
        if end_before < on_date < start_after:
            gap_before = (on_date - end_before).days
            gap_after = (start_after - on_date).days
            return trimester_before if gap_before <= gap_after else trimester_after

    return ordered[-1][0]


def is_trimester_unlocked(trimester, on_date=None):
    """A trimester section unlocks once the calendar reaches it — progressive
    release, so a section tree never lets a child jump ahead to material not
    yet taught in class. Once unlocked it stays unlocked (past trimesters
    remain available for revision). Anything outside T1/T2/T3 (e.g. an
    "expression" section, which has no trimester) is never gated."""
    if trimester not in TRIMESTER_ORDER:
        return True
    return TRIMESTER_ORDER.index(trimester) <= TRIMESTER_ORDER.index(current_trimester(on_date))
