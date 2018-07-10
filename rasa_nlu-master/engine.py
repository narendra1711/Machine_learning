
##dict of response for each type of intent
intent_response_dict = {
    "login": ["Login server was down. It is up now. Please check."],
    "LogonIssue":["Go to URL : password.reset.com, Enter you login id, enter password received, reset the password"],
    "Access":["First, connect a network cable to your laptop to the red port on your workstation. Run ipconfig /all on your command prompt. Share WiFi Mac or Hardware address to the IT team. IT team then adds your MAC ID to enable WiFi access","First, connect a network cable to your laptop to the red port on your workstation. Run ipconfig /all on your command prompt. Share WiFi Mac or Hardware address to the IT team. IT team then adds your MAC ID to enable WiFi access"],
    "Cleanup":["Microsoft Internet Explorer users can go to 'Tools' (or the little cog icon in the top left), then go to 'Safety' and choose 'Delete browsing history...', you can then choose to delete your Internet cookies. In Google Chrome, go to 'More Tools' and choose 'Clear browsing data...'. Firefox users can go to 'History', then choose 'Clear recent history...'."],
    "faqlink":['You can check all the answers here <a href="http://sparsh/faq-on-email-support.pdf</a>']
}

def getFAQInfo(entities):
    if entities == None:
        return "Could not find out specific information about this ..." +  intent_response_dict["faq_link"]
    if len(entities) == 1:
        return intent_response_dict[entities[0]]
    for ent in entities:
        qtype = ent["type"]
        qval = ent["entity"]
        if qtype == "gst-query-value":
            return intent_response_dict[qval]

        return intent_response_dict[entities[0]]
    return "Sorry.." + intent_response_dict["faq_link"]
