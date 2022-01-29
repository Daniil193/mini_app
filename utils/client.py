import requests
from typing import Dict, Any

def print_info(answer: Dict) -> Any:
    """
    Print info from response
    
    :param answer: User's comment
    :return: 
    """
    print("-*-"*20)
    
    info_for_print = {k:v for k, v in answer.items() if v not in ['', 'Not toxic']}
    if len(info_for_print) != 0:
        for k, v in info_for_print.items():
                print(f"For comment is found <{k}> as <{v}>")
    else:
        print("Nothing wrong found")
        
    print("-*-"*20)
    print()
    
if __name__ == '__main__':
    
    base_url = "http://127.0.0.1:5000/prepare_comment/"
    
    while True:
        
        comm = input("Enter comment: ")
        
        response = requests.get(base_url, params = {"comment": comm})
        answer = response.json()
        
        print_info(answer)
            

