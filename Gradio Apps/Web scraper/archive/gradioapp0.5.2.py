#Importiing neccessary packages
try:
    import gradio as gr
    import pandas as pd
    import time
    from selenium import webdriver
    import json
    from bs4 import BeautifulSoup as bs
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By # used for waiting page to load
    from selenium.webdriver.support.ui import WebDriverWait # used for waiting page to load
    from selenium.webdriver.support import expected_conditions as EC # used for waiting page to load
    import requests
    import markdown
    import docx
    from docx.shared import Pt, RGBColor
    print("All packages imported successfully")
except:
    print("Error importing packages")
    exit(1)

TEST_APIKEY = ""

def webScrape(url, time_rate):
    chrome_options = Options()
    # Optional: Run headless so a browser window doesn't physically pop up
    # chrome_options.add_argument("--headless") 
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(time_rate * 0.5) # Allow page to load initial elements
        
        # --- NEW COOKIE BYPASS LOGIC ---
        # Khan Academy and common cookie managers use buttons containing these texts
        cookie_keywords = ["Accept", "Agree", "Allow all", "Dismiss", "Accept Cookies"]
        for keyword in cookie_keywords:
            try:
                # Try finding a button matching the text and click it
                cookie_button = driver.find_element(By.XPATH, f"//button[contains(text(), '{keyword}')] | //button[contains(., '{keyword}')]")
                cookie_button.click()
                print(f"Automatically clicked cookie button: '{keyword}'")
                time.sleep(2) # Give it a second to close the pop-up
                break
            except:
                continue # If it doesn't find this specific keyword, keep checking others
        # -------------------------------

        # Scroll to bottom to trigger lazy-loading content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(time_rate * 0.1) 
        
        html = driver.page_source  # Fixed: Removed ()
        
        soup = bs(html, "html.parser")
        body_content = soup.body
        if not body_content:
            return "Could not find body tag."

        # Remove script and style elements
        for script_or_style in body_content(["script", "style"]):
            script_or_style.extract()

        # Get text with proper spacing
        cleaned_content = body_content.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        cleaned_content = cleaned_content.replace("\xa0", " ")
        return cleaned_content
    finally:
        driver.quit()  # Fixed: Ensures the browser always closes!
def aiPrompt(prompt, API_Key, system_prompt, time_rate):
    
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
            "Authorization": f"Bearer {API_Key}",
            "Content-Type": "application/json"
    }       

    data = {
            "model": "z-ai/glm-4.5-air:free",  # free model
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
        ] }
    time.sleep(time_rate*0.8)
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() 
        
        # SUCCESS PATH: Pull the data and return it immediately
        output = response.json()["choices"][0]["message"]["content"]
        time.sleep(time_rate * 0.4)
        return output
        
    except Exception as e:
        # ERROR PATH: Log detailed server errors and cleanly halt execution
        print(f"\n--- API CALL FAILED ---")
        print(f"Error details: {e}")
        if 'response' in locals() and response.status_code != 200:
            print(f"Server response text: {response.text}")
        print(f"-----------------------\n")
        raise e

def aiOrganiser(p, goal, detail_level, hdmi_code):
    api_key2 = p
    if api_key2 == "TESTESTEST":
        api_key2 = TEST_APIKEY
    intro_prompt = f"Generate a system prompt based on this goal: {goal}, make sure the final response is {detail_level}. Write your system prompt based on this content:{hdmi_code}"
    return intro_prompt, api_key2


def bigMan(url, goal, api_key, detailLevel, time_delay, output_format, title):
    if output_format == "Microsoft Word (.docx)":
        yield f"Starting program with docx generation, estimated time is {time_delay*8 + 20} seconds", None, None
    else:
        yield f"Starting program with output as {output_format}, estimated time is {time_delay*8} seconds", None, None


    time.sleep(time_delay*0.02)
    cleaned_content = webScrape(url, time_delay)
    time.sleep(time_delay*0.5)
    try:
        intro_prompt, api_key2 = aiOrganiser(api_key, goal, detailLevel, cleaned_content)
    except:
            yield "AI Organisation failed", None, None
            return
    time.sleep(time_delay*0.5)
    yield "AI Organisation complete", None, None
    time.sleep(time_delay*0.02)
    yield "Getting System Prompt....", None, None
    system_prompts = "You are a helpful assistant."
    if output_format != "Microsoft Word (.docx)":
        output = aiPrompt(prompt = f"{intro_prompt} based on the html code {cleaned_content}, in {output_format} format style", API_Key = api_key2, system_prompt = system_prompts, time_rate=time_delay)
    else: 
        output = aiPrompt(prompt = f"{intro_prompt} based on the html code {cleaned_content} as a stylised text", API_Key = api_key2, system_prompt = system_prompts, time_rate=time_delay)
    time.sleep(time_delay*0.5)
    system_prompts = output
    print(system_prompts)
    yield "Extracting details...", None, None
    output2 = aiPrompt(prompt = f"{goal}, make sure the final response is in Python String format, the html code is {cleaned_content}", API_Key = api_key2, system_prompt = system_prompts, time_rate=time_delay)
    time.sleep(time_delay*0.25)
    yield "Refining details...", None, None
    if output_format == "Microsoft Word (.docx)":
        #set up document
        doc = docx.Document()
        headTitle = doc.add_paragraph()
        title_run = headTitle.add_run(title)
        title_run.font.size = Pt(30)                  # Make it big
        title_run.font.bold = True
        mainParagraph= doc.add_paragraph()
        paragraphs = mainParagraph.add_run(output2)
        paragraphs.font.size = Pt(12)
        output_doc = doc.save(f"{title}.docx") 
        yield gr.Textbox(visible = True, value="Your document has been generated successfully!"), gr.Markdown(visible = False), gr.File(visible = True, value=f"{title}.docx")
        return
    elif output_format == "Markdown":
        final_output = markdown.markdown(output2)
        yield gr.Textbox(visible = False, value=""), gr.Markdown(visible = True, value=final_output), gr.File(visible = False)
        return
    else:
        final_output = output2
        yield gr.Textbox(visible = True, value=final_output), gr.Markdown(visible = False), gr.File(visible = False)
        return

def gradio_filenametoggle(status):
    if status != "Microsoft Word (.docx)":
        return gr.update(visible=False)
    else:
        return gr.update(visible=True)

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale = 1, min_width = 300):
            url = gr.Textbox(label = "url to your website")
            goal = gr.Textbox(label = "What do you need from this Website?")
            API_Key = gr.Textbox(label = "Your API Key from openrouter.ai (if you have none, input TESTESTEST)")
            detailLevel = gr.Dropdown(label = "how detailed do you want the output to be?", choices = ["Very Simple","Simple", "Moderately Detailed", "Detailed", "Very Detailed"])
            Lag = gr.Slider(2,50,step = 0.1, label = """Lag on your device (Set this slider higher if you have bad internet connection, get errors at lower values, etc. 
                                                        Recommended value is 15-20 to prevent any errors""")
        with gr.Column(scale=2, min_width = 300):
                text_output = gr.Textbox(label = "Status / Text Output", visible=True)
                file_output = gr.File(label = "Download your file (.docx)", visible=False)
                markdown_output = gr.Markdown(label = "Markdown Output", visible=False)
    with gr.Row():
        with gr.Column(scale = 1, min_width = 300):
            output_format = gr.Radio(label = "Output format", choices = ["Markdown", "Plain text", "Microsoft Word (.docx)"])
            title = gr.Textbox(label="Title for your Word Document (Only used if Word is chosen)", value="My Report", visible = False)
    
   
    output_format.change(
        fn=None, 
        inputs=output_format, 
        outputs=title,
        js="""
        (status) => {
            return status === 'Microsoft Word (.docx)' 
                ? {visible: true, __type__: 'update'} 
                : {visible: false, __type__: 'update'};
        }
        """
    )
    with gr.Row():
        with gr.Column(scale = 1, min_width = 300):
            startbutton = gr.Button("Start")

    startbutton.click(fn = bigMan, inputs=[url, goal, API_Key, detailLevel, Lag, output_format, title], outputs=[text_output, markdown_output, file_output], api_name = "webscraper")
demo.launch()