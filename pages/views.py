from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm,Registrationform
from django.contrib.auth import authenticate, login
import os
from .models import PersonalInfo,User
from django.urls import path, include

import face_recognition
import cv2 

def facedect(loc):
        cam = cv2.VideoCapture(0)   
        s, img = cam.read()
        if s:   
                
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                MEDIA_ROOT =os.path.join(BASE_DIR,'pages')

                loc=(str(MEDIA_ROOT)+loc)
                face_1_image = face_recognition.load_image_file(loc)
                face_1_face_encoding = face_recognition.face_encodings(face_1_image)[0]

                #

                small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                check=face_recognition.compare_faces(face_1_face_encoding, face_encodings)
                

                print(check)
                if check[0]:
                        return True

                else :
                        return False    

def about(request):
    return render(request,"about.html",{})

def base(request):
        if request.method =="POST":
                form =LoginForm(request.POST)
                if form.is_valid():
                        username=request.POST['email']
                        password=request.POST['password']
                        user = authenticate(request,username=username,password=password)
                        if user is not None:
                                if facedect(user.userprofile.head_shot.url):
                                        login(request,user)
                                return redirect('dashboard')
                                
                        else:
                                return redirect('index') #!Not sure whats this for       
        else:
                MyLoginForm = LoginForm()
                return render(request,"base.html",{"MyLoginForm": MyLoginForm})  

def home(request):
   return render(request, 'home.html', {})

#from django.contrib.auth.forms import UserCreationForm



def index(request):#!task:populate index page with the thing that you want.
    return render(request,"index.html",{})
def dashboard(request):#!task:populate index page with the thing that you want.
    return render(request,"personal_info.html",{})

def register(request):
        if request.method =="POST":
                form =Registrationform(request.POST)
                if form.is_valid():
                        form.save()
                        username=form.cleaned_data['username']
                        password=form.cleaned_data['password1']
                        user = authenticate(username=username,password=password)
                        login(request,user)
                        return redirect('index')
                else:
                        return redirect('index')        

        form =Registrationform()
        return render(request,'registration/register.html',{'form':form})        

def profile(request):
        return render(request,'profile.html',{})


def common(request):
        return render(request,'common.html',{})
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
def get_doc(request):
        if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save("current/doc.jpg", myfile)
                return redirect("get_face")
                #!1.getting the doc as image in variable
                #!2.passing that document in one function as param and return the cropped face only 
                #!3.now that we have particular user face and cropped face,we will compare them both 
                #! using opencv compare function and boom result will be True or False and we will show 
                #! message accordingly that user verified or not.


def get_face(request):
 # generate frame by frame from camera
    camera = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        success, frame1 = camera.read(0)  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame1)
        #     frame = buffer.tobytes()
            cv2.imwrite("pages/media/current/image.jpg", frame1)
            camera.release() 
            cv2.destroyAllWindows()
            break
    return redirect("compare_faces")

import face_recognition
def face_extract():
        doc = cv2.imread("pages/media/current/doc.jpg")
        gray = cv2.cvtColor(doc, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt2.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
                cv2.rectangle(doc, (x, y), (x+w, y+h), (0, 0, 255), 2)
                faces = doc[y:y + h, x:x + w]
                # cv2.imshow("face",faces)
                cv2.imwrite('pages/media/current/face.jpg', faces)
                break
def face_extract1():
        doc = cv2.imread("pages/media/current/image.jpg")
        gray = cv2.cvtColor(doc, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_alt2.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
                cv2.rectangle(doc, (x, y), (x+w, y+h), (0, 0, 255), 2)
                faces = doc[y:y + h, x:x + w]
                # cv2.imshow("face",faces)
                cv2.imwrite('pages/media/current/face1.jpg', faces)
                break
import os,shutil

def compare_faces(request):
        face_extract()
        face_extract1()

        known_image = face_recognition.load_image_file("pages/media/current/doc.jpg")
        unknown_image = face_recognition.load_image_file("pages/media/current/image.jpg")

        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces([biden_encoding], unknown_encoding,tolerance=0.5)
        # delete_in_folder_images()
        return HttpResponse(results)

def delete_in_folder_images():
        folder = 'pages/media/current'
        for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                         os.unlink(file_path)
                        elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
        
def save_info(request):
        user_id = request.POST.get("userid")
        occupation = request.POST.get('dropdown')
        first_name = request.POST.get('firstname') 
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email') 
        address = request.POST.get('address') 
        acc_no = request.POST.get('acc_no')
        personal_info_object=PersonalInfo.objects.create(user=User.objects.get(pk=user_id),firstname=first_name,lastname= last_name,
        phonenumber= phone,
        email= email,
        occupation= occupation,
        address = address,
        document_status = "unverified",
        account_number = acc_no)
        if personal_info_object:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save("current/doc.jpg", myfile)
                camera = cv2.VideoCapture(0)
                while True:
                        # Capture frame-by-frame
                        success, frame1 = camera.read(0)  # read the camera frame
                        if not success:
                                break
                        else:
                                ret, buffer = cv2.imencode('.jpg', frame1)
                                #     frame = buffer.tobytes()
                                cv2.imwrite("pages/media/current/image.jpg", frame1)
                                camera.release() 
                                cv2.destroyAllWindows()
                                break
                face_extract()
                face_extract1()

                known_image = face_recognition.load_image_file("pages/media/current/doc.jpg")
                unknown_image = face_recognition.load_image_file("pages/media/current/image.jpg")

                biden_encoding = face_recognition.face_encodings(known_image)[0]
                unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

                results = face_recognition.compare_faces([biden_encoding], unknown_encoding,tolerance=0.5)
                print(results)
                if results==True:
                        user_prof_obj=PersonalInfo.objects.filter(user=user_id,account_number=acc_no)    
                        
                        for object in user_prof_obj:
                                object.document_status="verified"
                                object.save()
                else:
                        user_prof_obj=PersonalInfo.objects.filter(user=user_id,account_number=acc_no)    
                        
                        for object in user_prof_obj:
                                object.document_status="unverified"
                                object.save()
                return redirect("accounts_list_user")

def accounts_list_user(request):
        user_id=request.user.id
        data=PersonalInfo.objects.filter(user=user_id)
        context = {
            "accounts": data,
        }
        return render(request,'user_accounts.html',context) 