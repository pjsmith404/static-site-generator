from textnode import TextNode

def main():
    text_node = TextNode("This is some text", "bold", "https://boot.dev")
    print(text_node)
    print(text_node == text_node)
    print(text_node == "something")

    try:
        text_node = TextNode("This is not a valid text type", "something")
    except ValueError as e:
        print(e)

main()
