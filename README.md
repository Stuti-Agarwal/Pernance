# Pernance
An OpenAI enabled Personal Chatbot


This Chatbot uses LangChain's conversation module with a pretrained model
Do try it out.
This initial commit is as per Kniru's take home assessment. Will be making it opensource and fully-free soon 


# This is not the most optimized as:
  - Limit in context: the chatbot is going to loose context at one point and start to hallucinate. {ADDED AN ADDITIONAL PROMPT STATEMENT TO ALWAYS KEEP transactional data in mind. }
  - Limited tokens per prompt may not be the most appropriate if the user wants to attach an article
  - It does not have any visualizations
  - The chatbot needs to have alerts for when a person overspends 
  
# NEXT STEPS
- Adding additional pages and forms/ sockets for recording transactional data
- Embedding historical data in groups {category+week} to avoid overburdening the model
-Shifting to fully open source LLMS
- Integrating Tools Like Wolfram Alpha for better math, and wikipedia for updating pages 
- Fintuneing the model using indexing
- Webscraping off relevant website for latest affairs and using articles as context to further let the user question on current affairs data
- Instead of finetuning every hour will look at making a secondary QA model for latest events and will finetune only for larger news immediately
- Need to add an impact evaluation 

# What the next steps mean in terms of functionality
- Results will be more relevant to current affairs
- Completely free 
- More context
