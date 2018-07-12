# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 14:10:27 2018

@author: narendra_mugada
"""
faq_mfa_response_dict = {
    "mfa_link": "MFA portal can be accessed @ https://rasssp.ad.infosys.com/MultiFactorAuth/  for registration. Use domain login credentials to login to the portal. Here, the user can activate MFA by registering their mobile number and personal PIN. There are 4 mandatory questions to be filled out to retrieve/change the PIN when forgotten. Also, you can set or change to a new PIN.",
}

faq_password_response_dict = {
    "password_link": "Please visit Sparsh (Webapps ? Account unlock / Password reset ? Registration) for a one-time registration for this facility or visit http://passaid."    
}

faq_accelerate_response_dict = {
    "accelarate_link": "To apply the job click here - http://iscls4apps/accelerate/home , and then click on FAQ for further details.,For any queries please contact : ZeroBench.HydSTP@infosys.com"
}

faq_emergency_response_dict = {
    "emergency_link": "Search for %Infosys Emergency% in Google Play Store and install the app.Complete the Multi-Factor authentication (MFA) process and activate your user profile"
}

faq_facilities_response_dict = {
    "gym":"Kindly make a request under Sparsh-> Harmony->facilites and Services or drop a mail to Facilities_Hyderabad@infosys.com for any queries",
    "membership card":"Kindly make a request under Sparsh-> Harmony->facilites and Services or drop a mail to Facilities_Hyderabad@infosys.com for any queries",
    "guest house":"Kindly make a request under Sparsh-> Harmony->facilites and Services or drop a mail to Facilities_Hyderabad@infosys.com for any queries",
    "member ship":"Kindly make a request under Sparsh-> Harmony->facilites and Services or drop a mail to Facilities_Hyderabad@infosys.com for any queries",
    "2 wheeler":"Kindly make a request under Sparsh-> Harmony->facilites and Services or drop a mail to Facilities_Hyderabad@infosys.com for any queries",
    "facility_link":"Please refer to www.sparsh.com/facilities"
}

faq_hr_response_dict = {
    "hr_link": "Kindly raise your queries / concerns  with your Unit-HR or contact :Hyd_HRD_ER@infosys.com"
}

faq_cag_response_dict = {
    "tax":"For any clarifications, please call the CAG Helpdesk or raise an AHD under Corporate Accounting Group(Loans & CLA)",
    "salary advance": "For any clarifications, please call the CAG Helpdesk or raise an AHD under Corporate Accounting Group(Loans & CLA)",
    "loan allowance": "For any clarifications, please call the CAG Helpdesk or raise an AHD under Corporate Accounting Group(Loans & CLA)",        
    "soft loan": "For any clarifications, please call the CAG Helpdesk or raise an AHD under Corporate Accounting Group(Loans & CLA)",        
    "salary loan": "For any clarifications, please call the CAG Helpdesk or raise an AHD under Corporate Accounting Group(Loans & CLA)",
    "cag_link":"Please refer www.sparsh.com/cag"
}

def getMFAInfo(entities):
    if len(entities) == 0:
        return faq_mfa_response_dict["mfa_link"]
    if len(entities) == 1:
        return faq_mfa_response_dict[entities[0]['value']]
    return "Sorry.." + faq_mfa_response_dict["mfa_link"]
    
def getPasswordInfo(entities):
    if len(entities) == 0:
        return faq_password_response_dict["password_link"]
    if len(entities) == 1:
        return faq_password_response_dict[entities[0]['value']]
    return "Sorry.." + faq_password_response_dict["password_link"]    

def getAccelarateInfo(entities):
    if len(entities) == 0:
        return faq_accelerate_response_dict["accelarate_link"]
    if len(entities) == 1:
        return faq_accelerate_response_dict[entities[0]['value']]
    return "Sorry.." + faq_accelerate_response_dict["accelarate_link"]

def getEmergencyInfo(entities):
    if len(entities) == 0:
        return faq_emergency_response_dict["emergency_link"]
    if len(entities) == 1:
        return faq_emergency_response_dict[entities[0]['value']]
    return "Sorry.." + faq_emergency_response_dict["emergency_link"]

def getFacilitiesInfo(entities):
    if len(entities) == 0:
        return faq_facilities_response_dict['facility_link']
    if len(entities) == 1:
        print("I'm here\n",entities)
        return faq_facilities_response_dict[entities[0]['value']]
    return "Sorry.." + faq_facilities_response_dict["facility_link"]

def getHRInfo(entities):
    if len(entities) == 0:
        return faq_hr_response_dict['hr_link']
    if len(entities) == 1:
        return faq_hr_response_dict[entities[0]['value']]
    return "Sorry.." + faq_hr_response_dict["hr_link"]

def getCAGInfo(entities):
    if len(entities) == 0:
        return faq_cag_response_dict['cag_link']
    if len(entities) == 1:
        return faq_cag_response_dict[entities[0]['value']]
    return "Sorry.." + faq_cag_response_dict["cag_link"]
