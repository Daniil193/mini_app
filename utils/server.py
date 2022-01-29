
from flask import Flask
from flask import request
from detoxify import Detoxify
from typing import Dict
import re

app = Flask(__name__)


class CommentInfo():
    
    def __init__(self, device_for_calc="cuda", model_type="multilingual"):
        
        self.dev_for_cals = device_for_calc
        self.model_type = model_type
        self.interest_toxic_labels = ["identity_attack", "insult", "threat"]
        self.toxic_threshold = 0.7
        self.feats_to_join = ["t.me/joinchat", "youtube.com/channel"]
        try:
            self.detox_model = Detoxify(self.model_type, device=self.dev_for_cals)
        except:
            self.detox_model = Detoxify(self.model_type, device="cpu")
    
    
    @staticmethod
    def get_urls_from_comment(comment: str) -> str:
        """
        Regular expression for extracting urls from comment, url NOT contain "tradingview.com/"

        :param comment: User's comment
        :return: urls from comment
        """
        regx = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        urls = re.findall(regx, comment)
        filtered_urls = [i for i in urls if "tradingview.com/" not in i]
        
        return " ]|[ ".join(filtered_urls)
    
    @staticmethod
    def search_hash_address_wallet(comment: str) -> str:
        """
        Regular expression for search 4 types of hash-addresses

        :param comment: User comment
        :return: founded wallets
        """
        regx = r"""0x[a-fA-F0-9]{40}|
                   [13][a-km-zA-HJ-NP-Z1-9]{25,34}|
                   X[1-9A-HJ-NP-Za-km-z]{33}|
                   4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}"""
        
        wallets = re.findall(regx, comment)
        
        return " ]|[ ".join(wallets)
    
    def search_calls_to_join_by_url(self, urls: str) -> str:
        """
        Find urls which contain templates of calls to join, for example: "t.me/joinchat"

        :param urls: List of extracted urls
        :return: urls which contain templates
        """
        urls_ = urls.split(" ]|[ ")
        calls = [url for feat in self.feats_to_join for url in urls_ if feat in url]
        
        return " ]|[ ".join(calls)
    
    def comment_toxic_level(self, comment: str) -> str:
        """
        Define toxic level of comment 
        
        :param comment: User's comment
        :return: level toxicity of comment
        """
        result = self.detox_model.predict([comment])
        result_interest_label = {k: v[0] for k,v in result.items() if k in self.interest_toxic_labels}
        
        if sum(result_interest_label.values()) >= self.toxic_threshold:
            
            return max(result_interest_label, key=result_interest_label.get) # get key with max value
        
        return "Not toxic"
    
    def prepare_comment(self, comment: str) -> Dict:
        """
        Analyze comment on toxicity, calls_to_join, wallets
        
        :param comment: User's comment
        :return: level toxicity of comment
        """
        
        if type(comment) != str:
            return dict()
        
        toxic_level = self.comment_toxic_level(comment)
        
        urls = self.get_urls_from_comment(comment)
        
        wallets = self.search_hash_address_wallet(comment)
        
        calls_to_join = self.search_calls_to_join_by_url(urls)
        
        return {"toxic_level": toxic_level,
                "urls": urls,
                "wallets": wallets,
                "calls_to_join": calls_to_join}




@app.route('/prepare_comment/')
def prepare_comment():
    
    comment = request.args.get('comment')
    
    return c_info.prepare_comment(comment)

if __name__ == '__main__':
    
    c_info = CommentInfo()
    app.run(debug = True)
    
    
    
    