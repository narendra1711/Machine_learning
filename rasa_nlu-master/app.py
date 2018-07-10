from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Interpreter

training_data = load_data('data/emailsupport.json')
trainer = Trainer(config.load("config/config.yml"))
trainer.train(training_data)
model_directory = trainer.persist('./models/')

intent_response_dict = {
    "login": ["Login server was down. It is up now. Please check."],
    "change":["Go to URL : password.reset.com, Enter you login id, enter password received, reset the password"],
    "problem":["Please check the LAN connection and restart the computer"],
    "product":["First, connect a network cable to your laptop to the red port on your workstation. Run ipconfig /all on your command prompt. Share WiFi Mac or Hardware address to the IT team. IT team then adds your MAC ID to enable WiFi access","First, connect a network cable to your laptop to the red port on your workstation. Run ipconfig /all on your command prompt. Share WiFi Mac or Hardware address to the IT team. IT team then adds your MAC ID to enable WiFi access"],
    "device":["First, connect a network cable to your laptop to the red port on your workstation. Run ipconfig /all on your command prompt. Share WiFi Mac or Hardware address to the IT team. IT team then adds your MAC ID to enable WiFi access","First, connect a network cable to your laptop to the red port on your workstation. Run ipconfig /all on your command prompt. Share WiFi Mac or Hardware address to the IT team. IT team then adds your MAC ID to enable WiFi access"],
    "cache":["Microsoft Internet Explorer/Google Chrome users can go to 'Tools' (or the little cog icon in the top left), then go to 'Safety' and choose 'Delete browsing history...', you can then choose to delete your Internet cookies. In Google Chrome, go to 'More Tools' and choose 'Clear browsing data...'. Firefox users can go to 'History', then choose 'Clear recent history...'."],
    "faqlink":['You can check all the answers here <a href="http://sparsh/faq-on-email-support.pdf</a>']
}

# where `model_directory points to the folder the model is persisted in
try:
    interpreter = Interpreter.load(model_directory)
    search = "Tell me about MFA Access"
    response = interpreter.parse(search)
    intent = str(response['intent']['name'])
    entities = response['entities']
    if(intent.startswith('faq_')):
        if len(entities) == 0:
            print("Could not find out specific information about this ..." +  str(intent_response_dict["faqlink"]))
        elif len(entities) == 1:
            print(intent_response_dict[entities[0]['entity']])
        else:
            for ent in entities:
                qtype = ent["type"]
                qval = ent["entity"]
                if qtype == "gst-query-value":
                    print(intent_response_dict[qval])
        
        print(intent_response_dict[entities[0]])
except Exception as e:
    print(e)
            

    
