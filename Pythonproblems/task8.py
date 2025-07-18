#check if the bracket is balanced or not

def balance_he_k_nai(expression):
    stack = []
    for char in expression:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack:
                return False
            top = stack.pop()
            if (char == ")" and top != "(") or (char == "}" and top != "{") or (char == "]" and top != "["):
                return False
    return not stack

#stack me push kr rhe hain brackets order k  or phir pop same reverse order me hota he to okay but agar pop krte waqt koi condition last if se match nhi krta to false return kr deta he to kam kharab he 

s1="{[()]}"
print(balance_he_k_nai(s1))

s2="({)}"
print(balance_he_k_nai(s2))