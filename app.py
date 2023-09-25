
import os
import logging

import gradio as gr
from langchain.chat_models import ChatOpenAI
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, \
    LLMPredictor, PromptHelper

# read any environment variables needed 
os.environ.get('OPENAI_API_KEY')

# set LLM model to be used 
MODEL_NAME = 'gpt-3.5-turbo'

# declare global variables 
index = None


def construct_index(data_directory_path:str, index_file_name:str)-> GPTSimpleVectorIndex:
    """
    construct the index from input docs 
    """
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name=MODEL_NAME, max_tokens=num_outputs))

    documents = SimpleDirectoryReader(data_directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk(index_file_name)
    return index


def load_index(file_name:str)->GPTSimpleVectorIndex:
    index = GPTSimpleVectorIndex.load_from_disk(file_name)
    return index 


def chatbot(input_text:str)->str:
    response = index.query(input_text, response_mode="compact")
    return response.response


def create_UI_interface(query_func:object, UI_title:str)->object:
    iface = gr.Interface(fn=query_func,
                    inputs=gr.components.Textbox(lines=7, label="Enter your text"),
                    outputs=gr.components.Textbox(lines=7, label="Chatbot response"),
                    title=UI_title)
    return iface 


def is_file_exists(file_name:str)->bool:
    """
    checks if a file exists    
    """
    return os.path.isfile(file_name) 


def get_logger(logger_name:str, log_level:str)->object:
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.info("Hello World")
    return logger 


if __name__ == "__main__":
    
    # set share status to False when running in Huggingface spaces, 
    # when run locally should be set to True f need a public sharable link
    chatbot_share_status = False 
    create_index_file = False   

    UI_title = "Chatbot to learn about ML & DL"
    index_file_name = "index.json"

    try:
        logger = get_logger("custom_chatbot", logging.INFO)
    except Exception as e:
        print ("Failed to create logger with error {}".format(e))
        raise e 
    
    try:
        # create an index file if not present already   or when flag is set
        if not is_file_exists(index_file_name) or create_index_file:
            try: 
                logger.info("Attempting to create an index file ....")
                index = construct_index("docs", index_file_name)
                logger.info("successfully created an index file")
            except Exception as e:
                error_msg = "error occurred while constructing index with msg {}".format(e)
                raise Exception(error_msg)
        
        # load the index file 
        try:
            logger.info("loading index file : '{}' form disk ....".format(index_file_name))
            index = load_index(index_file_name)
            logger.info("successfully loaded index file ")
        except Exception as e:
            error_msg = "error occurred while constructing index with msg : {}".format(e)
            raise Exception(error_msg)

        # create and launch web interface
        iface = create_UI_interface(chatbot, UI_title)
        logger.info("successfully created an UI interface")
        iface.launch(share=chatbot_share_status)

    except Exception  as e :
        logger.error("{}".format(e))



