import CYKParse
import Tree
import requests
import json
import re
import string
from geotext import GeoText
from nltk.corpus import words
import datetime
from datetime import datetime
import calendar
import unicodedata
from DateTime import Timezones
from geopy.geocoders import Nominatim
setofwords = set(words.words())
requestInfo = {
        'name': '',
        'time': '',
        'location': ''
}
haveGreeted = False
other_info= False
altword= []
new = []
today= 0
tomorrow = 0
compare = False
final= {}
# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    # print('t',T,'\n T.items()', T.items())
    sentenceTrees = { k: v for k,v in T.items() if k.startswith('S/0') }
    # print('sentenceTrees',sentenceTrees)
    completeSentenceTree = max(sentenceTrees.keys())
    # print('getSentenceParse', completeSentenceTree)
    return T[completeSentenceTree]
# def getSentenceParse(T):
#     print('t',T,'\n T.items()', T.items())
#     sentenceTrees = { k: v for k,v in T.items() }
#     print('sentenceTrees',sentenceTrees)
#     for i in sentenceTrees:
#         completeSentenceTree = (sentenceTrees.keys())
#     print('getSentenceParse', completeSentenceTree)
#     return T[completeSentenceTree]


# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestInfo
    lookingForLocation = False
    lookingForName = False
    for leaf in Tr.getLeaves():
        # print(leaf)
        if leaf[0] == 'Adverb':
            requestInfo['time'] = leaf[1]
        if lookingForLocation and leaf[0] == 'Name':
            requestInfo['location'] = leaf[1]
        if leaf[0] == 'Preposition' and leaf[1] == 'in':
            lookingForLocation = True
        else:
            lookingForLocation = False
        if leaf[0] == 'Noun' and leaf[1] == 'name':
            lookingForName = True
        if lookingForName and leaf[0] == 'Name':
            requestInfo['name'] = leaf[1]
def upRequestInfo(Tr):
    global requestInfo
    lookingForLocation = False
    lookingForName = False
    for leaf in Tr.getLeaves():
        # print(leaf)

        if leaf[0] == 'Name':
            requestInfo['location'] = leaf[1]


# This function contains the data known by our simple chatbot
def getTemperature(location, time):
    if time == 'now':
        return realTemperature(location)
    elif time == 'tomorrow':
        return forecast(location)
    else:
        return 'unknown'


# Format a reply to the user, based on what the user wrote.
def reply(): # reply function
    global requestInfo
    global haveGreeted
    if not haveGreeted and requestInfo['name'] != '':
        print("Hello", requestInfo['name'] + '.')
        haveGreeted = True
        return
    time = 'now' # the default
    if requestInfo['time'] != '':
        time = requestInfo['time']
    salutation = ''
    if requestInfo['name'] != '':
        salutation = requestInfo['name'] + ', '
    print(salutation + 'the temperature in ' + requestInfo['location'] + ' ' +
        time + ' is ' + getTemperature(requestInfo['location'], time) + '.')
    time = 'forecast' # the default
    if requestInfo['time'] != '':
        time = requestInfo['time']
    salutation = ''
    if requestInfo['name'] != '':
        salutation = requestInfo['name'] + ', '
    print(salutation + 'the temperature in ' + requestInfo['location'] + ' ' +
        time + ' is ' + getTemperature(requestInfo['location'], time) + '.')

def realTemperature(location): # current temp API

    # api_key='7a36b3a18b9cf39e7974709360a00f83'
    # URL = "https://api.openweathermap.org/data/2.5/weather?" + "q=" +str(location) + "&appid=" + api_key
    # response = requests.get(URL)
    # jdata = requests.get(URL).json()
    api_key = '7a36b3a18b9cf39e7974709360a00f83'
    api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key
    api_call += '&q=' + location
    jdata = requests.get(api_call).json()
    URL = "https://api.openweathermap.org/data/2.5/weather?" + "q=" + str(location) + "&appid=" + api_key
    response = requests.get(URL)
    location_data = {'city': jdata['city']['name'],'country': jdata['city']['country'] }
    print('chatbot','city:',location_data['city'], ' country: ',location_data['country'])
    if len(jdata['list']) > 0 and response.status_code == 200:
        data = response.json()#get data
        main = data['main']# get the main
        temperature = main['temp']# get the temperature
        humidity = main['humidity']#humidity
        pressure = main['pressure']#pressure
        report = data['weather']
        print('chatbot: the ',location, 'temperature is ', temperature - 273.15, 'celsius ', (temperature- 273.15)* 9/5+ 32, 'fahrenheit')
        print('*************************')
        print('chatbot: do you want more detailed information')
        user_detail_input = input('Y/N:')
        if user_detail_input.lower() in ['y', 'Yes', 'yes', 'ok','OK', 'fine','sure']:
            print('*************************')
            print('chatbot: the humidity is ',humidity)
            print('chatbot: the pressure is ',pressure)
            print('chatbot: the weather is ', report[0]['description'])
        else:
            print('ok, great')
        print('chatbot: Do you mane some useful cloth suggestions?')
        user_s_input = input('Y/N:')
        if user_s_input.lower() in ['y', 'Yes', 'yes', 'ok','OK', 'fine','sure']:
            print('*************************')
            celsius =temperature - 273.15
            return clothrecommendation(celsius)
        else:
            print('ok, great')

def forecast(location): # forecast API
    api_key = '7a36b3a18b9cf39e7974709360a00f83'
    api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key
    api_call += '&q=' + location
    jdata = requests.get(api_call).json()
    response = requests.get(api_call)

    location_data = {
            'city': jdata['city']['name'],'country': jdata['city']['country']
        }
    print('chatbot: ', 'the city is:',location_data['city'], ' and the country is: ',location_data['country'])
    if response.status_code == 200:
        item =  jdata['list'][3]
        temperature = item['main']['temp']
        report = item['weather'][0]['description']
        humidity = item['main']['humidity']#humidity
        pressure = item['main']['pressure']#pressure
        print('chatbot: the ', location, 'temperature is ', temperature - 273.15, 'celsius ',(temperature - 273.15) * 9 / 5 + 32, 'fahrenheit')
        print('*************************')
        print('chatbot: do you want to know more detailed information?')
        u_input = input('Y/N:')
        if u_input.lower() in ['y', 'Yes', 'yes', 'ok','OK', 'fine','sure']:
            print('*************************')
            print('chatbot: the weather is', report)
            print('chatbot: the humidity is ',humidity)
            print('chatbot: the pressure is ',pressure)
        else:
            print('ok, great')
        # if u_input.lower() in ['n', 'no', 'nope', 'nah', 'noo', 'nope']:
        #     print('chatbot: ok, great')
        print('chatbot: Do you mane some useful cloth suggestions?')
        user_s_input = input('Y/N:')
        if user_s_input.lower() in ['y', 'Yes', 'yes', 'ok','OK', 'fine','sure']:
            print('*************************')
            celsius = temperature - 273.15
            return clothrecommendation(celsius)
        else:
            print('ok, great')
        # if user_s_input.lower() in ['n', 'no', 'nope', 'nah', 'noo', 'nope']:
        #     print('chatbot: ok, great')
        # else:
        #     print('ok, great')

def clothrecommendation(celsius): # the cgat expertise on suggesting the best cloth to wear based on the temperature.
    print('chatbot: I will recommend and give you a list of best cloth to wear based on The Travel Insider and the local tempreture')
    if celsius<=0:
        print('chatbot: the temperature is sooo low, take care of your self and double-layered and hooded down jackets is recommended')
        print('Outerwear: Double-layered hooded down jackets (Preferably waterproof)\nTops: Sweaters, Jumpers, Turtlenecks\nBottoms: Pants, Leggings (Preferably waterproof) Thermal underwear\nAccessories: Beanies, Ear Muffs, Scarves, Thick Socks (bring multiple pairs to layer, if need be), Heat pads (for extra warmth!)\nWaterproof winter boots')
        print('\n')
    if celsius>0 and celsius<10:
        print('chatbot: Temperature is low! I recommend you to wear puffer coat, wrap-style overcoat, or even a down jacket. A chunky snood or infinity scarf and a wooly beanie ')
        print('Outerwear: Padded or Puffer Coat, Overcoats (Trench Coats, Fur or Faux Fur Coats etc.), Down Jackets\nTops: Sweaters, Jumpers, Turtlenecks\nBottoms: Jeans, Trousers\nThermal Underwear: Long-sleeved thermal top, Thermal leggings (at least one of each to layer underneath your jeans or sweaters for extra warmth)\nAccessories: Beanies, Berets, Touchscreen-Friendly Gloves, Scarves, SocksBoots')
        print('\n')
    if celsius>15:
        print('chatbot: the temperature is suitable and I recommend you to wear thin clothes')
        print('Lighter weaves of wool are suited for hot weather. Heavy fabrics tend to cling to your skin and trap sweat – adding\n a layer of heat between the fabric and your body. Instead of wearing heavier versions of cotton – such as twill, which is what your jeans are made of – opt for poplin, seersucker and madras cotton.')
        print('\n')
    if celsius>=10 and celsius<=15:
        print('chatbot: chill temperature and I recommend you to have minimal outerwear like a parka, biker jacket or leather jacket')
        print('Tops (for Layering): Shirts, Hoodies, Dresses\nLightweight Outerwear: Leather jackets, Biker jackets, Parkas, Pea Coat\nBottoms: Jeans, Trousers, Skirts Shoes: Sneakers, Boots\nAccessories: A light scarf *optional')
        print('\n')

def compare(location): #function commpare the temperature
    api_key = '7a36b3a18b9cf39e7974709360a00f83'
    api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key
    api_call += '&q=' + location
    response = requests.get(api_call)
    jdata = requests.get(api_call).json()
    if  response.status_code == 200:
        for item in jdata['list']:
            temperature = item['main']['temp']
            final['tomorrow'] =  temperature - 273.15

    URL = "https://api.openweathermap.org/data/2.5/weather?" + "q=" +str(location) + "&appid=" + api_key
    response = requests.get(URL)
    if  response.status_code == 200:
        data = response.json()#get data
        main = data['main']# get the main
        temperature = main['temp']# get the temperature
        final['today'] = temperature - 273.15
    print(final)
    return final
def history(location, year,month, day):
    geolocator = Nominatim(user_agent="Your_Name")
    l = geolocator.geocode(location)
    print('chatbot:' , l.address)
    ll = [l.latitude, l.longitude]
    latitude = ll[0]
    longitude = ll[1]
    date = datetime(year, month, day, 0, 0).timestamp()
    print(date)
    # date = datetime.datetime(year, month, day, 0, 0).strftime('%s')
    time = str(int(date))
    api_key = "7a36b3a18b9cf39e7974709360a00f83"
    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=%s&lon=%s&dt=%s&appid=%s" % (latitude, longitude, time, api_key)
    response = requests.get(url)
    data = json.loads(response.text)
    temp = data["current"]['temp']
    pressure = data["current"]['pressure']
    humidity = data["current"]['humidity']
    uvi = data["current"]['uvi']
    print('chatbot: the ', location, 'temperature is ', temp - 273.15, 'celsius ',(temp - 273.15) * 9 / 5 + 32, 'fahrenheit')
    print('*************************')
    print('chatbot: do you want to know more detailed information?')
    u_input = input('Y/N:')
    if u_input.lower() in ['y', 'Yes', 'yes', 'ok', 'OK', 'fine', 'sure']:
        print('*************************')
        print('chatbot: the uvi is', uvi)
        print('chatbot: the humidity is ', humidity)
        print('chatbot: the pressure is ', pressure)
    else:
        print('ok, great')

def flat(l): # function flat the list
    for i in l:
        if type(i) == list:
            flat(i)
        else:
            new.append(i)
    return new
# A simple hard-coded proof of concept.

def main(countinue=None):
    global requestInfo
    global unit
    greetingsummary = ['hi','hello', 'halo', 'sup','hii','nice to meet you','what\'s up']
    finalgreeting= ['by','bye', 'goodbye', 'thank you', 'see you']
    w = ['what\'s', 'how\'s']
    place = []
    name =''
    n = True
    while True:
        print('\n')
        try:
            thenum = ''
            date = []
            aaaa = False
            check = False
            listwords = []
            user_in = input("input(type the question here): ")# user input
            # thenum  = [int(x) for x in user_in.split() if s.isdigit()]
            # print(thenum)
            #tokenize the word
            for i in user_in:
                if f"'{i}'" != ascii(i):  # O(1)
                    user_in = user_in.replace(i, ' ')  # replace invalid with empty space
            split_string = user_in.rstrip().split()  #
            for word in split_string:
                # this method specify the characters to eliminate insipred from link https://stackoverflow.com/questions/1059559
                word = word.strip(string.punctuation)  # tokenize word and get rid of punctuation
                if word != '':  # O(1)
                    listwords.append(word)
            for i in listwords:
                if i not in setofwords:
                    date.append(i)
                    aaaa= True
            user_input = ' '.join([str(elem) for elem in listwords])
            # a = unicodedata.normalize('NFKD',user_in).encode('ascii','ignore')## nomarlize the input
            # user_input = a.decode(encoding="ascii", errors="ignore")
            places = GeoText(user_input)
            place = places.cities
            # print('place',place)
            output = list(user_input.split(' '))
            # print(output)
            if user_in.lower() == 'current date' or ('current' in output and 'date' in output) :
                d = datetime.now().day
                m = datetime.now().month
                y = datetime.now().year
                print('Chatbot: let me tell you current date and time:')
                print('Chatbot: ',str(m) + '/' + str(d) + '/' + str(y))
                print('Chatbot: let me know if you need more help')
                continue
            if 'calendar' in output:
                d = datetime.now().day
                m = datetime.now().month
                y = datetime.now().year

                print(str(m) + '/' + str(d) + '/' + str(y))
                print(calendar.month(int(y), int(m)))
                continue
            else:
                if 'I' in user_input and 'am' in user_input or ('My' in user_input and 'name' in user_input):## get and remeber the name of user
                    name = output[-1]
                    print('chatbot: hello', name, ', how can I help you?')
                    n = False
                if user_input in finalgreeting :## hanlde the input if user want to quit

                    if name !='': # if input has no name
                        print('chatbot:',user_input,',', name, 'Thank you for using the weather chatbot, have a good day!')
                        break
                    else:
                        print('chatbot: Thank you for using the weather chatbot, have a good day!') #break the program
                        break
                if user_input in greetingsummary:
                    print('chatbot: ', user_input, ', I\'m chatbot and how can I help you')
                    continue
                if (len(place) == 0 and output[0] not in greetingsummary ):
                    if n is True:
                        print('sorry, could you please say in another way. It seems missing some important information for me to understand')
                        n = True

                for i in output:# invalid sentence handling
                    if not i.isascii(): # check if valid
                        print('chatbot: sorry, I don\'t understand this, could you please say in another way? ')

                if user_input not in finalgreeting: # function to compare the temperature
                    if output[0].lower() == 'will':
                        location = ' '.join([str(i) for i in place])
                        compare(location)
                        if 'tomorrow' in output and 'today' in output :
                            a = output.index('tomorrow')
                            b = output.index('today')
                            if 'hotter' in output:
                                if a<b:
                                    if final['tomorrow']>final['today']:
                                        final.clear()
                                        print('chatbot: Yes, it is')
                                    else:
                                        final.clear()
                                        print('chatbot: No, it\'s not')
                            if 'cooler' in output or 'cool' in 'output':
                                if a>b:
                                    if final['tomorrow']>final['today']:
                                        final.clear()
                                        print('chatbot: No, it\'s not')
                                    else:
                                        final.clear()
                                        print('chatbot: Yes, it is')

                    if 'what\'s' in output: # handle the input with abbrivation
                        print(1111)
                        l = [['what', 'is'] if i == 'what\'s' else i for i in output]
                        flat(l)
                        T, P = CYKParse.CYKParse(new, CYKParse.getGrammarWeather())
                        sentenceTree = getSentenceParse(T)
                        upRequestInfo(sentenceTree)
                        reply()
                        for i in new:
                            if not i.isalpha() and i.isascii():
                                print('sorry, I don\'t undersatnd what you asking, could you say it in another way?')
                        new.clear()
                    # if 'how\'s' in output:
                    #     print(1)
                    #     l = [['how', 'is'] if i == 'how\'s' else i for i in output]
                    #     flat(l)
                    #     T, P = CYKParse.CYKParse(new, CYKParse.getGrammarWeather())
                    #     sentenceTree = getSentenceParse(T)
                    #     upRequestInfo(sentenceTree)
                    #     reply()
                    #     for i in new:
                    #         if not i.isalpha() and i.isascii():
                    #             print('sorry, I don\'t undersatnd what you asking, could you say it in another way?')
                    #     new.clear()

                    if output[0].lower() in ['what','how'] and output[-1].lower() in ['now', 'yesterday', 'tomorrow'] :
                        T, P = CYKParse.CYKParse(output, CYKParse.getGrammarWeather())
                        sentenceTree = getSentenceParse(T)
                        updateRequestInfo(sentenceTree)
                        reply()
                    # if 'tomorrow' not in user_input and 'yesterday' not in user_input and 'forecast' not in user_input:
                    #     if len(output)==2 and output[-1].lower()== 'temperature':
                    #         location = output[0]
                    #         realTemperature(location)
                    #     if len(output) == 3 and output[-1].lower() == 'temperature':
                    #         location = [' '.join(output[0 : 2])]
                    #         location = "".join(str(x) for x in location)
                    #         realTemperature(location)
                    if  bool(re.search(r'\d', user_in)) and output[0].lower() != 'will':# search with if there date in sentence
                        # print(date)
                        try:
                            try:
                                word = date[-1]
                                x = word.split('/')
                                year = x[2]
                                day= x[1]
                                month = x[0]
                                year = int(year)
                                day = int(day)
                                month = int(month)
                                location = ' '.join([str(i) for i in place])
                                # print(type(location),year,type(month),day)
                                history(location, year, month, day)
                                aaaa == False
                                date.clear()
                            except:
                                print('chatbot: sorry, I can only access past 5 days weather')
                        except:
                            try:
                                word = date[0]
                                x = word.split('/')
                                year = x[2]
                                day = x[1]
                                month = x[0]
                                year = int(year)
                                day = int(day)
                                month = int(month)
                                location = ' '.join([str(i) for i in place])
                                # print(type(location),year,type(month),day)
                                history(location, year, month, day)
                                aaaa == False
                                date.clear()
                            except:
                                print('chatbot: sorry, I can only access past 5 days weather')
                    if not  bool(re.search(r'\d', user_in)) and output[0].lower() != 'will':# search with if there no date in sentence
                        if 'forecast' in output or 'tomorrow' in output or 'next day' in output:
                            # T, P = CYKParse.CYKParse(output, CYKParse.getGrammarWeather())
                            # sentenceTree = getSentenceParse(T)
                            location = ' '.join([str(i) for i in place])
                            # print(location)
                            forecast(location)
                        # if 'now' in output or 'current' in output or 'today' in output :
                        #     # T, P = CYKParse.CYKParse(output, CYKParse.getGrammarWeather())
                        #     # sentenceTree = getSentenceParse(T)
                        #     location = ' '.join([str(i) for i in place])
                        #     realTemperature(location)
                        else:
                            location = ' '.join([str(i) for i in place])
                            realTemperature(location)


                        # T, P = CYKParse.CYKParse(output, CYKParse.getGrammarWeather())
                        # sentenceTree = getSentenceParse(T)
                        # upRequestInfo(sentenceTree)
                        # reply()
            # except:
            #     print('umm, I need more time to learn')
        except:
            pass
            # print('umm, I need more time to learn')






print('Welcome to use the weather chatbot program!')
print('     The help is on the way!')
main()

