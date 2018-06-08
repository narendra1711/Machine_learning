import os
import flask
from flask import Flask,render_template,request
app = Flask(__name__, static_url_path = "/images", static_folder = "images")

@app.after_request
def add_header(request):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    request.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    request.headers["Pragma"] = "no-cache"
    request.headers["Expires"] = "0"
    request.headers['Cache-Control'] = 'public, max-age=0'
    return request

APP_ROOT = os.path.dirname(os.path.realpath('__file__'))
'''@app.route('/', methods=['GET', 'POST'])
def upload_file():
    target = os.path.join(APP_ROOT, 'UploadsFolder/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print("file")
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return render_template('PdfUploadSuccess.html')'''

'''@app.route('/upload')
def upload_filee():
    return render_template('Upload_FS.html')

@app.route('/')
def upload_fileee():
    return render_template('Upload_FS1.html')'''

@app.route('/', methods=['GET', 'POST'])
def upload_fileew():
    target = os.path.join(APP_ROOT, 'UploadsFolder/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print("file")
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
    return render_template('KeywordUploadSuccess.html')

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/Search', methods=['GET', 'POST'])
def SearchKey():
    request.method == 'POST'
    string = request.form['nm']

    # Import Libraries
    import pandas as pd
    import numpy as np
    import cv2

    # ------------------------------------------------------------------------------------------
    # Input=Output of Vision API
    inputFileName = "input_boundaries.txt"
    # keysFileName="keys.txt"
    horiFileName = r"C:\Users\narendra_mugada\PycharmProjects\Invoice\UploadsFolder\Horizontal_Keys.txt"
    vertiFileName = r"C:\Users\narendra_mugada\PycharmProjects\Invoice\UploadsFolder\Vertical_Keys.txt"
    imagePath = "input.png"
    #string = "Ordering address"

    # ------------------------------------------------------------------------------------------
    # Function to read an input file and create word infos(Output of Vision API)
    def readInputFile(inputFileName):
        word_infos = []
        dict = {}
        f = open(inputFileName, 'r')

        for line in f:
            dict = {"boundingBox": line.strip().split('\'')[3],
                    "text": line.strip().split('\'')[7]}
            word_infos.append(dict)
        return word_infos

    word_infos = readInputFile(inputFileName)

    # ------------------------------------------------------------------------------------------
    # Function to create word_infos DataFrame
    def create_word_infosDataframe(word_infos):
        df = pd.DataFrame(word_infos)
        df = df.join(pd.DataFrame(df['boundingBox'].str.split(',').tolist(), columns=['x1', 'y1', 'x2', 'y2']))
        del df['boundingBox']
        df.x1 = df.x1.astype(np.int64)
        df.y1 = df.y1.astype(np.int64)
        df.x2 = df.x2.astype(np.int64)
        df.y2 = df.y2.astype(np.int64)
        return df

    # ------------------------------------------------------------------------------------------
    df = create_word_infosDataframe(word_infos)

    # ------------------------------------------------------------------------------------------
    # List of key words should be in List of Lists format(This varies from invoice-invoice)
    def readKeywords(horiFileName, vertiFileName):
        horiFile = open(horiFileName, 'r')
        vertiFile = open(vertiFileName, 'r')
        sub_keys = []

        for line in horiFile:
            string = line.split()
            sub_keys.append(string)

        for line in vertiFile:
            string = line.split()
            sub_keys.append(string)

        return sub_keys

    keys = []
    keys = readKeywords(horiFileName, vertiFileName)

    # keys=[["Please","deliver","to:"],['Purchase','Order'],['Ordering','address'],['Date'],['Vendor','address'],['Your','Vendor','No.','with','us:'],['Delivery','Date:'],['Contact','Person'],['PO','Number'],['Our','VAT','Registration','No.'],['Terms','of','Payment'],['Item'],['Material'],['Description'],['Order','quantity'],['Total','net','item','value'],['Telephone'],['Fax'],['Currency'],['Total','weight'],['Total','volume'],['Head','Office'],['Invoice','Address'],['Ordering','Office'],['Unit'],['Net','price'],['Net','value'],['Unit']]
    # keys=[['Item'],['Material'],['Description'],['Order','quantity'],['Total','net','item','value']]
    # keys=[["Please","deliver","to:"],['Purchase','Order'],['Ordering','address'],['Date'],['Vendor','address'],['Your','Vendor','No.','with','us:'],['Delivery','Date:'],['Contact','Person'],['PO','Number'],['Our','VAT','Registration','No.'],['Terms','of','Payment'],['Telephone'],['Fax'],['Currency']]
    # ------------------------------------------------------------------------------------------
    keys_bound = keys.copy()

    # ------------------------------------------------------------------------------------------
    # This function generates boundaries of gives keywords the same keys format
    def genKeyBoundaries(df, keys):
        for i in range(0, len(keys)):
            for j in range(0, len(keys[i])):
                for k in range(0, len(df)):
                    if (keys[i][j] == df.text[k]):
                        if (len(keys[i]) != 1):
                            if (j != 0):
                                if (keys[i][j - 1]['text'] == df.text[k - 1]):
                                    keys_bound[i][j] = {"text": df.text[k],
                                                        "value": [df.x1[k], df.y1[k], df.x2[k], df.y2[k]]}
                                else:
                                    continue
                            elif (j == 0):
                                if (keys[i][j + 1] == df.text[k + 1]):
                                    keys_bound[i][j] = {"text": df.text[k],
                                                        "value": [df.x1[k], df.y1[k], df.x2[k], df.y2[k]]}
                                else:
                                    continue
                            keys_bound[i][j] = {"text": df.text[k], "value": [df.x1[k], df.y1[k], df.x2[k], df.y2[k]]}
                        else:
                            keys_bound[i][j] = {"text": df.text[k], "value": [df.x1[k], df.y1[k], df.x2[k], df.y2[k]]}
        return keys_bound

    keys_bound = genKeyBoundaries(df, keys)

    # ------------------------------------------------------------------------------------------
    # Creating Keys Dataframe
    def create_keysDataframe(keys_bound):
        ind_keys = []
        for i in range(0, len(keys_bound)):
            for j in range(0, len(keys_bound[i])):
                ind_keys.append({'text': keys_bound[i][j]['text'], 'x1': keys_bound[i][j]['value'][0],
                                 'y1': keys_bound[i][j]['value'][1], 'x2': keys_bound[i][j]['value'][2],
                                 'y2': keys_bound[i][j]['value'][3]})
        df_keys = pd.DataFrame(ind_keys)
        columnsTitles = ['text', 'x1', 'y1', 'x2', 'y2']
        df_keys = df_keys.reindex(columns=columnsTitles)
        return df_keys

    df_keys = create_keysDataframe(keys_bound)

    # ------------------------------------------------------------------------------------------
    # Grouping key in a list
    def groupKeyWords(keys_bound):
        final = []
        dummy = {}
        a = ''
        for i in range(0, len(keys_bound)):
            a = ''
            x1 = keys_bound[i][0]['value'][0]
            y1 = keys_bound[i][0]['value'][1]
            x2 = keys_bound[i][0]['value'][2]
            y2 = keys_bound[i][0]['value'][3]
            for j in range(0, len(keys_bound[i])):
                x2_temp = keys_bound[i][len(keys_bound[i]) - 1]['value'][2]
                a = ' '.join([a, keys_bound[i][j]['text']])
                x1 = min(x1, keys_bound[i][j]['value'][0])
                y1 = min(y1, keys_bound[i][j]['value'][1])
                x2 = max(x1, keys_bound[i][j]['value'][0]) + x2_temp - min(x1, keys_bound[i][j]['value'][0])
                y2 = max(y2, keys_bound[i][j]['value'][3])

            dummy = {"text": a, "x1": x1, "y1": y1, "x2": x2, "y2": y2}
            final.append(dummy)
        return final

    final = groupKeyWords(keys_bound)

    # ------------------------------------------------------------------------------------------
    # Convert final grouped list to a dataframe
    def createGroupedDataframe(final):
        df_final = pd.DataFrame(final)
        columnsTitles1 = ['text', 'x1', 'y1', 'x2', 'y2']
        df_final = df_final.reindex(columns=columnsTitles1)
        return df_final

    df_final = createGroupedDataframe(final)

    # ------------------------------------------------------------------------------------------
    # This function appends df and df_keys, resets index and convert to a df_total dataframe
    def append_resetIndex(df, df_keys):
        frames = [df, df_keys]
        s1 = pd.concat(frames)
        df_subtotal = s1.drop_duplicates(keep=False)
        total = [df_subtotal, df_final]
        df_total = pd.concat(total)
        df_total = df_total.reset_index(drop=True)
        df_subtotal = df_subtotal.reset_index(drop=True)
        return df_total, df_subtotal

    df_total, df_subtotal = append_resetIndex(df, df_keys)

    # ------------------------------------------------------------------------------------------
    # This function extracts vertical data between two keywords
    def extractVerticalData(prev, nxt):
        extract = []
        extractedData = []
        a = b = 0
        for i in range(0, len(df)):
            txt = ""

            if (df['x1'][i] == prev['x1'] and df['y1'][i] == prev['y1']):
                a = len(prev.text.split(' ')) - 2
                a = a + i
                print("a", a)
                # extract.append({'text':txt+df_total['text'][i],"Boundaries":[df_total['x1'][i],df_total['y1'][i],df_total['x2'][i],df_total['y2'][i]]})
            if (df['x1'][i] == nxt['x1'] and df['y1'][i] == nxt['y1']):
                b = i
                print("b", b)
        for i in range(a + 1, b):
            extract.append(
                {'text': txt + df['text'][i], "Boundaries": [df['x1'][i], df['y1'][i], df['x2'][i], df['y2'][i]]})
        extractedData.append({"text": prev['text'], "data": extract})
        x1 = extractedData[0]['data'][0]['Boundaries'][0]
        y1 = extractedData[0]['data'][0]['Boundaries'][1]
        x2 = y2 = x3 = y3 = 0
        x2_temp = extractedData[0]['data'][0]['Boundaries'][2]
        y2_temp = extractedData[0]['data'][0]['Boundaries'][3]
        for j in range(0, len(extractedData[0]['data'])):
            x1 = min(x1, extractedData[0]['data'][j]['Boundaries'][0])
            y1 = min(y1, extractedData[0]['data'][j]['Boundaries'][1])
            if (x3 < extractedData[0]['data'][j]['Boundaries'][0]):
                x2_temp = extractedData[0]['data'][j]['Boundaries'][2]
            x3 = max(x3, extractedData[0]['data'][j]['Boundaries'][0])
            x2 = x3 + x2_temp
            print(x2_temp)
            if (y3 < extractedData[0]['data'][j]['Boundaries'][1]):
                y2_temp = extractedData[0]['data'][j]['Boundaries'][3]
            y3 = max(y3, extractedData[0]['data'][j]['Boundaries'][1])
            y2 = y3 + y2_temp
        x2 = x2 - x1
        y2 = y2 - y1
        return (extractedData, x1, y1, x2, y2)

    # ------------------------------------------------------------------------------------------
    # This function extracts horizaontal data between two keywords
    extract = []
    extractedData = []

    def extractHorizontalData(current):
        for i in range(0, len(df_total)):
            if ((abs(df_total['y1'][i] - current['y1']) <= 4) and
                    (abs(df_total['y2'][i] - current['y2']) <= 4) and
                    current['x1'] <= df_total['x1'][i] and
                    current['text'] != df_total['text'][i]):
                x1 = df_total.x1[i]
                y1 = df_total.y1[i]
                x2 = df_total.x2[i]
                y2 = df_total.y2[i]
                text = current['text']
                extractedData.append({"text": current['text'],
                                      "data": [{"text": df_total['text'][i],
                                                "Boundaries": [df_total.x1[i],
                                                               df_total.y1[i],
                                                               df_total.x2[i],
                                                               df_total.y2[i]]
                                                }]})

        return (text, x1, y1, x2, y2)

    # ------------------------------------------------------------------------------------------
    # This function checks whether the key word should be sent to extractHorizontalData or extractVerticalData
    def checkHorizontalVertical(string, horiFileName, vertiFileName):
        horiFile = open(horiFileName, 'r')
        vertiFile = open(vertiFileName, 'r')
        sub_keys = []

        for line in horiFile:
            if string in line:

                for i in range(0, len(df_final)):
                    if (string == df_final.text[i].strip()):
                        index = i
                print(index)

                text, x1, y1, x2, y2 = extractHorizontalData(df_final.iloc[index])
                print(text, x1, y1, x2, y2)

                image_path = imagePath
                image = cv2.imread(image_path)

                def drawRectangleKey(text, x1, y1, x2, y2):
                    cv2.rectangle(image, (x1, y1), (x1 + x2, y1 + y2), (0, 0, 255), 1)
                    return

                drawRectangleKey("text", df_final.x1[index], df_final.y1[index], df_final.x2[index], df_final.y2[index])

                def drawRectangleValue(text, x1, y1, x2, y2):
                    cv2.rectangle(image, (x1, y1), (x1 + x2, y1 + y2), (0, 100, 0), 1)
                    return

                drawRectangleValue("text", x1, y1, x2, y2)

                #cv2.imshow('Detected', image)
                cv2.imwrite(r'C:\Users\narendra_mugada\PycharmProjects\Invoice\images\Rectangled.png', image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
            else:
                print("hello")
        for line in vertiFile:
            if string in line:
                j = 0
                index = 0

                for i in range(0, len(df_final)):
                    if (string == df_final.text[i].strip()):
                        index = i
                    if (index == 1):
                        j = 5
                    elif (index == 5):
                        j = 6
                print(index, j)
                text, x1, y1, x2, y2 = extractVerticalData(df_final.iloc[index], df_final.iloc[j])
                # print(text,x1,y1,x2,y2)
                # extractedData,x1,y1,x2,y2=extractVerticalData(df_final.iloc[2],df_final.iloc[3])
                # print(extractedData)
                image_path = imagePath
                image = cv2.imread(image_path)

                def drawRectangleKey(text, x1, y1, x2, y2):
                    cv2.rectangle(image, (x1, y1), (x1 + x2, y1 + y2), (0, 0, 255), 1)
                    return

                drawRectangleKey('text', df_final.x1[index], df_final.y1[index], df_final.x2[index], df_final.y2[index])

                def drawRectangleValue(text, x1, y1, x2, y2):
                    cv2.rectangle(image, (x1, y1), (x1 + x2, y1 + y2), (0, 100, 0), 1)
                    return

                drawRectangleValue('text', x1, y1, x2, y2)

                #cv2.imshow('Detected', image)
                cv2.imwrite(r'C:\Users\narendra_mugada\PycharmProjects\Invoice\images\Rectangled.png', image)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
        return sub_keys

    df_final = df_final.reset_index(drop=True)
    df_total = df_total.sort_values('x1')
    df_total = df_total.reset_index(drop=True)
    df_final = df_final.sort_values('y1')
    df_final = df_final.reset_index(drop=True)
    df_total = df_total.sort_values('y1')
    df_total = df_total.reset_index(drop=True)

    checkHorizontalVertical(string, horiFileName, vertiFileName)

    # ------------------------------------------------------------------------------------------
    # This function extratcs tabular data
    dummy = []
    boundary = df_final.iloc[1]

    def extractTabularData(prev, nxt):
        for i in range(0, len(df_total)):
            if (prev['x1'] <= (df_total.x1[i] + 2) and
                    nxt['x1'] - 2 > df_total.x1[i] and
                    boundary['y1'] > df_total.y1[i] and
                    prev['y1'] < df_total.y1[i]):
                dummy.append(df_total.text[i])
        return dummy

    extractTabularData(df_final.iloc[0], df_final.iloc[1])

    # ------------------------------------------------------------------------------------------

    return render_template('Display.html')


if __name__ == '__main__':
    app.run()
