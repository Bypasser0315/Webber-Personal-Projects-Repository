# Prerequisites

What has to be in place before `WhatsappAutomaterFinal.ipynb` can send messages. The full walkthrough is in `README.md`.

## Software

- Python 3
- Google Chrome
- pandas and Selenium

```bash
pip install pandas selenium
```

## Account

- A WhatsApp account you can log into with WhatsApp Web
- WhatsApp Web in English, because the notebook looks for the buttons labelled Attach and Send
- After the first cell opens Chrome, scan the WhatsApp QR code in that window with the WhatsApp app on your phone, then run the second cell. If the QR code is not scanned, the notebook will not work. You scan once each time you run the first cell.

## Files

Put **one** `.csv` and **one** `.txt` in this folder, next to the notebook. The notebook stops if it finds any other number of those files.

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

Save the message as UTF-8.

## Image (optional)

Text only: when the first cell asks for an image, enter `NA`.

Image plus text: enter the full path to one photo or video on this computer, without quotes. WhatsApp's photo picker accepts `mp4`, `3gpp`, and QuickTime as well as photos. That one file is attached for every person.
