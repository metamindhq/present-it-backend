import replicate
import time

input = {
    "prompt": "The world's largest black forest cake, the size of a building, surrounded by trees of the black forest"
}

start_time = time.time()
output = replicate.run(
    "black-forest-labs/flux-schnell",
    input=input
)
print("Time taken: ", time.time() - start_time)
print(output)