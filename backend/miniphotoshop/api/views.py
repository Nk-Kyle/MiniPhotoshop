from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import io
from PIL import Image
import numpy as np
import re


def convertToMatrix(request):
    body = json.loads(request.body)
    base64image = body['pict']
    base64image = re.sub("^data:image\/\w+;base64,", "",base64image)
    base64_decoded = base64.b64decode(base64image)
    image = Image.open(io.BytesIO(base64_decoded))
    formatImage = Image.open(io.BytesIO(base64_decoded)).format
    image_np = np.array(image)
    return image_np, formatImage


    
# Create your views here.
@csrf_exempt
def rotateRight(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if len(matrix.shape) == 3:
            result = np.empty([matrix.shape[1],matrix.shape[0],matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[1],matrix.shape[0]],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        for i in range(r):
            for j in range(c):
                result[j, r-i-1] = matrix[i,j]
        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def rotateLeft(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if len(matrix.shape) == 3:
            result = np.empty([matrix.shape[1],matrix.shape[0],matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[1],matrix.shape[0]],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        for i in range(c):
            for j in range(r-1,-1,-1):
                result[c-i-1, j] = matrix[j,i]
        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def horizontalFlip(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if (len(matrix.shape) == 3):
            result = np.empty([matrix.shape[0],matrix.shape[1],matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[0],matrix.shape[1]],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        for i in range(r):
            for j in range(c//2):
                result[i,j] = matrix[i, c-1-j]
                result[i, c-1-j] = matrix[i,j]

        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def verticalFlip(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if (len(matrix.shape) == 3):
            result = np.empty([matrix.shape[0],matrix.shape[1],matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[0],matrix.shape[1]],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        for i in range(r):
            for j in range(c):
                result[i,j] = matrix[r-1-i, j]
                result[r-1-i, j] = matrix[i,j]

        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def zoomIn(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if (len(matrix.shape) == 3):
            result = np.empty([matrix.shape[0]*2,matrix.shape[1]*2,matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[0]*2,matrix.shape[1]*2],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        m = 0
        n = 0
        for i in range(r):
            for j in range(c):
                result[m,n] = matrix[i,j]
                result[m,n+1] = matrix[i,j]
                result[m+1,n] = matrix[i,j]
                result[m+1,n+1] = matrix[i,j]
                n += 2
            m += 2
            n = 0

        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def zoomOut(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if (len(matrix.shape) == 3):
            result = np.empty([matrix.shape[0]//2,matrix.shape[1]//2,matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[0]//2,matrix.shape[1]//2],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        m = 0
        n = 0
        if (len(matrix.shape) == 3):
            for i in range(r//2):
                for j in range(c//2):
                    for k in range(3):
                        result[i,j,k] = (int(matrix[m,n,k]) + int(matrix[m,n+1,k]) + int(matrix[m+1,n,k]) + int(matrix[m+1,n+1,k]))//4
                    n += 2
                m += 2
                n = 0
        else:
            for i in range(r//2):
                for j in range(c//2):
                    result[i,j] = (int(matrix[m,n]) + int(matrix[m,n+1]) + int(matrix[m+1,n]) + int(matrix[m+1,n+1]))//4
                    n += 2
                m += 2
                n = 0

        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def grayScale(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if (len(matrix.shape) == 3):
            result = np.empty([matrix.shape[0],matrix.shape[1]],dtype=np.uint8)
            r = matrix.shape[0]
            c = matrix.shape[1]
            for i in range(r):
                for j in range(c):
                    result[i,j] = (int(matrix[i,j,0]) * 0.229 + int(matrix[i,j,1]) * 0.587 + int(matrix[i,j,2]) * 0.114)

        else:
            result = matrix

        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def negative(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        result = 255 - matrix
        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def complement(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        result = ~matrix
        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def brighten(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if len(matrix.shape) == 3:
            result = np.empty([matrix.shape[0],matrix.shape[1],matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[0],matrix.shape[1]],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        if len(matrix.shape) == 3:
            for i in range(r):
                for j in range(c):
                    for k in range(3):
                        result[i,j,k] = min(int(matrix[i,j,k]) + 25, 255)
        else:
            for i in range(r):
                for j in range(c):
                    result[i,j] = min(int(matrix[i,j]) + 25, 255)
        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def contrast(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if len(matrix.shape) == 3:
            result = np.empty([matrix.shape[0],matrix.shape[1],matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[0],matrix.shape[1]],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        if len(matrix.shape) == 3:
            cval = [np.percentile(matrix[:,:,k],(1,99)) for k in range(3)]
            for i in range(r):
                for j in range(c):
                    for k in range(3):
                        val = int((matrix[i,j,k] - cval[k][0])/(cval[k][1] - cval[k][0]) * 255)
                        if val < 0:
                            val = 0
                        elif val > 255:
                            val = 255
                        result[i,j,k] = val
        else:
            cval = [np.percentile(matrix,(1,99))]
            for i in range(r):
                for j in range(c):
                    val = int((matrix[i,j] - cval[0][0])/(cval[0][1] - cval[0][0]) * 255)
                    if val < 0:
                        val = 0
                    elif val > 255:
                        val = 255
                    result[i,j] = val
        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def log(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if len(matrix.shape) == 3:
            result = np.empty([matrix.shape[0],matrix.shape[1],matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[0],matrix.shape[1]],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        if len(matrix.shape) == 3:
            for i in range(r):
                for j in range(c):
                    for k in range(3):
                        result[i,j,k] = max(0, min(255,int(np.log(matrix[i,j,k] + 1) * 50)))
        else:
            for i in range(r):
                for j in range(c):
                    result[i,j] = max(0, min(255,int(np.log(matrix[i,j] + 1) * 50)))
        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})

@csrf_exempt
def exp(request):
    if request.method == 'POST':
        matrix, formatImage = convertToMatrix(request)
        if len(matrix.shape) == 3:
            result = np.empty([matrix.shape[0],matrix.shape[1],matrix.shape[2]],dtype=np.uint8)
        else:
            result = np.empty([matrix.shape[0],matrix.shape[1]],dtype=np.uint8)
        r = matrix.shape[0]
        c = matrix.shape[1]
        if len(matrix.shape) == 3:
            for i in range(r):
                for j in range(c):
                    for k in range(3):
                        result[i,j,k] = max(0, min(255,int(matrix[i,j,k] ** 0.8)))
        else:
            for i in range(r):
                for j in range(c):
                    result[i,j] = max(0, min(255,int(matrix[i,j] ** 0.8)))
        image = Image.fromarray(result)
        buffered = io.BytesIO()
        image.save(buffered, format=formatImage)
        encoded = base64.b64encode(buffered.getvalue())
    return JsonResponse({'res':"data:image/"+formatImage+";base64,"+encoded.decode('utf-8')})


