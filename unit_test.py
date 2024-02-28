import unittest
import sqlite3
import tkinter as tk
from io import StringIO
from main import OTPApp
from tkinter import Tk
from unittest.mock import patch
from ibek import generate_otp, save_otp_to_db, get_recent_otp_from_db, send_otp_email, verify_otp
from test import EmailSenderApp 

class TestOTPFunctions(unittest.TestCase):

    def test_generate_otp(self):
        otp = generate_otp()
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

    @patch('builtins.print')
    def test_save_otp_to_db(self, mock_print):
        otp = '123456'
        save_otp_to_db(otp)
        conn = sqlite3.connect('otp.db')
        c = conn.cursor()
        c.execute("SELECT * FROM otps WHERE otp=?", (otp,))
        result = c.fetchone()
        conn.close()
        self.assertIsNotNone(result)
        # self.assertEqual(result[0], otp)
        # mock_print.assert_not_called()

    def test_get_recent_otp_from_db(self):
        recent_otp = get_recent_otp_from_db()
        # self.assertIsNone(recent_otp)  # Assuming the database is initially empty
    pass

    @patch('win32com.client.Dispatch')
    def test_send_otp_email(self, mock_outlook):
        email = 'test@example.com'
        otp = '123456'
        send_otp_email(email, otp)
        mock_outlook().CreateItem().Send.assert_called_once()

    def test_verify_otp(self):
        otp = '123456'
        save_otp_to_db(otp)
        self.assertTrue(verify_otp(otp))
        self.assertFalse(verify_otp('654321'))

class TestOTPApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = OTPApp(self.root)
        
    def test_open_ibek(self):
        with patch('subprocess.Popen') as mock_popen, \
             patch.object(self.root, 'withdraw') as mock_withdraw:
            self.app.open_ibek()
            mock_popen.assert_called_once_with(['python', 'ibek.py'])
            mock_withdraw.assert_called_once()


class TestEmailSenderApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()  # Corrected from self.root = Tk()
        self.app = EmailSenderApp(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        # Set up the GUI with test data
        self.app.recipient_entry.insert(0, 'recipient@example.com')
        self.app.subject_entry.insert(0, 'Test Subject')
        self.app.code_text.insert('1.0', 'Test Body')

        # Call the send_email method
        self.app.send_email()

        # Assert that the SMTP server was called with the correct arguments
        mock_smtp.assert_called_with("smtp.gmail.com", 587)
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once()

if __name__ == '__main__':
    unittest.main()
