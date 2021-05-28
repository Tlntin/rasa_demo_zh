from rasa.nlu.tokenizers.tokenizer import Tokenizer, Token
from typing import Dict, Text, Any, List
from rasa.shared.nlu.training_data.message import Message

class MyTokenizer(Tokenizer):
    """
    自定义分词器，为了配合bert，不过用了一下并不好用，先放着。
    """
    language_list = ["zh"]
    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        """Construct a new Tokenizer."""
        super().__init__(component_config)
        from transformers import AutoTokenizer
        self.my_tokenizer = AutoTokenizer.from_pretrained("data/model")

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["transformers"]

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        """Construct a new Tokenizer."""
        text = message.get(attribute)
        tokenized = self.my_tokenizer.tokenize(text)
        # print(tokenized)
        tokenized = [(r, text.index(r))  if r in text else (r, 0) for r in tokenized]
        # print(tokenized)
        tokens = [Token(word, start) for (word, start) in tokenized]
        return self._apply_token_pattern(tokens)