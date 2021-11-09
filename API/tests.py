from django.test import TestCase, RequestFactory
from . import validators
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class ValidatorsTestCase(TestCase):
    def test_check_if_not_future_date(self):
        future_date = str(datetime.now().date() + relativedelta(days=1))
        present_date = date = str(datetime.now().date())
        past_date = str(datetime.now().date() + relativedelta(days=-2))

        future_date_status = validators.check_if_not_future_date(future_date)
        present_date_status = validators.check_if_not_future_date(present_date)
        past_date_status = validators.check_if_not_future_date(past_date)

        self.assertEqual(future_date_status, False)
        self.assertEqual(present_date_status, True)
        self.assertEqual(past_date_status, True)

    def test_check_if_not_present_date(self):
        future_date = str(datetime.now().date() + relativedelta(days=1))
        present_date = str(datetime.now().date())
        past_date = str(datetime.now().date() + relativedelta(days=-2))

        future_date_status = validators.check_if_not_present_date(future_date)
        present_date_status = validators.check_if_not_present_date(present_date)
        past_date_status = validators.check_if_not_present_date(past_date)

        self.assertEqual(future_date_status, True)
        self.assertEqual(present_date_status, False)
        self.assertEqual(past_date_status, True)

    def test_check_if_not_past_date(self):
        future_date = str(datetime.now().date() + relativedelta(days=1))
        present_date = str(datetime.now().date())
        past_date = str(datetime.now().date() + relativedelta(days=-2))

        future_date_status = validators.check_if_not_past_date(future_date)
        present_date_status = validators.check_if_not_past_date(present_date)
        past_date_status = validators.check_if_not_past_date(past_date)

        self.assertEqual(future_date_status, True)
        self.assertEqual(present_date_status, True)
        self.assertEqual(past_date_status, False)

    def test_check_if_valid_date(self):
        valid_date = "2021-01-03"
        invalid_date = "2021-01-033"

        valid_date_status = validators.check_if_valid_date(valid_date)
        invalid_date_status = validators.check_if_valid_date(invalid_date)

        self.assertEqual(valid_date_status, True)
        self.assertEqual(invalid_date_status, False)

    def test_check_if_not_null(self):
        null_value = None
        blank_value = ""
        data = "test"

        null_value_status = validators.check_if_not_null_value(null_value)
        blank_value_status = validators.check_if_not_null_value(blank_value)
        data_status = validators.check_if_not_null_value(data)

        self.assertEqual(null_value_status, False)
        self.assertEqual(blank_value_status, True)
        self.assertEqual(data_status, True)

    def test_check_if_not_blank(self):
        blank_value = ""
        data = "test"

        blank_value_status = validators.check_if_not_blank_value(blank_value)
        data_status = validators.check_if_not_blank_value(data)

        self.assertEqual(blank_value_status, False)
        self.assertEqual(data_status, True)

    def test_convert_date_formats(self):
        date_format_1 = "2020-01-01"
        date_format_2 = "20200101"
        date_format_3 = "2020.01.01"
        date_format_4 = "2020/01/01"
        date_format_5 = "01.01.2020"
        date_format_6 = ""
        date_format_7 = "01-01-2020"

        date = datetime.strptime("2020-01-01", "%Y-%m-%d").date()

        date_1 = validators.convert_date_formats(date_format_1)
        date_2 = validators.convert_date_formats(date_format_2)
        date_3 = validators.convert_date_formats(date_format_3)
        date_4 = validators.convert_date_formats(date_format_4)
        date_5 = validators.convert_date_formats(date_format_5)
        date_6 = validators.convert_date_formats(date_format_6)
        date_7 = validators.convert_date_formats(date_format_7)

        self.assertEqual(date_1, date)
        self.assertEqual(date_2, date)
        self.assertEqual(date_3, date)
        self.assertEqual(date_4, date)
        self.assertEqual(date_5, date)
        self.assertEqual(date_6, None)
        self.assertEqual(date_7, date)

    def test_calculate_threshold(self):
        self.assertEqual(validators.calculate_threshold(0,10), 100)
        self.assertEqual(validators.calculate_threshold(1,9), 90)

    def test_check_if_array_not_null(self):
        null_value = []
        data1 = ["test_data"]
        data2 = ["test_data", "test_data2"]

        null_value_status = validators.check_if_array_not_null_value(null_value)
        one_value_status = validators.check_if_array_not_null_value(data1)
        two_value_status = validators.check_if_array_not_null_value(data2)

        self.assertEqual(null_value_status, False)
        self.assertEqual(one_value_status, True)
        self.assertEqual(two_value_status, True)




