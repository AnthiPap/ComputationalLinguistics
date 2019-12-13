import re
import argparse

def argparser():
    Argparser = argparse.ArgumentParser()
    Argparser.add_argument('--candidate', type=str, help='Reference File')


    args = Argparser.parse_args()
    return args

args = argparser()

f = open(args.candidate, 'r').readlines()


with  open('corrected_candidate.txt', 'w') as out:
    for i in f:
        i=re.sub(r'[Yy]our winter jerky child?.', 'your child with winter vomiting disease ', i)
        i=re.sub(r'[Gg]et fluid?.', 'become dehydrated ', i)
        i=re.sub(r'[Gg]ets fluid?.', 'becomes dehydrated ', i)
        i=re.sub(r'[Cc]ervical mucosa?.', 'mucous membranes of the cervix ', i)
        i=re.sub(r'[Tt]rust board?.', 'support comitte ', i)
        i=re.sub(r'[Bb]lood glucose meters?.', 'insulin ', i)
        i=re.sub(r'[Bb]ile stones?.', 'gallstones ', i)
        i=re.sub(r'[Rr]eturn visit(s)?.', 'follow-up visit(s) ', i)
        i=re.sub(r'[Cc]ellurar tests?.', 'cervical screening ', i)
        i=re.sub(r'[Ff]everish cramps?.', 'febrile seizure ', i)
        i=re.sub(r'[Ee]ar in the ear?.', 'earache ', i)
        i=re.sub(r'[Ee]ar pain?.', 'earache ', i)
        i=re.sub(r'[Tt]hroat fleas?.', 'sore throat ', i)
        i=re.sub(r'[Xx]-ray nurse?.', 'radiology nurse ', i)
        i=re.sub(r'[Tt]hroat fluids?.', 'bacteria found in the throat ', i)
        i=re.sub(r'Discrimination Ombudsman?.', 'Equality Ombudsman ', i)
        i=re.sub(r'[Mm]ammography survey?.', 'mammography examination ', i)
        i=re.sub(r'[Τt]reatment with cytostatics?.', 'chemotherapy ', i)
        i=re.sub(r'[Aa]ntipyretics drugs?.', 'temperature-reducing medicine ', i)
        i=re.sub(r'[Dd]rugs?.', 'medicines? ', i)
        i=re.sub(r'[Dd]rug?.', 'medicine ', i)
        i=re.sub(r'[Τt]est answer?.', 'test result ', i)
        i=re.sub(r'[Ss]et up?.', 'control ', i)
        i=re.sub(r'[Hh]igh-cost protection?.', 'high-cost ceiling system ', i)
        i=re.sub(r'IVO?.', 'The Swedish National Board of Health and Welfare ', i)
        i=re.sub(r'[Cc]onsumables?.', 'disposable items ', i)
        i=re.sub(r'[Ss]ecretion?.', 'discharge ', i)
        i=re.sub(r'[Ιi]llness?.', 'disease ', i)
        i=re.sub(r'[Pp]ad?.', 'ball ', i)
        i=re.sub(r'[Gg]reasy?.', 'cotton wool ', i)
        i=re.sub(r'[Gg]et sinusitis?.', 'develop sinusitis ', i)
        i=re.sub(r'[Gg]ets sinusitis?.', 'develops sinusitis ', i)
        i=re.sub(r'[Bb]aby?.', 'child ', i)
        i=re.sub(r'[Rr]isky?.', 'hazardous ', i)
        i=re.sub(r'[Rr]eception?.', 'clinic', i)
        i=re.sub(r'[Aa]nalgesic?.', 'pain-killing ', i)
        i=re.sub(r'[Ss]ampling?.', 'specimen ', i)
        i=re.sub(r'[Ss]tudies?.', 'tests ', i)
        i=re.sub(r'[Ff]ever?.', 'temperature ', i)
        i=re.sub(r'[Rr][Rr]oom?.', 'clinic ', i)
        i=re.sub(r'[Cc]ervical mucus?.', 'mucus membrane of the cervix ', i)
        i=re.sub(r'[Ss]hut down from?.', 'suspended ', i)
        i=re.sub(r'[Ss]oft paper?.', 'soft tissue ', i)
        i=re.sub(r'[Ee]ar injuries  in?.', 'earache caused by ', i)
        i=re.sub(r'[Ee]ar infection?.', 'ear inflammation ', i)
        i=re.sub(r'[Oo]stomy items?.',  'stoma care products ', i)
        i=re.sub(r'[Gg]et dropped?.', 'are connected to the drip ', i)
        i=re.sub(r'[Gg]ets dropped?.', 'is connected to the drip ', i)
        i=re.sub(r'[Ll]eave cell samples?.' ,'get a cervical smear ',i)
        i=re.sub(r'[Hh]as been in the?.' ,'has discharge from the ',i)
        i=re.sub(r'[Nn]ewborn babies?.' ,'newborn infants ',i)
        i=re.sub(r'[Tt]raffic crimes?.' ,'traffic offenses ',i)
        i=re.sub(r'[Ss]ample?.' ,'specimen ',i)
        i=re.sub(r'[Oo]ccupational groups?.' ,'professionals ',i)
        i=re.sub(r'[Aa]re cold?.' ,'have a cold ',i)
        i=re.sub(r'[Ll]ocal hospitals and local hospitals?.' ,'local and neighborhood hospitals ',i) 
        i=re.sub(r'[Cc]onnected to the dentists?.' ,'affiliated with Privattandläkarna ',i)

        i=re.sub('\d+\,\d+', '{}', i).format(*map(lambda x:'{}'.format('SEK'+ ' '+ str(x)), re.findall('\d+\,\d+', i))) #adds SEK before numbers larger than 4 digits.
        
        if re.search(r'(\bchild\b)|(children\b)',i.lower()): #adds the word 'old' in the correct context.
            i=re.sub('\byear\b',r' year old',i)
            i=re.sub('\bmonth\b',r' month old',i)
        out.write(i)





