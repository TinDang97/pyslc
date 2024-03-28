# Created by tindang at 28/3/24
import requests

def get_stream_response(url: str, data: dict):
    with requests.post(url, json=data, stream=True) as response:
        for line in response.iter_content(chunk_size=1, decode_unicode=True):
            yield line

def main(port: int = 8888):
    url = f"http://0.0.0.0:{port}/chat/stream/"

    while True:
        chat_uid = input("Enter chat_uid: ")
        if chat_uid:
            break

    while True:
        payload = {
            "content": input("Enter your message: "),
            "chat_uid": chat_uid
        }
        if payload["content"] == "exit":
            break

        if not payload["content"]:
            continue

        print("Sending message...")
        print("Response: ", end="")
        for line in get_stream_response(url, payload):
            print(line, end="")
        print()

if __name__ == '__main__':
    main()
