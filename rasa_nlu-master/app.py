from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Interpreter
from engine import getMFAInfo,getPasswordInfo,getAccelarateInfo,getEmergencyInfo,getFacilitiesInfo,getHRInfo,getCAGInfo

training_data = load_data('data/emailsupport.json')
trainer = Trainer(config.load("config/config.yml"))
trainer.train(training_data)
model_directory = trainer.persist('./models/')

interpreter = Interpreter.load(model_directory)

# where `model_directory points to the folder the model is persisted in
def get_rasaResponse():
    try:
        if(intent.startswith('FAQ-')):
            if(intent == "FAQ-MFA"):
                response_text = getMFAInfo(entities)               
            elif(intent == "FAQ-Password"):
                response_text = getPasswordInfo(entities)
            elif(intent == "FAQ-Accelerate"):
                response_text = getAccelarateInfo(entities)
            elif(intent == "FAQ-Emergency"):
                response_text = getEmergencyInfo(entities)
            elif(intent == "FAQ-Facilities"):
                response_text = getFacilitiesInfo(entities)
            elif(intent == "FAQ-HR"):
                response_text = getHRInfo(entities)
            elif(intent == "FAQ-CAG"):
                response_text = getCAGInfo(entities)
        else:
            print("Given mail comes under L1 or L2 or L3")
        return response_text
    except Exception as e:
        print(e)

search = "how to get a soft loan" 
response = interpreter.parse(search)
intent = str(response['intent']['name'])
entities = response['entities']
get_rasaResponse()
    
