import email

raw = b"Subject: test\n\nThis is the body"
msg = email.message_from_bytes(raw)
print("Subject:", msg["Subject"])