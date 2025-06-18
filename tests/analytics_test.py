import unittest
import sys, os
from datetime import date, timedelta
sys.path.append(os.path.abspath("."))

import db.controller as dbc
import obj.request_handler as request
import db.populate_debug_data as debug_data
import obj.user as usr
import obj.habit as habit
import obj.subscription as sub


file = dbc.Connection.TEST


#* ********************************************* Completion State *********************************************
class TestSubCompleteState(unittest.TestCase):
    """
    This tests completion states, i.e. is a subscription currently completed.
    """
    @classmethod
    def setUpClass(cls) -> None:
        setup_test_db()

    @classmethod
    def tearDownClass(cls) -> None:
        dbc.db_drop_all(conn=file)
        os.remove(str(file.value)) if os.path.exists(str(file.value)) else None
        return super().tearDownClass()

    def test_sub_compl_state_daily_false(self) -> None:
        """Tests if the subscription should currently be in a completed state.
        Uses 'Sub 1' defined in  setUpClass() -> setup_test_db().
        ### Sub 1 -> Daily, completed: 10 days, last 5 days ago
        This test case is used on a subscription that is currently NOT completed, thus False."""
        s = test_helper_query_db_for_sub(1)
        if not s:
            self.assertTrue(False)
            return

        last_compl = request.get_latest_sub_completion_for_user(1, s.id, conn=file)
        if not last_compl:
            self.assertTrue(False)
            return

        self.assertFalse(s.get_completed_state(last_compl))

    def test_sub_compl_state_daily_true(self) -> None:
        """Tests if the subscription should currently be in a completed state.
        Uses 'Sub 2' defined in  setUpClass() -> setup_test_db().
        ### Sub 2 -> Daily, completed: 12 days, then 3 days break, then 2 days incl. today, streak: 2|12
        This test case is used on a subscription that is currently completed, thus True."""
        s = test_helper_query_db_for_sub(2)
        if not s:
            self.assertTrue(False)
            return

        last_compl = request.get_latest_sub_completion_for_user(1, s.id, conn=file)
        if not last_compl:
            self.assertTrue(False)
            return

        self.assertTrue(s.get_completed_state(last_compl))

    def test_sub_compl_state_weekly_false(self) -> None:
        """Tests if the subscription should currently be in a completed state.
        Uses 'Sub 3' defined in  setUpClass() -> setup_test_db().
        ### Sub 3 -> Weekly, completed: last_sunday, 1w break, then 8 times, streak: 1|8
        This test case is used on a subscription that is currently NOT completed, thus False."""
        s = test_helper_query_db_for_sub(3)
        if not s:
            self.assertTrue(False)
            return

        last_compl = request.get_latest_sub_completion_for_user(1, s.id, conn=file)
        if not last_compl:
            self.assertTrue(False)
            return

        self.assertFalse(s.get_completed_state(last_compl))

    def test_sub_compl_state_weekly_true(self) -> None:
        """Tests if the subscription should currently be in a completed state.
        Uses 'Sub 4' defined in  setUpClass() -> setup_test_db().
        ### Sub 4 -> Weekly, completed: today, last 3 sundays, streak: 4|4
        This test case is used on a subscription that is currently completed, thus True."""
        s = test_helper_query_db_for_sub(4)
        if not s:
            self.assertTrue(False)
            return

        last_compl = request.get_latest_sub_completion_for_user(1, s.id, conn=file)
        if not last_compl:
            self.assertTrue(False)
            return

        self.assertTrue(s.get_completed_state(last_compl))


#* ********************************************* User Analytics *********************************************
class TestUserAnalytics(unittest.TestCase):
    """
    This tests the user's statistics used for the statistic screen in the app.
    For now, this is achieved by simply copying the functionality and applying it to the test database.
    With this we can check if it produces the expected result.
    """

    @classmethod
    def setUpClass(cls) -> None:
        setup_test_db()

    @classmethod
    def tearDownClass(cls) -> None:
        dbc.db_drop_all(conn=file)
        os.remove(str(file.value)) if os.path.exists(str(file.value)) else None
        return super().tearDownClass()

    def test_user_default_analytics(self) -> None:
        """Mimics code used in the stats_screen.
        This functionality should arguably be in the user class.
        """
        best_cur = (0, "No streaks yet.")
        best_max = (0, "No streaks yet.")

        oldest = (date.today(), "No habits found.")

        easiest:tuple[float, str, int] = (0.00, "No habits found.", 0) # success rate, habit data name, expected completions
        hardest:tuple[float, str, int] = (100.00, "No habits found.", 0)

        total_compl_done:int = 0
        total_compl_exp:int = 0

        usr_subs = request.get_subs_for_user(user_id=1, conn=file)

        for s in usr_subs:
            # streaks
            if s.cur_streak > best_cur[0]:
                best_cur = (s.cur_streak, s.habit_data.name)
            if s.max_streak > best_max[0]:
                best_max = (s.max_streak, s.habit_data.name)

            # oldest
            if s.creation_date < oldest[0]:
                oldest = (s.creation_date, s.habit_data.name)

            # easiest / hardest - prioritize habits with higher number of expected completions
            rate:tuple[int, int, float] = s.get_completion_rate(b_test=True)
            if rate[2] > easiest[0] or (rate[2] == easiest[0] and rate[1] > easiest[2]):
                easiest = (rate[2], s.habit_data.name, rate[1])
            if rate[2] < hardest[0] or (rate[2] == hardest[0] and rate[1] > hardest[2]):
                hardest = (rate[2], s.habit_data.name, rate[1])
            total_compl_done += rate[0]
            total_compl_exp += rate[1]

        if total_compl_done + total_compl_exp == 0:
            avg_compl_rate:float = 0
        else:
            avg_compl_rate:float = round((total_compl_done / total_compl_exp) * 100, 2)

        # * TRUE if:
        # * best current streak is Sub 4 with 4 completions
        # * best maximum streak is Sub 2 with 12 completions
        # * oldest test habit created is Sub 3, roughly 10 weeks old
        # * average completion works out to be: 38/47 = 80.85%
        self.assertTrue(
            best_cur[0] == 4 and\
            best_max[0] == 12 and\
            oldest[1] == "testhabit3" and\
            avg_compl_rate == 80.85
        )


#* ********************************************* Sub Streaks *********************************************
class TestSubStreakCalculation(unittest.TestCase):
    """
    This tests correctness of a given subscriptions streak calculation and analytics.
    Important: the main calculation happens in check_streak_broken(); when a user logs in, this is called on all their subs.
    Otherwise there is no real 'calcuation' as we can simply query the given db entry which is updated accordingly.
    These updates happen if either a streak is broken or a new completion is added/revoked. These scenarios will be tested.
    """
    @classmethod
    def setUpClass(cls) -> None:
        setup_test_db()

    @classmethod
    def tearDownClass(cls) -> None:
        dbc.db_drop_all(conn=file)
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        return super().tearDownClass()

    def test_sub_analytics(self) -> None:
        """Tests correctness of a subscriptions analytics. Other than statistics that can just be querried,
        this, for now, only includes completion rate calculations.
        Using Sub 2:
        ### Sub 2 -> Daily, completed: 12 days, then 3 days break, then 2 days incl. today, streak: 2|12
        """
        s = test_helper_query_db_for_sub(2)
        if not s:
            self.assertTrue(False)
            return

        compl_rate:tuple[int, int, float] = s.get_completion_rate(b_test=True)

        # expected is determined by when the subscription was created (in this case 18 days ago)
        expected_rate:tuple[int, int, float] = (14, 18, 77.78)

        self.assertEqual(compl_rate, expected_rate)

    def test_sub_streak_daily_intact(self) -> None:
        """ Tests if the subscription's streak can be correctly identified as broken.
        Uses 'Sub 1' defined in  setUpClass() -> setup_test_db().
        ### Sub 1 -> Daily, completed: 10 days, last 5 days ago
        """
        s = test_helper_query_db_for_sub(2)
        if not s:
            self.assertTrue(False)
            return

        self.assertFalse(s.check_streak_broken(b_test=True)) # (false -> it's NOT broken)

    def test_sub_streak_daily_broken(self) -> None:
        """ Tests if the subscription's streak can be correctly identified as broken.
        Uses 'Sub 5' defined in  setUpClass() -> setup_test_db().
        ### Sub 5 -> Mondays, completed monday 2w ago, thus streak is thus broken
        """
        s = test_helper_query_db_for_sub(1)
        if not s:
            self.assertTrue(False)
            return

        self.assertTrue(s.check_streak_broken(b_test=True)) # (true -> it's broken)

    def test_sub_streak_weekly_intact(self) -> None:
        """ Tests if the subscription's streak can be correctly identified as broken.
        Uses 'Sub 3' defined in  setUpClass() -> setup_test_db().
        ### Sub 3 -> Weekly, completed: last_sunday, 1w break, then 8 times, streak: 1|8
        """
        s = test_helper_query_db_for_sub(3)
        if not s:
            self.assertTrue(False)
            return

        self.assertFalse(s.check_streak_broken(b_test=True)) # (false -> it's NOT broken)

    def test_sub_streak_weekly_broken(self) -> None:
        """ Tests if the subscription's streak can be correctly identified as broken.
        ### NEW Sub 6 -> Weekly, completed monday 2w ago, thus streak is thus broken
        """
        # New sub 6 for this case (re-using, habit_data 1 - this is currently not seen as a problem)
        entry_id = dbc.db_create_habit_sub(1, 1, get_previous_weekday(6, 2).isoformat(), get_previous_weekday(6, 2).isoformat(), sub.Periodicity.WEEKLY.value, 0, 1, conn=file)
        dbc.db_create_completion(get_previous_weekday(6, 2).isoformat(), 1, 6, conn=file)
        s = test_helper_query_db_for_sub(entry_id)

        if not s:
            self.assertTrue(False)
            return

        self.assertTrue(s.check_streak_broken(b_test=True)) # (true -> it's broken)

    def test_sub_streak_weekday_intact(self) -> None:
        """ Tests if the subscription's streak can be correctly identified as broken.
        ### NEW Sub 7 -> Mondays, completed: last_sunday. This means it can't be broken.
        Even if it is Sunday today, then the habit/sub may be imcomplete but the streak is not broken until this sunday is over.
        """
        # New sub 7 for this case (re-using, habit_data 1 - this is currently not seen as a problem)
        entry_id = dbc.db_create_habit_sub(1, 1, get_previous_weekday(6, 1).isoformat(), get_previous_weekday(6, 1).isoformat(), sub.Periodicity.SUNDAY.value, 1, 1, conn=file)
        dbc.db_create_completion(get_previous_weekday(6, 1).isoformat(), 1, 7, conn=file)
        s = test_helper_query_db_for_sub(entry_id)

        if not s:
            self.assertTrue(False)
            return

        self.assertFalse(s.check_streak_broken(b_test=True)) # (false -> it's NOT broken)

    def test_sub_streak_weekday_broken(self) -> None:
        """ Tests if the subscription's streak can be correctly identified as broken.
        ### Sub 5 -> Mondays, completed monday 2w ago, thus streak is thus broken
        """
        s = test_helper_query_db_for_sub(5)
        if not s:
            self.assertTrue(False)
            return

        self.assertTrue(s.check_streak_broken(b_test=True)) # (true -> it's broken)



#* ********************************************* Helper Functions *********************************************
def setup_test_db() -> None:
    """Setup functionality seperated as this can use these db entries for multiple tests.
    Prevents duplicate lines."""
    os.remove(str(file.value)) if os.path.exists(str(file.value)) else None
    # debug_data.populate_all(conn=file)
    dbc.db_init(file)

    # Setup pre-reqs (these are tested in db_test.py)
    dbc.db_create_user("Tester", "test_user", "tester@example.com", "password", conn=file)
    dbc.db_create_habit_data(1, "Tester", "testhabit1", "this is a test", False, False, conn=file)
    dbc.db_create_habit_data(1, "Tester", "testhabit2", "this is also a test", False, False, conn=file)
    dbc.db_create_habit_data(1, "Tester", "testhabit3", "this again, is a test", False, False, conn=file)
    dbc.db_create_habit_data(1, "Tester", "testhabit4", "still testing", False, False, conn=file)
    dbc.db_create_habit_data(1, "Tester", "testhabit5", "these are descriptions btw", False, False, conn=file)

    # Sub 1 -> Daily, completed: 10 days, last 5 days ago
    dbc.db_create_habit_sub(1, 1, (date.today() - timedelta(days=10+5)).isoformat(), (date.today() - timedelta(days=5)).isoformat(), sub.Periodicity.DAILY.value, 0, 10, conn=file)
    for i in range(10):
        dbc.db_create_completion((date.today() - timedelta(days=5+i)).isoformat(), user_id=1, habit_sub_id=1, conn=file)

    # Sub 2 -> Daily, completed: 12 days, then 3 days break, then 2 days incl. today, streak: 2|12
    dbc.db_create_habit_sub(1, 2, (date.today() - timedelta(days=12+3+2)).isoformat(), date.today().isoformat(), sub.Periodicity.DAILY.value, 2, 12, conn=file)
    for i in range(0, 12+3+2):
        if (i == 2 or i == 3 or i == 4): continue
        dbc.db_create_completion((date.today() - timedelta(days=i)).isoformat(), 1, 2, conn=file)

    # Sub 3 -> Weekly, completed: last_sunday, 1w break, then 8 times, streak: 1|8
    dbc.db_create_habit_sub(1, 3, get_previous_weekday(6, 10).isoformat(), date.today().isoformat(), sub.Periodicity.WEEKLY.value, 1, 8, conn=file)
    dbc.db_create_completion(get_previous_weekday(6, 1).isoformat(), user_id=1, habit_sub_id=3, conn=file)
    for i in range (8):
        dbc.db_create_completion(get_previous_weekday(6, 3+i).isoformat(), user_id=1, habit_sub_id=3, conn=file)

    # Sub 4 -> Weekly, completed: today, last 3 sundays, streak: 4|4
    dbc.db_create_habit_sub(1, 4, get_previous_weekday(6, 1).isoformat(), date.today().isoformat(), sub.Periodicity.WEEKLY.value, 4, 4, conn=file)
    dbc.db_create_completion(date.today().isoformat(), user_id=1, habit_sub_id=4, conn=file)
    dbc.db_create_completion(get_previous_weekday(6, 3).isoformat(), 1, 4, conn=file)
    dbc.db_create_completion(get_previous_weekday(6, 2).isoformat(), 1, 4, conn=file)
    dbc.db_create_completion(get_previous_weekday(6, 1).isoformat(), 1, 4, conn=file)

    # Sub 5 -> Mondays, completed monday 2w ago, thus streak is thus broken
    dbc.db_create_habit_sub(1, 5, get_previous_weekday(0, 2).isoformat(), get_previous_weekday(0, 2).isoformat(), sub.Periodicity.MONDAY.value, 0, 1, conn=file)
    dbc.db_create_completion(get_previous_weekday(0, 2).isoformat(), 1, 5, conn=file)


def test_helper_query_db_for_sub(sub_id:int, conn:dbc.Connection=dbc.Connection.TEST) -> sub.HabitSubscription|None:
    """Querries the db via the controller directly (uses function exlusively for testing purposes),
    then checks & formats result and returns it.

    Args:
        sub_id (int): id of the sub to query
        conn (dbc.Connection, optional): connection to use. Defaults to dbc.Connection.TEST.

    Returns:
        sub.HabitSubscription|None: habit sub object based on the query result
    """
    result = dbc.db_get_habit_sub_by_id(sub_id, conn=conn)

    if len(result) <= 0 or len(result[0]) <= 0:
        return None

    return sub.HabitSubscription(
        sub_id=result[0][0],
        user_id=result[0][1],
        data_id=result[0][2],
        periodicity=result[0][3],
        cur_streak=result[0][4],
        max_streak=result[0][5],
        creation_date=result[0][6],
        last_completed_date=result[0][7],
        habit_data=request.get_habit_data(data_id=result[0][2], conn=conn)
    )


def get_previous_weekday(target_weekday:int, weeks_ago:int=1) -> date:
    """Returns the date of the `weeks_ago`-th previous occurrence of the target weekday.
    Helper function.

    Args:
        target_weekday (int): Monday = 0, Sunday = 6.
        weeks_ago (int): 1 for last week, 2 for 2nd last, etc.

    Returns:
        date: The date of the desired past weekday.
    """
    today = date.today()
    today_weekday = today.weekday()
    days_since_target = (today_weekday - target_weekday) % 7 + 7 * (weeks_ago - 1)
    return today - timedelta(days=days_since_target)