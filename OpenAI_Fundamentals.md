# OpenAI API Fundamentals

> Notes for Week 4 --- OpenAI API & Prompt Engineering\
> Focus: API fundamentals, tokens, embeddings, parameters, structured
> outputs, validation, errors, security, cost and latency.

------------------------------------------------------------------------

## 1. What is an API?

An API (Application Programming Interface) is an interface that allows
one application to communicate with another service.

For an OpenAI application:

``` text
Python Application
        ↓
     OpenAI API
        ↓
      Model
        ↓
    Response
        ↓
Python Application
```

The API is the communication layer. The model performs the AI
processing.

------------------------------------------------------------------------

# 2. API Authentication

## What is authentication?

Authentication answers:

> "Who is making this API request, and are they allowed to use the API?"

OpenAI API requests are authenticated using an **API key**.

Conceptually:

``` text
Python Application
        ↓
API Key
        ↓
OpenAI API
        ↓
Authentication check
        ↓
Model
```

OpenAI's API uses API keys for authentication. At the HTTP level, the
key is sent using Bearer authentication:

``` text
Authorization: Bearer OPENAI_API_KEY
```

In the OpenAI Python SDK, we normally do not manually write this header.
The SDK reads the key and handles the request.

Example:

``` python
from openai import OpenAI

client = OpenAI()
```

If `OPENAI_API_KEY` is available as an environment variable, the SDK can
automatically use it.

### Important

An API key is a **secret credential**.

Never:

-   Put the real key directly into source code
-   Commit the key to GitHub
-   Put the key in frontend/browser code
-   Share the key with other people

Use environment variables or a secure key-management system instead.

Example environment variable:

``` text
OPENAI_API_KEY=your_api_key_here
```

For local development, a `.env` file can be used with a package such as
`python-dotenv`, but the `.env` file should be added to `.gitignore`.

Example:

``` gitignore
.env
```

------------------------------------------------------------------------

# 3. OpenAI Python SDK and Client

The OpenAI SDK is a Python library that provides convenient methods for
communicating with the OpenAI API.

``` python
from openai import OpenAI

client = OpenAI()
```

### What is `client`?

`client` is an instance of the SDK's `OpenAI` client class.

It provides the methods used to communicate with OpenAI services.

For example:

``` python
response = client.responses.create(
    model="YOUR_MODEL",
    input="What is Python?"
)
```

Think of:

``` text
client
  ↓
SDK object used by our Python application
  ↓
communicates with OpenAI API
```

------------------------------------------------------------------------

# 4. Basic API Request and Response Flow

A typical flow is:

``` text
User Input
    ↓
Python Application
    ↓
Construct API Request
    ↓
Authentication
    ↓
OpenAI API
    ↓
Selected Model
    ↓
Model Processing
    ↓
API Response
    ↓
Python Application
    ↓
Final Output
```

Example:

``` python
response = client.responses.create(
    model="YOUR_MODEL",
    input="What is Python?"
)

print(response.output_text)
```

The exact response fields depend on the API endpoint and SDK object
being used.

------------------------------------------------------------------------

# 5. Models and Model Selection

A model is the AI model that processes the request.

Different models can differ in:

-   Capability
-   Reasoning ability
-   Speed
-   Cost
-   Context capacity
-   Supported features

Model selection should be based on the application's requirements.

Do not choose a model only because it is the largest or newest.
Consider:

``` text
Capability
    ↕
Cost
    ↕
Latency
```

------------------------------------------------------------------------

# 6. Instructions and Message Roles

When working with model inputs, different roles can communicate
different types of information.

## System instructions

System-level instructions provide high-level behavior or rules for the
model.

Example:

``` text
You are a helpful programming tutor.
```

They are used to establish behavior or constraints.

## Developer instructions

Developer instructions represent instructions supplied by the
application/developer.

Example:

``` text
Always return the answer in JSON.
```

They are useful for defining application-level behavior and constraints.

## User instructions

The user message contains the user's request or user-provided context.

Example:

``` text
Explain Python lists.
```

### Instruction hierarchy

A simplified mental model is:

``` text
System / Developer instructions
            ↓
        User request
            ↓
          Model
```

OpenAI's current API documentation states that developer/system
instructions take precedence over user instructions. For newer reasoning
models, developer messages are used in place of older system-message
patterns in some APIs.

### Important

The roles are not just labels.

They help separate:

-   High-level behavior
-   Application/developer requirements
-   User requests

Example:

``` text
Developer:
"Answer in exactly 3 bullet points."

User:
"Explain Python in 10 paragraphs."
```

The application-level instruction can constrain the response despite the
user's request.

------------------------------------------------------------------------

# 7. Important API Parameters

## Temperature

Controls randomness/variation in generation where supported.

Conceptually:

``` text
Lower temperature
→ more predictable output

Higher temperature
→ more variation
```

It is not a direct "creativity slider" and its availability/behavior
depends on the model/API.

------------------------------------------------------------------------

## Top-p

`top_p` controls token selection using **cumulative probability**.

Suppose the model is choosing the next token and its candidate
probabilities are:

``` text
Python     0.50
Java       0.20
C++        0.15
Rust       0.10
Go         0.05
```

If:

``` text
top_p = 0.70
```

the model considers candidates until their cumulative probability
reaches the threshold:

``` text
Python = 0.50
Python + Java = 0.70
```

So the candidate set can be approximately:

``` text
Python
Java
```

If:

``` text
top_p = 0.90
```

the cumulative set could include:

``` text
Python  0.50
Java    0.20
C++     0.15
Rust    0.10
```

because the cumulative probability reaches/exceeds 0.90.

### Important

`top_p` does NOT mean:

> "Take the top P words."

It means:

> "Consider the smallest set of likely next-token candidates whose
> cumulative probability reaches the chosen threshold."

------------------------------------------------------------------------

## Top-k

`top_k` limits the candidate pool to the K highest-probability next
tokens.

Example:

``` text
top_k = 3
```

means the model considers the three highest-probability candidates.

Important: `top_k` is not a universal parameter across all OpenAI
models/APIs. Always check whether the selected model/API supports it.

------------------------------------------------------------------------

## max_output_tokens

Limits how many output tokens the model can generate.

Example:

``` python
max_output_tokens=300
```

means:

> Generate at most 300 output tokens.

It does NOT mean 300 words.

``` text
1 token ≠ 1 word
```

Tokenization determines how text is divided into tokens.

------------------------------------------------------------------------

# 8. Tokenization

Tokenization converts text into tokens that a model can process.

Conceptually:

``` text
"I love Python"
       ↓
Tokenizer
       ↓
["I", " love", " Python"]
```

The exact result depends on the tokenizer.

## Tokenization types

### 1. Word-level tokenization

Splits text mainly into whole words.

``` text
"I love Python"
        ↓
["I", "love", "Python"]
```

Simple, but it has problems with unknown words and large vocabularies.

### 2. Character-level tokenization

Splits text into individual characters.

``` text
"Hello"
   ↓
["H", "e", "l", "l", "o"]
```

Very flexible, but produces many units.

### 3. Subword tokenization

Splits words into smaller meaningful pieces.

``` text
"unbelievable"
      ↓
["un", "believ", "able"]
```

This is especially important for modern NLP/LLMs.

Common subword approaches include:

-   BPE (Byte Pair Encoding)
-   WordPiece
-   Unigram

### 4. Byte-level approaches

Some tokenization systems operate using byte-level representations as
part of their process. This helps handle arbitrary text and unusual
characters.

### Practical OpenAI point

When using an OpenAI model through the API, you normally do **not
manually choose a tokenizer** for the request. The model/tokenizer
configuration handles tokenization.

------------------------------------------------------------------------

# 9. Tokens vs Token IDs

These are different concepts.

### Token

A token is a piece of text produced by tokenization.

### Token ID

A token ID is a numerical identifier assigned to a token in a
tokenizer's vocabulary.

Conceptually:

``` text
" Python"
    ↓
token
    ↓
token ID: 8392
```

The actual number is tokenizer/model dependent.

The general flow is:

``` text
Text
 ↓
Tokens
 ↓
Token IDs
```

------------------------------------------------------------------------

# 10. Embeddings

Embedding is a separate concept from tokenization.

A simplified model pipeline is:

``` text
Text
 ↓
Tokenization
 ↓
Token IDs
 ↓
Learned numerical representations
 ↓
Transformer
 ↓
Output
```

A token ID by itself is just an integer identifier. A learned
embedding/representation maps it into a vector that the neural network
can work with.

Conceptually:

``` text
"king"
  ↓
token ID
  ↓
embedding
  ↓
[0.21, 0.73, -0.14, ...]
```

The actual vectors are much larger and are learned by the model.

## Types of embeddings / embedding approaches

### 1. Static word embeddings

Traditional NLP methods assign a relatively fixed vector to a word.

Examples:

-   Word2Vec
-   GloVe
-   FastText

### 2. Contextual embeddings

Transformer-based models can produce representations that depend on the
surrounding context.

For example, the representation of:

``` text
"I went to the bank to deposit money."
```

can differ from:

``` text
"I sat on the river bank."
```

because the context changes the meaning.

### 3. Sentence/document embeddings

An embedding model can represent a larger piece of text as a vector.

These are commonly used for:

-   Semantic search
-   Similarity comparison
-   Clustering
-   Recommendation
-   RAG

### Important distinction

There are two related but different ideas:

``` text
LLM internal representations
        vs
Dedicated embedding model/API
```

Do not treat them as the same API feature.

------------------------------------------------------------------------

# 11. Input Tokens and Output Tokens

API usage can be measured in tokens.

``` text
Input tokens
+
Output tokens
=
Total token usage
```

For example:

``` text
Input:  1,000 tokens
Output:   500 tokens
--------------------
Total:  1,500 tokens
```

Actual API response objects can expose usage information such as input
tokens, output tokens, and total tokens, depending on the endpoint.

------------------------------------------------------------------------

# 12. How API Cost Is Calculated

API pricing is generally based on the model and the amount/type of
usage.

For text generation, the basic idea is:

``` text
Input token cost
+
Output token cost
=
Total token cost
```

Because providers publish prices per a large number of tokens (commonly
per 1 million tokens), the calculation is:

``` text
Input cost =
(input tokens / 1,000,000) × input price per 1M tokens

Output cost =
(output tokens / 1,000,000) × output price per 1M tokens

Total =
Input cost + Output cost
```

## Clear example

Suppose a hypothetical model costs:

``` text
Input:  $2 per 1M tokens
Output: $8 per 1M tokens
```

Your request uses:

``` text
Input:  10,000 tokens
Output:  2,000 tokens
```

Then:

``` text
Input cost:
10,000 / 1,000,000 × $2
= $0.02

Output cost:
2,000 / 1,000,000 × $8
= $0.016

Total:
$0.02 + $0.016
= $0.036
```

So that request would cost **\$0.036** under this hypothetical pricing.

### Important

The actual price is **model-dependent and can change**. Some
models/pricing plans can also have different rates for cached input,
long context, batch processing, or other features.

Always check the current official pricing page before calculating real
costs.

------------------------------------------------------------------------

# 13. Reasoning / Reasoning Effort

Some models support reasoning controls.

A reasoning setting can control how much reasoning effort the model
uses.

Conceptually:

``` text
Lower effort
→ potentially less computation / lower latency

Higher effort
→ potentially more computation / higher latency
```

The exact parameter names and supported values depend on the model/API.

Do not assume there is a universal:

``` python
thinking=True
```

parameter.

The API concept is **reasoning**.

------------------------------------------------------------------------

# 14. Latency

Latency is the time taken for an API operation/response.

Factors that can affect latency include:

-   Model
-   Input size
-   Output length
-   Reasoning effort
-   Network conditions
-   Service/load conditions

For an interactive application, latency matters because users experience
the delay between sending a request and seeing a response.

------------------------------------------------------------------------

# 15. Streaming

Without streaming:

``` text
Request
   ↓
Wait
   ↓
Complete response
   ↓
Display
```

With streaming:

``` text
Request
   ↓
First response chunk
   ↓
Next chunk
   ↓
Next chunk
   ↓
...
```

The application can display output as it arrives instead of waiting for
the complete response.

This can improve perceived responsiveness.

------------------------------------------------------------------------

# 16. Structured Outputs

Normal model output can be free-form text.

For an application, we may instead want predictable structured data.

Example:

``` json
{
  "category": "Electronics",
  "subcategory": "Headphones",
  "confidence": 0.95
}
```

Structured Outputs are useful when application code needs predictable
fields and types.

Important distinction:

``` text
"Please return JSON"
        ≠
Structured Outputs
```

A natural-language instruction asks the model to follow a format.

Structured Outputs provide a defined output structure/schema that the
application can rely on more reliably.

------------------------------------------------------------------------

# 17. JSON

JSON is a common data format for structured information.

Example:

``` json
{
  "name": "John",
  "age": 22,
  "city": "Chennai"
}
```

JSON represents the actual data.

------------------------------------------------------------------------

# 18. Schema

A schema is a blueprint/ruleset describing the expected structure and
types of data.

Example:

``` text
name → string
age → integer
city → string
```

Think:

``` text
JSON   = actual data
Schema = rules describing expected data
```

------------------------------------------------------------------------

# 19. Validation

Validation checks whether received data conforms to the expected schema.

Valid:

``` json
{
  "name": "John",
  "age": 22
}
```

Invalid for a schema requiring `name` to be a string and `age` to be an
integer:

``` json
{
  "name": 123,
  "age": "twenty"
}
```

### Important distinction

Schema validation does not automatically prove that the information is
factually correct.

For example:

``` json
{
  "name": "John",
  "age": 999
}
```

may be schema-valid if `age` only requires an integer, even though the
value may be factually wrong.

Therefore:

``` text
Schema validation
≠
Factual correctness
```

------------------------------------------------------------------------

# 20. Pydantic

Pydantic is a Python library commonly used to define and validate
structured data.

Example:

``` python
from pydantic import BaseModel

class ProductResult(BaseModel):
    category: str
    subcategory: str
    confidence: float
```

This defines:

``` text
category     → string
subcategory  → string
confidence   → float
```

The data can then be validated against this model.

Conceptually:

``` text
Model response
      ↓
Structured data
      ↓
Pydantic model
      ↓
Validation
      ↓
Validated Python object
```

------------------------------------------------------------------------

# 21. API Error Handling

An API request can fail.

Common HTTP/API errors include:

  Status   General meaning
  -------- -----------------------------
  400      Bad/invalid request
  401      Authentication problem
  403      Permission/access problem
  404      Resource/model not found
  429      Rate limit or quota problem
  5xx      Server-side error

Examples we encountered during hands-on:

``` text
429 → insufficient quota / no API credits
404 → model not found or unavailable
```

A production application should handle errors rather than allowing every
API failure to crash the application.

Conceptually:

``` python
try:
    response = client.responses.create(...)
except Exception as e:
    print("API request failed:", e)
```

In production code, prefer handling specific SDK/API exception types
when appropriate.

------------------------------------------------------------------------

# 22. API Error vs Validation Error

These are different.

## API error

The request itself failed.

``` text
Application
    ↓
API
    ↓
❌ Request failed
```

Example:

``` text
401 Unauthorized
```

## Validation error

The API returned data, but the data does not satisfy your expected
schema.

``` text
Application
    ↓
API
    ↓
✅ Response received
    ↓
❌ Schema validation failed
```

Therefore:

``` text
API error
= request/communication/service problem

Validation error
= received data does not match expected structure/rules
```

------------------------------------------------------------------------

# 23. API Key Security Summary

Use:

``` text
Environment variable
        ↓
OPENAI_API_KEY
        ↓
OpenAI SDK
        ↓
API request
```

Do not use:

``` python
client = OpenAI(
    api_key="REAL_SECRET_KEY"
)
```

inside code that may be committed to GitHub.

For local development:

``` text
.env
```

can contain the secret, while:

``` gitignore
.env
```

keeps it out of Git.

A safe example file can be:

``` text
.env.example
```

with:

``` text
OPENAI_API_KEY=your_api_key_here
```

Never commit the real secret.

If a real API key is accidentally exposed, revoke/rotate it rather than
relying only on deleting the exposed text.

------------------------------------------------------------------------

# 24. Complete Mental Model

Keep this overall flow in mind:

``` text
User
 ↓
Python Application
 ↓
API Client / SDK
 ↓
API Key Authentication
 ↓
OpenAI API
 ↓
Model
 ↓
Tokenization
 ↓
Token IDs
 ↓
Learned numerical representations
 ↓
Transformer / Reasoning
 ↓
Output
 ↓
Structured Output / JSON (when requested)
 ↓
Schema Validation
 ↓
Python Application
 ↓
User
```

And around the process:

``` text
Parameters → influence generation
Tokens → measure model input/output usage
Pricing → converts usage into API cost
Latency → measures response time
Error handling → handles failures
```

------------------------------------------------------------------------

# 25. Quick Revision Table

  -----------------------------------------------------------------------
  Topic                               Remember this
  ----------------------------------- -----------------------------------
  API                                 Interface between your application
                                      and a service

  API key                             Secret credential used for
                                      authentication

  SDK                                 Library that makes API
                                      communication easier

  Client                              SDK object used to make requests

  Model                               AI model that processes the request

  System                              High-level model
                                      behavior/instructions

  Developer                           Application-level instructions

  User                                User's request/context

  Temperature                         Controls output variation where
                                      supported

  Top-p                               Chooses from candidates within
                                      cumulative probability

  Top-k                               Limits candidates to K
                                      highest-probability tokens where
                                      supported

  Max output tokens                   Maximum generated output tokens

  Token                               Piece of text produced by
                                      tokenization

  Token ID                            Numeric identifier for a token

  Embedding                           Learned numerical vector
                                      representation

  Input tokens                        Tokens sent to the model

  Output tokens                       Tokens generated by the model

  Cost                                Based on usage and the model's
                                      pricing

  Reasoning                           Additional model
                                      reasoning/computation where
                                      supported

  Latency                             Response time

  Streaming                           Receive/display output
                                      progressively

  Structured output                   Predictable structured response

  JSON                                Data representation format

  Schema                              Rules/blueprint for expected data

  Validation                          Checks data against the schema

  Pydantic                            Python tool for defining/validating
                                      data

  API error                           Request/service failure

  Validation error                    Returned data fails schema
                                      validation
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Official References

-   OpenAI Developer Quickstart
-   OpenAI API Reference --- Authentication
-   OpenAI API Reference --- Messages / Instructions
-   OpenAI API Pricing

These should be checked for current model-specific parameters and
pricing because the API evolves over time.
