from configuration.secret import TEST_RECIPIENT, TEST_SENDER

if __name__ == '__main__':
    TEST_SENDER.send_recipient_email(TEST_RECIPIENT)
