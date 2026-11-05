#Importiing neccessary packages
try:
    import gradio as gr
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
#Web Scraping Function
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
        driver.quit()  #Ensures the browser always closes
#AI Prompt Function
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

#AI Organiser Function
def aiOrganiser(p, goal, detail_level, hdmi_code):
    api_key2 = p
    if api_key2 == "TESTESTEST":
        api_key2 = TEST_APIKEY
    intro_prompt = f"Generate a system prompt based on this goal: {goal}, make sure the final response is {detail_level}. Write your system prompt based on this content:{hdmi_code}"
    return intro_prompt, api_key2

#Gradio Function
def bigMan(url, goal, api_key, detailLevel, time_delay, output_format, title, table, specs):
    if output_format == "Microsoft Word (.docx)":
        yield f"Starting program with docx generation, estimated time is {time_delay*8 + 5} seconds", None, None
    else:
        yield f"Starting program with output as {output_format}, estimated time is {time_delay*8} seconds", None, None


    time.sleep(time_delay*0.1)
    yield "Scraping Website html...", None, None
    cleaned_content = webScrape(url, time_delay)
    time.sleep(time_delay*0.5)
    try:
        intro_prompt, api_key2 = aiOrganiser(api_key, goal, detailLevel, cleaned_content)
        yield "AI Organisation complete", None, None
    except:
            yield "AI Organisation failed", None, None
            return
    
    time.sleep(time_delay*0.02)

    #The system prompt
    yield "Getting System Prompt....", None, None
    system_prompts = (
        f"""You are a precise web-scraping content extraction assistant. 
        Your job is to extract content based on the user's goal: {goal}, 
        ignoring all website navigation, advertisements, and popups."""
    )
    
    yield "Finalising the input...", None, None
    
    # 2. Inject the goal and detail level directly into the main user prompt
    detail_instruction = f"The final response must be {detailLevel}."
    
    if output_format == "Markdown" and table == True and specs != "":
        bigPrompt = f"User Goal: {goal}. {detail_instruction} Based on this scraped text:{cleaned_content}Format style: Markdown with a table.\nAdditional Customizations: {specs}"
    elif output_format == "Markdown" and table == True and specs == "":
        bigPrompt = f"User Goal: {goal}. {detail_instruction} Based on this scraped text:{cleaned_content}Format style: Markdown with a table."
    elif output_format == "Microsoft Word (.docx)":
        bigPrompt = f"User Goal: {goal}. {detail_instruction} Based on this scraped text:{cleaned_content}. Format style: Stylised text suitable for a Word document document."
    elif output_format == "Markdown" and table == False and specs != "":
        bigPrompt = f"User Goal: {goal}. {detail_instruction} Based on this scraped text:{cleaned_content}Format style: Markdown.\nAdditional Customizations: {specs}"
    else:
        bigPrompt = f"User Goal: {goal}. {detail_instruction} Based on this scraped text:{cleaned_content}Format style: {output_format}."
    
    # The Core prompt call remains the same
    time.sleep(time_delay*0.5) 
    output2 = aiPrompt(prompt = bigPrompt, API_Key = api_key2, system_prompt = system_prompts, time_rate=time_delay)
    print(bigPrompt)
    yield "Refining details...", None, None
    if output_format == "Microsoft Word (.docx)":
        #set up document
        doc = docx.Document()
        time.sleep(time_delay*0.1)

        #Title
        headTitle = doc.add_paragraph()
        title_run = headTitle.add_run(title)
        title_run.font.size = Pt(30)                  # Make it big
        title_run.font.bold = True                    # Make it bold

        #Body Paragraph 
        mainParagraph= doc.add_paragraph()
        paragraphs = mainParagraph.add_run(output2)
        paragraphs.font.size = Pt(12)
        output_doc = doc.save(f"{title}.docx") 
        yield gr.Textbox(visible = True, value="Your document has been generated successfully!"), gr.Markdown(visible = False), gr.File(visible = True, value=f"{title}.docx") #return the file
        return
    elif output_format == "Markdown":
        #Markdown output
        final_output = markdown.markdown(output2)
        print(final_output)
        yield gr.Textbox(visible = False, value=""), gr.Markdown(visible = True, value=final_output), gr.File(visible = False)
        return 
    else:
        # Plain text output
        final_output = output2
        yield gr.Textbox(visible = True, value=final_output), gr.Markdown(visible = False), gr.File(visible = False)
        return

#Gradio Function for toggling visibility between Radios
def gradio_filenametoggle(status):
    if status == "Microsoft Word (.docx)":
        return gr.Textbox(visible=True), gr.Checkbox(value = False, visible=False), gr.Textbox(value="", visible=False)
    elif status == "Markdown":
        return gr.Textbox(visible=False), gr.Checkbox(value = False, visible=True), gr.Textbox(value="", visible=True)
    else:
        return gr.Textbox(visible=False), gr.Checkbox(value = False, visible=False), gr.Textbox(value="", visible=False)

def toggle_boolean(current_state):
    # Do any custom backend processing or logging here if you need to:
    print(f"Checkbox state is now: {current_state}")
    
    # Return the state as-is so Gradio doesn't undo the user's click
    return current_state

#Gradio Interface
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
            output_format = gr.Radio(label = "Output format", choices = ["Plain text","Markdown","Microsoft Word (.docx)"])
            title = gr.Textbox(label="Title for your Word Document (Only used if Word is chosen)", value="My Report", visible = True)
            MDtable = gr.Checkbox(label="Includes table in output for Markdown", value = False, visible = True)
            MDSpecs = gr.Textbox(label="Add additional customisations to your prompt for a Markdown output", value="", visible = True)

    
    output_format.change(
        fn= gradio_filenametoggle, 
        inputs=output_format, 
        outputs=[title, MDtable, MDSpecs]
    )
    with gr.Row():
        with gr.Column(scale = 1, min_width = 300):
            startbutton = gr.Button("Start")

    #Functions
    output_format.change( fn= gradio_filenametoggle, inputs=output_format, outputs=[title, MDtable, MDSpecs])
    MDtable.input(fn=toggle_boolean, inputs=MDtable, outputs=MDtable)
    startbutton.click(fn = bigMan, inputs=[url, goal, API_Key, detailLevel, Lag, output_format, title, MDtable, MDSpecs], outputs=[text_output, markdown_output, file_output], api_name = "webscraper")

demo.launch()
