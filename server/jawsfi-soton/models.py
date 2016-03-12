from google.appengine.ext import ndb
import datetime


class Pi(ndb.Model):
    """A model for storing Rasberry Pi devices"""
    pi_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    activated = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)


class Result(ndb.Model):
    mac_address = ndb.StringProperty(required=True)
    signal = ndb.IntegerProperty(required=True)
    result_set = ndb.KeyProperty(required=True)


class ResultSet(ndb.Model):
    # Standard time needs to be in UTC and represents the time of the results
    # e.g. 06/03/2016 12:00...12:10...12:20...12:30 irrespective of what time it was
    # actually received and processed
    standard_time = ndb.DateTimeProperty()
    added = ndb.DateTimeProperty(auto_now_add=True)


def get_num_unique_sets():
    qry = ResultSet.query()
    return qry.count()


def get_unique_results():
    qry = Result.query()
    return qry.count()


def get_last_submission():
    qry = ResultSet.query().order(-ResultSet.added)
    results = qry.fetch(limit=1)
    if results:
        return results[0].added
    else:
        return None


def device_registered(token):
    qry = Pi.query(Pi.pi_id == token)
    results = qry.fetch(limit=1)
    if results:
        return results[0].activated
    else:
        return None


def register_pi(token, name):
    qry = Pi.query(Pi.pi_id == token)
    results = qry.fetch(limit=1)
    results[0].name = name
    results[0].activated = True
    results[0].put()


def process_results(results, time):
    def add_result(mac_address, signal, result_set_key):
        db_result = Result(mac_address=key, signal=value, result_set=result_set_key)
        db_result.put()

    def is_new_reading_stronger(signal_new, signal_old):
        return True if signal_new > signal_old else False

    def get_result(mac):
        qry = Result.query(Result.mac_address == mac)
        results = qry.fetch(limit=1)  # Only working with 1 at the moment

        return results[0]

    def get_other_sets(time, key):
        # Query ndb to see if there are any other Results Sets for this time.
        qry = ResultSet.query(ResultSet.standard_time == time, ResultSet.key != key)
        results = qry.fetch(limit=10)  # Only working with 10 at the moment

        return results

    def roundTime(dt=None, roundTo=60):
        """Round a datetime object to any time laps in seconds
		dt : datetime.datetime object, default now.
		roundTo : Closest number of seconds to round to, default 1 minute.
		Author: Thierry Husson 2012 - Use it as you want but don't blame me.
		"""
        if dt == None: dt = datetime.datetime.now()
        seconds = (dt - dt.min).seconds
        # // is a floor division, not a comment on following line:
        rounding = (seconds + roundTo / 2) // roundTo * roundTo
        return dt + datetime.timedelta(0, rounding - seconds, -dt.microsecond)

    # Round the time to the nearest 5 minute interval
    time = roundTime(time, roundTo=5 * 60)

    # Create a new ResultSet including the rounded time
    result_set = ResultSet()
    result_set.standard_time = time
    result_set_key = result_set.put()

    other_sets = get_other_sets(time, result_set_key)

    for key, value in results.iteritems():
        # If there are other sets, see if reading exists in it
        if other_sets:
            result = get_result(key)
            # If the result being processed is in the other set, compare signal strength
            if result:
                # If new value is stronger, remove old value and add new one to ndb
                if is_new_reading_stronger(value, result.signal):
                    result.key.delete()
                    add_result(key, value, result_set_key)
                else:
                    print('New reading is weaker, not putting in store')

            # There are others sets, but no matching mac address
            else:
                add_result(key, value, result_set_key)

        # No other relevant sets in ndb, proceed to add new value
        else:
            add_result(key, value, result_set_key)
