from unittest.mock import Mock, AsyncMock, patch, call
import pytest
import pandas as pd

# import functions to test
import Mensa_Bot.bot as bot


class TestStart:
    "Tests relating to the start command"

    @pytest.mark.asyncio
    async def test_start_message(self):

        "Test if right start message is sent"
        mocked_update = AsyncMock()
        mocked_update.effective_chat.id = 0
        mocked_context = AsyncMock()

        await bot.start_msg(mocked_update, mocked_context)
        mocked_context.bot.send_message.assert_called_with(chat_id=0, text="Hallo vom Mensabot! \nWas kann ich für dich tun?")


class TestSendMsg:
    "Tests related to send_msg"

    def test_message_multiple_entries(self):
        "Test if jobs for each client_id are returned"
        mock_db = Mock()
        mock_text = Mock()
        mock_client1 = Mock(chat_id=0)
        mock_client2 = Mock(chat_id=1)
        mock_db.select.return_value = [mock_client1, mock_client2]

        mock_context = Mock()

        test_gen = bot.send_msg(mock_context, mock_db, mock_text)
        test = [*test_gen]
        assert test[0] == mock_context.bot.send_message(client_id=0)
        assert test[1] == mock_context.bot.send_message(client_id=1)

    def test_right_text(self):
        "Test if right text is parsed"
        mock_db = Mock()
        mock_db.select.return_value = [Mock()]

        mock_context = Mock()

        test_gen = bot.send_msg(mock_context, mock_db, 'Test')
        test = [*test_gen]
        assert test[0] == mock_context.bot.send_message(text='Test')


class TestMenuMessage:
    "Tests related to menu Message"

    # Setup data used in testing from files
    df_main = pd.read_pickle('./tests/data/main.pk1')

    @pytest.mark.asyncio
    @patch('Mensa_Bot.bot.Menu')
    @patch('Mensa_Bot.bot.parse_menu')
    async def test_parse_menu_called(self, mock_parse, mock_db):
        "Test if parse_menu is called"
        mock_context = Mock()
        mock_db = Mock()
        mock_parse.return_value = (self.df_main, None)

        await bot.menu_message(mock_context)
        mock_parse.assert_called()

    @pytest.mark.asyncio
    @patch('Mensa_Bot.bot.gen_message')
    @patch('Mensa_Bot.bot.Menu')
    @patch('Mensa_Bot.bot.parse_menu')
    async def test_gen_message_called(self, mock_parse, mock_db, mock_message):
        "test if gem_message is called with right parameters"
        mock_context = Mock()
        mock_db = Mock()
        mock_parse.return_value = (self.df_main, None)

        mock_message.return_value = ""

        await bot.menu_message(mock_context)

        called_df = mock_message.call_args.args[0]
        pd.testing.assert_frame_equal(self.df_main, called_df)


    @pytest.mark.asyncio
    @patch('Mensa_Bot.bot.send_msg')
    @patch('Mensa_Bot.bot.gen_message')
    @patch('Mensa_Bot.bot.Menu')
    @patch('Mensa_Bot.bot.parse_menu')
    async def test_send_msg_called(self, mock_parse, mock_db, mock_message, send_msg):
        "test if send_message is called with right parameters"
        mock_context = Mock()
        mock_parse.return_value = (self.df_main, None)

        mock_message.return_value = "Test"

        await bot.menu_message(mock_context)
        send_msg.assert_called_with(mock_context, mock_db, "Test")

    @pytest.mark.asyncio
    @patch('Mensa_Bot.bot.send_msg')
    @patch('Mensa_Bot.bot.gen_message')
    @patch('Mensa_Bot.bot.Menu')
    @patch('Mensa_Bot.bot.parse_menu')
    async def test_create_tasks(self, mock_parse, mock_db, mock_message, send_msg):
        "test if send_message is called with right parameters"
        mock_context = Mock()
        mock_parse.return_value = (self.df_main, None)

        mock_message.return_value = "Test"

        await bot.menu_message(mock_context)
        mock_context.application.create_task.assert_called()

class TestVegiMessage:
    "Tests related to veggi Message"

    # Setup data used in testing from files
    df_main = pd.read_pickle('./tests/data/main.pk1')
    df_veggi = df_main.loc[
        df_main["Art"].str.contains("\N{carrot}")
        | df_main["Art"].str.contains("\N{broccoli}")
    ]

    @pytest.mark.asyncio
    @patch('Mensa_Bot.bot.Veggi')
    @patch('Mensa_Bot.bot.parse_menu')
    async def test_parse_menu_called(self, mock_parse, mock_db):
        "Test if parse_menu is called"
        mock_context = Mock()
        mock_db = Mock()
        mock_parse.return_value = (self.df_main, None)

        await bot.veggi_message(mock_context)
        mock_parse.assert_called()

    @pytest.mark.asyncio
    @patch('Mensa_Bot.bot.gen_message')
    @patch('Mensa_Bot.bot.Veggi')
    @patch('Mensa_Bot.bot.parse_menu')
    async def test_gen_message_called(self, mock_parse, mock_db, mock_message):
        "test if gen_message is called with right parameters"
        mock_context = Mock()
        mock_db = Mock()
        mock_parse.return_value = (self.df_main, None)

        mock_message.return_value = ""

        await bot.veggi_message(mock_context)

        called_df = mock_message.call_args.args[0]
        pd.testing.assert_frame_equal(self.df_veggi, called_df)

    @pytest.mark.asyncio
    @patch('Mensa_Bot.bot.send_msg')
    @patch('Mensa_Bot.bot.gen_message')
    @patch('Mensa_Bot.bot.Veggi')
    @patch('Mensa_Bot.bot.parse_menu')
    async def test_send_msg_called(self, mock_parse, mock_db, mock_message, send_msg):
        "test if send_message is called with right parameters"
        mock_context = Mock()
        mock_parse.return_value = (self.df_main, None)

        mock_message.return_value = "Test"

        await bot.veggi_message(mock_context)
        send_msg.assert_called_with(mock_context, mock_db, "Test")

    @pytest.mark.asyncio
    @patch('Mensa_Bot.bot.send_msg')
    @patch('Mensa_Bot.bot.gen_message')
    @patch('Mensa_Bot.bot.Veggi')
    @patch('Mensa_Bot.bot.parse_menu')
    async def test_create_tasks(self, mock_parse, mock_db, mock_message, send_msg):
        "test if send_message is called with right parameters"
        mock_context = Mock()
        mock_parse.return_value = (self.df_main, None)

        mock_message.return_value = "Test"

        await bot.veggi_message(mock_context)
        mock_context.application.create_task.assert_called()


