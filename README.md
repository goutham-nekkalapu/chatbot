
- Install anaconda 
  - Download this script : https://repo.anaconda.com/archive/Anaconda3-2023.03-1-Linux-x86_64.sh
  - Make the script executable : chmod +x Anaconda3-2023.03-1-Linux-x86_64.sh
  - Run the script : ./Anaconda3-2023.03-1-Linux-x86_64.sh

- Create a virtual python environment 
  - conda env create --name chatbot --file=chatbot_env.yml

- Switch to 'chatbot' python environment 
  - conda activate chatbot

- Place the pdfs that we are interested in 'docs' directory 

- Get OpenAI token
  - Login into your OpenAI's account
  - Go to this URL : https://platform.openai.com/account/api-keys
  - If there is no Key that is already created, create a new secret key 
  - Copy the secret key 

- set the ket in environment variable 
  - populate the above key value created in set_env.sh file 
  - run the script to set the env in your terminal 

- Run the script
  - Python app.py

- Using the UI
  - Once script is run, initially it will take some time to create 'index.json' 
  - In terminal, you will see a local URL : http://127.0.0.1:7860/ 
  - You can interact with the contents of your PDF using the chatbot interface that this URL 


## Deploying the chat bot to host to public 
- When we intend to deploy the final chatbot to wide users, we need not necessarily run it in our local machine. We can host it in any of the cloud providers or services like 'huggingface'

- Here we will cover the steps to  host on hugginface's spaces 

- Create account with huggingface : https://huggingface.co/

- Create a new huggingface space
  - go to : https://huggingface.co/spaces
  - choose 'create new space' to create one
  - in the next page for 'Select the Space SDK' section, 'choose Gradio'
  - choose hardware as per need, this can be changed at any time dynamically 


- Changes needed to the script
  - name it as app.py ; as this is the file name that hosting service will look for 
  - comment out the line , where we construct 'index.json'. 
    - index = construct_index("docs")
  - change the 'iface.launch(share=True)' to 'iface.launch(share=False)'; this needs to be done as we can not host the app publicly from the huggingface spaces 

 
- Uploading your chatbot files to spaces:
  - go to your newly created space
  - on the right top corner choose 'files' tab and upload the following files:
    - app.py
    - index.json 
    - requirements.txt

- Once you upload, go to 'app' tab, you will see that the app is building, will take few minutes for it.
  After that you can start using it 

- At the bottom page, open 'Use via API'; you will find a code snippet on how you can use what you have deployed through API calls from other applications of your choice. 

- Do explore the other tabs like 'settings' for various compute and storage options 

- For other UI related enhancements and CLI way of deploying this application, refer to below link:
  - https://www.tanishq.ai/blog/gradio_hf_spaces_tutorial

