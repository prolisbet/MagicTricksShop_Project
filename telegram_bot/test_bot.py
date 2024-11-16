import unittest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message
from main_tb import start, verify_user


class BotTest(unittest.TestCase):
    @patch('main_tb.bot')
    def test_start_command(self, mock_bot):
        mock_message = AsyncMock(Message)
        mock_message.text = "/start"
        response = start(mock_message)
        self.assertIsInstance(response, AsyncMock)

    @patch('main_tb.get_user_by_username', return_value=(1, "testuser"))
    @patch('main_tb.bot')
    def test_verify_user_success(self, mock_bot, mock_get_user):
        mock_message = AsyncMock(Message)
        mock_message.text = "testuser"
        response = verify_user(mock_message, {})
        self.assertIsInstance(response, AsyncMock)
