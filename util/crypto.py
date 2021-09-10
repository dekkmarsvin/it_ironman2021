from types import SimpleNamespace
import json

def xor_two_str(a,b):
    a = int(a,base=16)
    b = int(b,base=16)
    return hex(a ^ b)

def HashID(Hash:SimpleNamespace):
    str1 = (xor_two_str(Hash.A1, Hash.A2)[2:]).upper()
    str2 = (xor_two_str(Hash.B1, Hash.B2)[2:]).upper()
    # print(f"str1:{str1}, str2:{str2}")
    return str1 + str2 
    
def Sign(APIService:str, Hash:SimpleNamespace, Nonce:str, HashID:str, Msg:str):
    print()

if __name__ == '__main__':
    A1 = "4D9709D699CA40EE"
    A2 = "5A4FEF83140C4E9E"
    B1 = "BC74301945134CB4"
    B2 = "961F67F8FCA44AB9"

    Hash = SimpleNamespace(A1 = A1, A2 = A2, B1 = B1, B2 = B2)
    print(HashID(Hash))
