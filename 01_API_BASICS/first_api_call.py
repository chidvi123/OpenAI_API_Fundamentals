from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-6-astra",
    input="Write a one-sentence bedtime story about a unicorn.",
    # instructions :"...." # give model behaviour / system-lvl instructions
    # "temperature" :"..." # controls randomness 
        # low temperature - More predictable / consistent 
        # High temperature - Moe variation / randomness
    # "top_p" :"..." #control sampling / probability distribution 
        #cummulative probability 
    # top_k :"...."
        #only consider top K most probable tokens
    # "max_output_tokens" :"..." #limit how much the model can generate
    # text 
        # important when you start leaning Structured Outputs
    # tools
        # allow model to interact with capabilities outside simple text generation
        # like example web search , file search , function calling 
    #tool_choice
        # which tool should you use 
    #stream
        # response arrives incrementally instead of waiting for complete output
    # previous_response_id
        # useful when you want to continue from a previous response
    # metadata
        # This is basically your applications extra info attached to a request/response
)

print(response.output_text)