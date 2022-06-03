from pprint import pprint
import nltk
#nltk.download('stopwords')
from Questgen import main
qe= main.BoolQGen()
payload = {
            "input_text": "The exact cause of migraines is unknown, but they're thought to be the result of abnormal brain activity temporarily affecting nerve signals, chemicals and blood vessels in the brain. Its not clear what causes this change in brain activity, but its possible that your genes make you more likely to experience migraines as a result of a specific trigger."
        }
output = qe.predict_boolq(payload)
pprint (output)

qg = main.QGen()
output = qg.predict_mcq(payload)
pprint (output)
