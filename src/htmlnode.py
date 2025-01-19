class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        if (
                self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props
            ):
            return True

        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""

        return "".join(
            map(lambda item: f' {item[0]}="{item[1]}"', self.props.items())
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")

        if self.tag == None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Invalid HTML: no tag")

        if self.children == None:
            raise ValueError("Invalid HTML: no children")
 
        return f"<{self.tag}{self.props_to_html()}>{children_to_html(self.children)}</{self.tag}>"

def children_to_html(children):
    if len(children) < 1:
        return ""

    return f"{children[0].to_html()}{children_to_html(children[1:])}"
