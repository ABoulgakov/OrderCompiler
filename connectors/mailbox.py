import imaplib
import email
from email.header import decode_header
import json
from bs4 import BeautifulSoup


def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

def decode_mime_words(s):
    decoded = decode_header(s)
    return ''.join([
        (t[0].decode(t[1]) if isinstance(t[0], bytes) else t[0])
        for t in decoded
    ])

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
                except:
                    pass
            elif content_type == "text/html" and "attachment" not in content_disposition:
                try:
                    html = part.get_payload(decode=True).decode(errors="ignore")
                    body = BeautifulSoup(html, "html.parser").get_text()
                    break
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode(errors="ignore")
        except:
            pass
    return body.strip()

def fetch_emails(server, email_adress, password):
    imap = imaplib.IMAP4_SSL(server)
    imap.login(email_adress, password)
    imap.select("INBOX")

    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()

    emails_json = []
    print(f"Nombre d'emails trouvés: {len(email_ids)}")

    for i in email_ids:
        res, msg_data = imap.fetch(i, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject = decode_mime_words(msg.get("Subject", ""))
        from_ = decode_mime_words(msg.get("From", ""))
        to_ = decode_mime_words(msg.get("To", ""))
        date = msg.get("Date", "")
        body = get_email_body(msg)

        emails_json.append({
            "subject": subject,
            "from": from_,
            #"to": to_,
            "time": date,
            "body": body
        })

    imap.logout()

    #with open("data/inbox_emails.json", "w", encoding="utf-8") as f:
    #    json.dump(emails_json, f, indent=2, ensure_ascii=False)

    print("✅ Emails récupérés avec succès")

    return emails_json

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()
    imap_server = os.getenv("IMAP_SERVER")
    email_adress = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASS")
    fetch_emails(imap_server, email_adress, email_password)