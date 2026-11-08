# WhatsApp Bot

This notebook sends a personalised WhatsApp message to each person in a contact list. It opens WhatsApp Web in Chrome, fills in each person's name, and can attach one image to every message.

I built this to practise browser automation with Python, Selenium, and pandas.

**IMPORTANT: There are 2 separate items in the notebook:**
- Cell 1-2: Standard Image & Send
- Cell 3: Message Spammer

## What you need

- Python 3
- Google Chrome
- A WhatsApp account you can log into with WhatsApp Web
- pandas and Selenium

```bash
pip install pandas selenium
```

## Whatsapp Bot: Standard Section

This section is dedicated to Cell 1-2 of the Notebook.

### How it Works

There are 2 types of messages this program can send:

Plain text: Occurs when image input is "NA"
Image + text: Occurs when image input is a path to an image on your computer. 

### Plain Text

The text is contained inside the .txt file. The program reads it, then converts [name] into each individual's name as written in the .csv file.

Here is an example output:

<img width="174" height="36" alt="Screenshot 2026-11-03 215905" src="https://github.com/user-attachments/assets/c56de1f8-3b87-4082-9537-4d42a7ecfcec" />

This is a plain text output.

Here is an example output with multiple people:

<img width="483" height="306" alt="Screenshot 2026-11-03 215644" src="https://github.com/user-attachments/assets/3b86d9f1-0bcf-4afe-8096-3a355b6462e8" />

*note that the names and profile pictures here are censored for privacy reasons.

### Image + Text

The text is also contained inside the .txt file, only with an image added this time. The program attaches the text to the image then sends it.

Here is an example output:

<img width="368" height="289" alt="Screenshot 2026-11-03 220318" src="https://github.com/user-attachments/assets/017fae58-398a-49ea-89c7-b309e9e922c4" />

This is an image + text output. 

Here is an example output with multiple people:

<img width="472" height="302" alt="Screenshot 2026-11-03 220309" src="https://github.com/user-attachments/assets/1d941248-a227-42fa-8ab2-1137d9d3a847" />

*The image icon is present here, so an image is present in the message. The profile pictures, names are also censored here for privacy reasons.

### Files to add

Put **one** `.csv` and **one** `.txt` in this folder, next to `WhatsappAutomaterFinal.ipynb`. The notebook stops if it finds any other number of those files.

The CSV needs these column names exactly:

```csv
Name,Phone Number
Ada,85291234567
```

Phone numbers should include the country code, with no `+`, spaces, or dashes. `85291234567` works. `+852 9123 4567` does not.

The text file is the message. Write `[name]` where the person's name should go:

```text
Hello [name], this is a reminder.
```

For Ada, that becomes `Hello Ada, this is a reminder.`

### How to run

1. Open `WhatsappAutomaterFinal.ipynb`.
2. Run the first code cell.
3. When it asks for an image, enter a full path such as `C:/Users/Bypasser/Pictures/poster.jpeg`, or enter `NA` to send text only.
4. Chrome opens WhatsApp Web. Scan the QR code and wait until your chats load.
5. Run the second code cell. Leave that Chrome window alone until the list finishes.

The first cell prints the CSV and text file it found. The second cell walks the list from top to bottom.

### Attaching an image

When the first cell asks for an image, paste the full path to one file:

```text
C:/Users/Bypasser/Pictures/poster.jpeg
```

Enter the path **without quotes**. Type `NA` when you want text only. Anything else is treated as a file path, including `na` or a path with a typo.

Then, **scan the whatsapp QR code in the automated chrome browser using your mobile phone in the whatsapp app** then run the second cell.
- if the QR code is not scanned, this code will NOT work.
- note that you only have to scan the QR code once every time you run the 1st cell.
  
That one file is pasted into the chat for every person. After the preview opens, the whole text file is pasted in as one caption, with `[name]` replaced for each row. The notebook then clicks Send once and waits 5 seconds before the next chat.

The file has to be on this computer, and it has to be a photo or a video that WhatsApp's photo picker accepts (`mp4`, `3gpp`, or QuickTime). WhatsApp Web needs to be in English, because the notebook looks for the buttons labelled Attach and Send.

### How it works

The notebook looks in this folder for the contact list and the message. If you start Jupyter from the parent `My_Projects` folder, it also checks a nested `Whatsapp Message Automater` folder.

For each row it opens a WhatsApp chat for that phone number and replaces `[name]` in the template.

- **Text only:** it types the whole file as one message, then presses Enter once.
- **With an image:** it pastes the photo, waits for the preview, pastes the whole text file as one caption, clicks Send once, and waits 5 seconds before the next person.

## Whatsapp Bot: Spammer

Note: Do not use this to harass someone. This is only here for demonstrative purposes.

### Inputs

Run cell 3 in the ipynb directly, then submit the inputs:
|Input|What to submit|
|----|-----|
|Phone| Phone number you wish to send this message to|
|Message| Input your message. |
|Raw Count| How many messages you wish to send. This must be an integer. (Max is 100 messages)|

## What’s in this folder

| File | Purpose |
| --- | --- |
| `WhatsappAutomaterFinal.ipynb` | Opens WhatsApp Web and sends the messages |
| Your `.csv` | Names and phone numbers |
| Your `.txt` | Message template |
| `README.md` | This file |

## Tips

- Log in during the first cell, then run the second cell in the same Chrome window. Running the first cell again opens a new window.
- Keep the column headers as `Name` and `Phone Number`. Other names are ignored.
- Save the message as UTF-8 so names and punctuation stay intact.
- A missing image path, or a number WhatsApp cannot open, stops the loop on that person.
- Sending a long list quickly can get the account rate-limited. Use this for people who expect the message.
