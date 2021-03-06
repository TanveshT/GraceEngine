from engine.cards.card import Card
from engine.cards.sticker import Sticker

# from card import Card
# from sticker import Sticker

class Expression(Card):

    '''
    For information on card and attributes and methods, 
    refer parent class Card in card.py
    '''

    ''' 
    expression_list is list of tuples
    loc is position of the expression in the expression tuple
    '''
    def __init__(self, expression, card_number:int=0, loc:int=0):
        self.expression = []
        for item in expression[loc]:
            (sticker_type, sticker_value) = item
            sticker =Sticker(sticker_type,sticker_value)
            self.expression.append(sticker)
        card_id = "expression"
        card_type = [False, False, True, False, False, False, 0]
        super(Expression,self).__init__(card_id, card_type, card_number)
        self.code = ""
    
    def generate_card(self):
        self.card_dict["card_id"] = self.card_id
        self.card_dict["card_number"] = self.card_number
        self.card_dict["card_type"] = self.card_type
        self.card_dict["card_color"] = "color_math"
        self.card_dict["display"] = []
        for x in self.expression:
            sticker = {
                "val_type":"sticker",
                "sticker_name":x.sticker_type,
                "sticker_value":x.sticker_value
            }
            self.card_dict["display"].append(sticker)
        self.card_dict["external_dependant"] = {}
        self.card_dict["children"] = []

        return self.card_dict
    
    def generate_code(self, nesting_level = 0):
        self.code = ""
        if self.expression == []:
            return None
        for item in self.expression:
            self.code += " " + item.sticker_value
        return self.code

if __name__ == "__main__":
    test_card_1 = Expression([[("variable","count"),("operator", "+"),("number", "2")]],0,0)
    for item in test_card_1.expression:
        print(item.sticker_type, item.sticker_value,type(item))
    print("Card: \n",test_card_1.generate_card())
    print("Code: \n",test_card_2.generate_code())

    test_card_2 = Expression([[("variable","apple"),("operator", "-"),("number", "2")]],0,0)
    for item in test_card_2.expression:
        print(item.sticker_type, item.sticker_value,type(item))
    print("Card: \n",test_card_2.generate_card())
    print("Code: \n",test_card_2.generate_code())