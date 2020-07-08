from parsec import *
from datetime import datetime, timedelta
from dateutil.parser import parse
from mobilitydb.time import Period, PeriodSet
from mobilitydb.temporal import Temporal
from mobilitydb.temporal.temporal_parser import parse_temporalinst


class TemporalInst(Temporal):
    """
    Abstract class for representing temporal values of instant duration.
    """
    __slots__ = ['_value', '_time']

    def __init__(self, value, time=None):
        if(time is None):
            # Constructor with a single argument of type string
            if isinstance(value, str):
                couple = parse_temporalinst(value, 0)
                value = couple[2][0]
                time = couple[2][1]
            # Constructor with a single argument of type tuple or list
            elif isinstance(value, (tuple, list)):
                value, time = value
            else:
                raise Exception("ERROR: Could not parse temporal instant value")
        # Now both value and time are not None
        assert(isinstance(value, (str, type(self).BaseClass))), "ERROR: Invalid value argument"
        assert(isinstance(time, (str, datetime))), "ERROR: Invalid time argument"
        self.getValue = type(self).BaseClass(value) if isinstance(value, str) else value
        self.getTimestamp = parse(time) if isinstance(time, str) else time

    @classmethod
    def duration(cls):
        """
        Duration of the temporal value, that is, ``'Instant'``.
        """
        return "Instant"

    @property
    def getValue(self):
        """
        Value component.
        """
        return self.getValue

    @property
    def getValues(self):
        """
        List of distinct values.
        """
        return [self.getValue]

    @property
    def startValue(self):
        """
        Start value.
        """
        return self.getValue

    @property
    def endValue(self):
        """
        End value.
        """
        return self.getValue

    @property
    def minValue(self):
        """
        Minimum value.
        """
        return self.getValue

    @property
    def maxValue(self):
        """
        Maximum value.
        """
        return self.getValue

    @property
    def getTimestamp(self):
        """
        Timestamp.
        """
        return self.getTimestamp

    @property
    def getTime(self):
        """
        Period set on which the temporal value is defined.
        """
        return PeriodSet({Period(self.getTimestamp, self.getTimestamp, True, True)})

    @property
    def timespan(self):
        """
        Interval on which the temporal value is defined. It is zero for
        temporal values of instant duration.
        """
        return timedelta(0)

    @property
    def period(self):
        """
        Period on which the temporal value is defined ignoring the potential time gaps.
        """
        return Period(self.getTimestamp, self.getTimestamp, True, True)

    @property
    def numInstants(self):
        """
        Number of instants.
        """
        return 1

    @property
    def startInstant(self):
        """
        Start instant.
        """
        return self

    @property
    def endInstant(self):
        """
        End instant.
        """
        return self

    def instantN(self, n):
        """
        N-th instant.
        """
        if n == 1:
            return self
        else:
            raise Exception("ERROR: Out of range")

    @property
    def instants(self):
        """
        List of instants.
        """
        return [self]

    @property
    def numTimestamps(self):
        """
        Number of timestamps.
        """
        return 1

    @property
    def startTimestamp(self):
        """
        Start timestamp.
        """
        return self.getTimestamp

    @property
    def endTimestamp(self):
        """
        End timestamp.
        """
        return self.getTimestamp

    def timestampN(self, n):
        """
        N-th timestamp
        """
        if n == 1:
            return self.getTimestamp
        else:
            raise Exception("ERROR: Out of range")

    @property
    def timestamps(self):
        """
        List of timestamps.
        """
        return [self.getTimestamp]

    def shift(self, timedelta):
        """
        Shift the temporal value by a time interval.
        """
        self.getTimestamp += timedelta
        return self

    def intersectsTimestamp(self, timestamp):
        """
        Does the temporal value intersect the timestamp?
        """
        return self.getTimestamp == timestamp

    def intersectsTimestampSet(self, timestampset):
        """
        Does the temporal value intersect the timestamp set?
        """
        return any(self.getTimestamp == timestamp for timestamp in timestampset.timestamps)

    def intersectsPeriod(self, period):
        """
        Does the temporal value intersect the period?
        """
        return period.contains_timestamp(self.getTimestamp)

    def intersectsPeriodSet(self, periodset):
        """
        Does the temporal value intersect the period set?
        """
        return any(period.contains_timestamp(self.getTimestamp) for period in periodset.periods)

    # Comparisons are missing
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.getValue == other.getValue and self.getTimestamp == other.getTimestamp:
                return True
        return False

    def __str__(self):
        return (f"'{self.getValue!s}@{self.getTimestamp!s}'")

    def __repr__(self):
        return (f'{self.__class__.__name__ }'
                f'({self.getValue!r}, {self.getTimestamp!r})')

