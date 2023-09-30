from unittest.mock import Mock, AsyncMock, patch
import asyncio
import pytest
import pandas as pd

# import functions to test
import Mensa_Bot.bot as bot

class TestMenuParser():
    "Tests relating to the parse_menu function"

    # Setup data used in testing from files
    df_main = pd.read_pickle('./tests/data/main.pk1')
    df_side = pd.read_pickle('./tests/data/side.pk1')
    with open('./tests/data/web.txt', 'r') as f:
        webtext = f.read()

    @patch('Mensa_Bot.bot.requests.get')
    def test_parse_main_dishes_correctly(self, mock_get):
        "Test if main dishes are parsed correctly"

        mock_get.return_value = Mock(text=self.webtext)

        main_test, _ = bot.parse_menu()

        assert main_test.equals(self.df_main)
        
    @patch('Mensa_Bot.bot.requests.get')
    def test_parse_side_dishes_correctly(self, mock_get):
        "Test if side dishes are parsed correctly"

        mock_get.return_value = Mock(text=self.webtext)

        _, side_test = bot.parse_menu()

        assert side_test.equals(self.df_side)
 
class TestMessageGen():
    "class that tests the gen_message function"

    # get data to compare with 
    main_dishes = pd.read_pickle('./tests/data/main.pk1')
    with open('./tests/data/msg.txt', 'r') as f:
        message = f.read()

    def test_generated_message_ok(self):
        "Test if generated message is correct"

        test_message = bot.gen_message(self.main_dishes)

        assert test_message == self.message 



class TestFries():
    "class that tests the check_fries function"

    # get data to compare with
    side_dishes = pd.read_pickle('./tests/data/side.pk1')

    def test_some_fries(self):
        "Test if fries are correctly identified"
        side_dishes = self.side_dishes.copy()
        side_dishes['Gerichte'].iloc[2] = 'Pommes frites'

        test_result = bot.check_fries(self.side_dishes)

        assert test_result == False 
 
    def test_no_fries(self):
        "Test if no fries are correctly identified"

        test_result = bot.check_fries(self.side_dishes)

        assert test_result == False 
 
