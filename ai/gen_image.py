from gradio_client import Client


def generate_image(prompt: str):
    client = Client("black-forest-labs/FLUX.1-dev")
    result = client.predict(
        prompt=prompt,
        seed=0,
        randomize_seed=True,
        width=1024,
        height=1024,
        guidance_scale=5.5,
        num_inference_steps=28,
        api_name="/infer"
    )
    # result = client.predict(
    #     prompt,
    #     # str in 'Prompt' Textbox component
    #     "(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, "
    #     "floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, "
    #     "blurry, amputation, (NSFW:1.25)",  # str in 'Negative prompt' Textbox component
    #     True,  # bool in 'Use negative prompt' Checkbox component
    #     0,  # float (numeric value between 0 and 2147483647) in 'Seed' Slider component
    #     512,  # float (numeric value between 512 and 2048) in 'Width' Slider component
    #     512,  # float (numeric value between 512 and 2048)in 'Height' Slider component
    #     6,  # float (numeric value between 0.1 and 20.0) in 'Guidance Scale' Slider component
    #     True,  # bool in 'Randomize seed' Checkbox component
    #     api_name="/run"
    # )
    # image_path = result[0][0].get("image")
    image_path = result[0]

    return image_path
