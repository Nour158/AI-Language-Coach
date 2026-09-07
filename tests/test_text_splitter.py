from ai.rag.text_splitter import StructureAwareTextSplitter


sample_text = """
# Present Perfect

The present perfect connects past actions to the present.

## Structure

Subject + have/has + past participle.

## Examples

I have visited London.
She has finished her homework.

## Common Mistakes

I have went to London.
I have gone to London.

# Past Simple

The past simple is used for completed actions in the past.

## Examples

I visited London last year.
She finished her homework yesterday.
"""


splitter = StructureAwareTextSplitter(
    chunk_size=150,
    overlap=20
)

chunks = splitter.split_text(sample_text)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {i} ---")
    print(chunk)