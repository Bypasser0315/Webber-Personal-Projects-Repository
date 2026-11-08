<div align="center">

[**Overview**](README.md) &nbsp;&nbsp;|&nbsp;&nbsp; [Install](INSTALL.md)

  ![alt text](readme-images/image-3.png)
  
  <span style="font-size: 24px; font-weight: bold"> A personal projects repository <span>
  
  ![Selenium](readme-images/Selenium.svg) ![Gradio](readme-images/Gradio.svg) ![alt text](readme-images/image-4.png) ![alt text](readme-images/image-7.png) ![alt text](readme-images/image-16.png) <img width="63" height="20" alt="image" src="https://github.com/user-attachments/assets/e30ceb6b-f323-41ff-81ff-f9b88b150ca9" /> <img width="90" height="20" alt="image" src="https://github.com/user-attachments/assets/4516bb95-72e1-44a0-b8d8-0c7bdc264be4" />
  
  <span style="font-size: 16px;"> Made with Gemini and Cursor <span>
</div>

## Introduction
This is my personal collection of projects. The packages for all of them are in [requirements.txt](requirements.txt). Install steps are [here](INSTALL.md).

**The projects focus mainly on these attributes:**
- Web Scraping
- Automation
- Sorting
- AI

### List of Content

| Project | Function |
| ------- | ------- |
| ![Gradio App](readme-images/image-9.png) | ![Gradio](readme-images/Gradio.svg) app that processes a website from an url, then uses an AI (free model) to extract information based on user request.|
| ![Cookie Cooker](readme-images/image-10.png) | ![Selenium](readme-images/Selenium.svg) app that automatically plays cookie clicker. |
| ![Whatsapp Bot](readme-images/image-11.png) | ![Selenium](readme-images/Selenium.svg) app that automates whatsapp messages by sending a message + image(optional) to a large group of recipients listed in a CSV file. |
| ![HKTV Mall](readme-images/image-12.png) | Web scraping Demonstration. Uses ![Selenium](readme-images/Selenium.svg) to navigate through HKTV Mall website's dynamnic HTML, then analyses it using ![pandas](readme-images/image-7.png) and visualised using <img width="63" height="20" alt="image" src="https://github.com/user-attachments/assets/422f359e-d59c-45f6-b93c-b07d735ce886" />. | 
| ![Sorting Algorithms](readme-images/image-13.png) | A small collection of programs that perform sorts of numbered item lists in different methods. |
| ![D1 Papers](readme-images/image-14.png) | A Demonstration that uses ![pypdf](readme-images/image-17.png) to scrape the pdf, then sort D1 Question and Answer Papers together by topic by locating specific keywords. |

## Gradio App

The gradio app is the most ambitious project in this repository. I made this app to provide a clearer interface so that users can get better outputs from AI without having to purchase a subscription.

It is a multi-purpose, web-based application that works natively on the user's computer. 

Here's an example output:

[News summary.pdf](https://github.com/user-attachments/files/34429324/News.summary.pdf)

<img width="904" height="971" alt="image" src="https://github.com/user-attachments/assets/ca7dbf50-9039-4f4e-bd63-ae8ab215e892" />


The app works in a linear direction:

```mermaid
timeline 
  title How the Gradio App works
  section Input
    Reading Input: The program reads the user input and obtains necessary variables.
  section Reading
    Scraping: The program grabs the website html and uses BeautifulSoup4 to clean it. 
    Countermeasures: There are specific measures to combat cookies, advertisements, pop ups and dynamic HTML.
  section Prompting & Output
    AI Prompting: The program submits the cleaned HTML and user prompt to an AI on openrouter/free. 
    Output: AI Output is read and an output is provided based on the user input. Outputs could be plain text, Markdown or PDFs. 
```

For this app to work, you must have an [OpenRouter](https://openrouter.ai) key. You can use one with 0 tokens as this uses a free model. 

### Navigation

Thanks to Gradio, a simple input/output interface was achieved. There are 2 main sections of input:
- Prompt
- Output format

The prompt box features several adjustable elements and the input HTML, and the output box decides the format of the output:

<img width="624" height="766" alt="ScreenRecording2026-11-08191202-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/5eda8ec5-649e-4091-8fcd-a3eb92921fbb" />

This layout aims to minimize confusion and allow for a flexible range of both inputs and outputs.

Try it out on your computer!

## Cookie Cooker

Cookie Cooker is a fun project that plays [Cookie Clicker](https://cookie-clicker2.com/) in Chrome. It clicks the big cookie and buys Cursor, Grandma, Farm, and Mine when they are affordable.

Here's a short demo:

<img width="800" height="449" alt="ScreenRecording2026-11-03182613-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/4bb68cf7-d5b0-448c-b750-b6627ce6ae1f" />

Try it out on your computer!

## Whatsapp Bot

Whatsapp Bot automates large-scale whatsapp messages for companies and advertisements. It works by scraping the HTML using BeautifulSoup4, then traces whatsapp html using Selenium to locate elements to input images and text, and to send the message.

There are 2 versions of the app:
- Standard (text + image option, to many recipients)
- Spammer (just text, to one single recipient)

The standard is designed for companies to do advertisements to a large group of people, while the spammer is just for demonstrative purposes only.
  
Here is a quick demo of how it sends messages (Cell 3):

<img width="660" height="494" alt="ScreenRecording2026-11-08142911-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/382afa71-7cc6-4f4f-a7fd-2636c621c240" />

In the standard version, the app can jump from recipient to recipient:

<img width="800" height="903" alt="ScreenRecording2026-11-08181201-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/8b4cc56d-f51e-47db-a3fe-d3524bb13d89" />

Note that the names can also change from recipient to recipient. Do not use spammer to harass someone.

## HKTV Mall scraper

`HKTV Mall Web Scraping Demonstration` scrapes beef steak search results from HKTV Mall, and combats dynamic HTML by scrolling to the bottom then scraping.

Then, the statistics are scraped and the characteristics, such as origin of Product, sale quantity, overall rating of the product are found using Selenium locators, then grouped using pandas.

Characteristics of the data set, such as most common origin of product, products with the highest sales, etc, are analysed.

This is one of the Dataframes extracted by pandas:

<img width="784" height="404" alt="image" src="https://github.com/user-attachments/assets/d4eec72e-1b42-4a34-9ca7-e14346f20fb1" />

Using the Dataframe from pandas, the data can be easily visualised using Matplotlib.

Here is a pie chart showing origin of the products, plotted using Matplotlib:

<img width="591" height="449" alt="image" src="https://github.com/user-attachments/assets/478ebb01-db86-44dd-81e3-5c91a465e74b" />

By using a criteria model, a top 10 recommendation list can be obtained (this as of 8/11/2026):

<img width="1032" height="369" alt="Screenshot 2026-11-08 125942" src="https://github.com/user-attachments/assets/68b90ac0-78f6-4d20-bc9a-954523586c7f" />

Note that the current figure may differ from the one pre-loaded in the notebook. 

## Sorting algorithms

`Sorting Algorithms` was made as a learning project. It has three programs that read numbers until you type `end`, then sort them:

| Program | Method |
| --- | --- |
| `bubble_sort.py` | Compare neighbours and move the smaller one forward |
| `bogo_sort.py` | Shuffle until the list happens to be sorted |
| `random_quick_sort.py` | Pick a random pivot and sort the two sides |

## IAL D1 papers

`IAL D1 Papers` sorts Edexcel International A Level Decision Mathematics 1 past papers by topic. The source papers are in `Past Papers`. `D1management.ipynb` files each question into one pack and rebuilds the PDFs in `D1_Sorted_Final`:

- Algorithms
- Critical Path Analysis
- Graph I
- Graph II
- Linear Programming

The sorted by-topic PDFs are available to view in `D1_Sorted_Final`.
