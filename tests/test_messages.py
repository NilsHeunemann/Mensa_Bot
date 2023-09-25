from unittest.mock import Mock, AsyncMock, patch
import pytest

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
