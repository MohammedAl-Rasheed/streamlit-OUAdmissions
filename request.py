import os
import openai

openai.api_key = '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'
question = "What is this person's average: \n99.75 (Gr12 only) --> 99 (including gr11 english but my english teacher never gave out 96)"

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt= question,
  temperature=0.7,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

res = response.choices[0].text
# keep only numerical values and symbolols with in res using regex
res = (''.join((ch if ch in '0123456789.' else ' ') for ch in res))
# clear white space from res
res = ' '.join(res.split())
res = [float(i) for i in res.split()]
print(res[0])

