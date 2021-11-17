#------------ Please Install all packages mentioned in 'requirements.txt' for execution of code -----------
# ---------------- Importing All necessary files from respective Libraries -------------------
import os 
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import threading
import pafy
from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio




#----------------- Defining Functions For performing different tasks ---------------------

#---- VideoUrl() FUnction to Fetch Video Url from User InterFace --- 
def VideoUrl():
    downloadingTotalSizeResult.configure(text='')
    downloadingRecieveSizeResult.configure(text='')
    downloadingTimeSizeResult.configure(text='')
    getdetail = threading.Thread(target=getVideo)
    getdetail.start()


#----------- getVideo() FUnction to Fetch Video details from video Url ------
def getVideo():
    listbox.delete(0, END)
    url = urlText.get()
    data = pafy.new(url)
    streams = data.allstreams
    index = 0
    for i in streams:
        rawSize = i.get_filesize()  # 'get_filesize()' returns data in byte
        # to get size in MB || 0.1f i.e format until 0.1 floating point
        filesize = '{:0.1f}'.format(rawSize//(1024*1024))
        listItem = str(index)+'.'.ljust(3, ' ')+str(i.quality).ljust(10, ' ')+str(
            i.extension).ljust(5, ' ') + str(i.mediatype)+' '+filesize.rjust(10, ' ')+'Mb'

        # Populate listbox
        listbox.insert(END, listItem)
        index = index+1


# ----------- SelectCursor() Function to select specific audio or video file to download via Index number ----------
def SelectCursor(event):
    global downloadIndex
    listboxdata = listbox.get(listbox.curselection())
    downloadStream = listboxdata[:3]
    downloadIndex = int(''.join(x for x in downloadStream if x.isdigit()))
    print(downloadIndex, '   ', listboxdata)



#----------- downloadAudioData() function to download audio file if audio format is selected --------
def downloadAudioData():
    global downloadIndex
    listbox.delete(0, END)
    url = urlText.get()
    data = pafy.new(url)
    print(data)
    streams = data.allstreams
    audio = data.getbestaudio()
    filedr = filedialog.askdirectory()
    downloadingBarLabel.configure(text='Downloading Progress')

    def mycallback(total, received, ratio, rate, estimatetime):
        global totalscale
        # print(total ,received,ratio,rate,estimatetime)
        # Setting value of Progress Bar
        totalscale = float('{:.5}'.format(total/(1024*1024)))
        downloadingProgressBar.configure(maximum=totalscale)
        downloadingProgressBar.configure(value=received/(1024*1024))

        # Arranging Other vlaues for lables
        rawtotalCount = float('{:0.5}'.format(total/(1024*1024)))
        rawreceivedCount = float('{:0.5}'.format(received/(1024*1024)))
        rawestimateTime = '{:0.2f}'.format(estimatetime)

        totalCount = f'{rawtotalCount} mb'
        receivedCount = f'{rawreceivedCount} mb'
        estimateTime = f'{rawestimateTime} sec'

        # Adding those values to lables
        downloadingTotalSizeResult.configure(text=totalCount)
        downloadingRecieveSizeResult.configure(text=receivedCount)
        downloadingTimeSizeResult.configure(text=estimateTime)

    streams[downloadIndex].download(
        filepath=filedr, quiet=True, callback=mycallback)
    downloadingBarLabel.configure(text='Downloaded Sucessfully')



#----------- downloadVideoData() function to download video file if video format is selected --------
def downloadVideoData():
    global downloadIndex
    listbox.delete(0, END)
    url = urlText.get()
    data = pafy.new(url)
    print(data)
    streams = data.allstreams
    audio = ''
    new_Audioname = ''
    audioIndex = 0
                      
    filedr = filedialog.askdirectory()
    downloadingBarLabel.configure(text='Downloading Progress')

    def mycallback(total, received, ratio, rate, estimatetime):
        global totalscale
        
        # Setting value of Progress Bar
        totalscale = float('{:.5}'.format(total/(1024*1024)))
        downloadingProgressBar.configure(maximum=totalscale)
        downloadingProgressBar.configure(value=received/(1024*1024))

        # Arranging Other vlaues for lables
        rawtotalCount = float('{:0.5}'.format(total/(1024*1024)))
        rawreceivedCount = float('{:0.5}'.format(received/(1024*1024)))
        rawestimateTime = '{:0.2f}'.format(estimatetime)

        totalCount = f'{rawtotalCount} mb'
        receivedCount = f'{rawreceivedCount} mb'
        estimateTime = f'{rawestimateTime} sec'

        # Adding those values to lables
        downloadingTotalSizeResult.configure(text=totalCount)
        downloadingRecieveSizeResult.configure(text=receivedCount)
        downloadingTimeSizeResult.configure(text=estimateTime)


    # -------- Downloading raw VIdeo(audio less) File---
    streams[downloadIndex].download(filepath=filedr, quiet=True, callback=mycallback)


    #--Updating downloading bar label-
    downloadingBarLabel.configure(text='Fetching audiofiles...')
    
    
    # -------- Downloading raw audio File seprately---
    for i in streams:
        if(i.extension) == 'm4a' and (i.mediatype) == 'audio':             
            streams[audioIndex].download(filepath=filedr, quiet=True, callback=mycallback)
            new_Audioname = str(data.title+'.'+i.extension) 
            print(streams[audioIndex])

        audioIndex = audioIndex + 1
           
           
           
    # --- COde to merge raw Video and Audio File and creating merged File ---
    downloadingBarLabel.configure(text='Converting.....')
    videoname = str(data.title+'.'+streams[downloadIndex].extension) 
    mergename = str(data.title+'YTD.'+streams[downloadIndex].extension)
    videofilepath = str(filedr+'/'+videoname)
    audiofilepath = str(filedr+'/'+new_Audioname)
    mergepath = str(filedr+'/'+mergename)
    print(videofilepath,'/',audiofilepath)
    
    # Got ffmepg tools from moviepy
    ffmpeg_merge_video_audio(videofilepath,
                            audiofilepath,
                            mergepath,
                            vcodec='copy',
                            acodec='copy',
                            ffmpeg_output=False,
                            logger=None)

    # ---- Removing/Deleting previously downoloded raw audio & video Files from directory
    os.remove(f'{filedr}/{videoname}')
    os.remove(f'{filedr}/{new_Audioname}')
    
    #--Updating downloading bar label-
    downloadingBarLabel.configure(text='Downloaded Sucessfully')    


# --------------- DownloadFile() function to download selected file -----------------
def DownloadFile():
    global downloadIndex
    listbox.delete(0, END)
    url = urlText.get()
    data = pafy.new(url)
    print(data)
    streams = data.allstreams
    
    #== If User Selects VideoFile 'downloadVideoData' function will be called else 'downloadAudioData' function will be called
    if streams[downloadIndex].mediatype == 'video':
        getdata = threading.Thread(target=downloadVideoData)
        getdata.start()
    else:
        getdata = threading.Thread(target=downloadAudioData)
        getdata.start()







# ------------------ GUI (Graphical User InterFace) CODE -------------------
root = Tk() #declaring root as Tk()
root.title('Youtube Downloader')
root.geometry('780x600')
root.configure(bg='white')
root.resizable(False, False)
downloadIndex = 0
totalscale = 0
#------------------- ScrollBar ----------------------#
yscrollbar = Scrollbar(root)
yscrollbar.place(x=477, y=210, height=196, width=20)


# ----------- URL Bar-------
urlText = StringVar()
UrlEntery = Entry(root, textvariable=urlText, font=('arial', 20, 'italic normal'), width=31,
                  bd=1, bg='black', fg='yellow', cursor='xterm white', insertbackground='yellow')
UrlEntery.place(x=20, y=150)

################## LABELS ###################

introlabel = Label(root, text='Welcome to Youtube Audio Video Downloader', width=36,
                   relief='ridge', bd=0, font=('Helvetica', 26, 'roman normal'), fg='black')
introlabel.place(x=15, y=20)

UrlLabel = Label(root, text='Enter URL below :', width=15, relief='ridge', bd=0, font=(
    'Helvetica', 15, 'roman normal'), fg='black', bg='white')
UrlLabel.place(x=20, y=120)

listbox = Listbox(root, yscrollcommand=yscrollbar.set, width=50, height=10, font=('arial', 12, 'italic bold'),
                  relief='solid', bd=2, highlightcolor='gray', highlightbackground='black', highlightthickness=2)
listbox.place(x=20, y=210)
# bind passess event by default
listbox.bind("<<ListboxSelect>>", SelectCursor) #---- calling SelectCursor Function for binding selected Video Format ------


# ---- Total Size ------
downloadingTotalSizeLabel = Label(
    root, text='Total Size :', font=('arial', 15, 'roman bold'), bg='white')
downloadingTotalSizeLabel.place(x=500, y=240)

downloadingTotalSizeResult = Label(
    root, text='', font=('arial', 15, 'roman bold'), bg='white')
downloadingTotalSizeResult.place(x=650, y=240)


# ---- RECEIVED Size ------
downloadingRecieveSizeLabel = Label(
    root, text='Received Size :', font=('arial', 15, 'roman bold'), bg='white')
downloadingRecieveSizeLabel.place(x=500, y=290)

downloadingRecieveSizeResult = Label(
    root, text='', font=('arial', 15, 'roman bold'), bg='white')
downloadingRecieveSizeResult.place(x=650, y=290)


# ---- TIME Size ------
downloadingTimeSizeLabel = Label(
    root, text='Time Left :', font=('arial', 15, 'roman bold'), bg='white')
downloadingTimeSizeLabel.place(x=500, y=340)

downloadingTimeSizeResult = Label(
    root, text='', font=('arial', 15, 'roman bold'), bg='white')
downloadingTimeSizeResult.place(x=650, y=340)

downloadingBarLabel = Label(root, text=' ', font=(
    'arial', 15, 'roman bold'), bg='white')
downloadingBarLabel.place(x=500, y=500)


# ------------------ PROGRESS BAR --------------------
downloadingProgressLabel = Label(root, text='', width=36, font=(
    'arial', 15, 'roman bold'), bg='white', fg='black', bd=0, relief='raised')
downloadingProgressLabel.place(x=20, y=500)

downloadingProgressBar = ttk.Progressbar(
    downloadingProgressLabel, orient=HORIZONTAL, value=0, length=100, maximum=totalscale)
downloadingProgressBar.grid(row=0, column=0, ipadx=185, ipady=3)


# ---------------- BUttons -----------------------
ClicBtn = Button(root, text='Search', font=('arial', 15, 'roman bold'), bd=0,
                 bg='gray', fg='black', activeforeground='white', width=12, command=VideoUrl) #-- calling VideoUrl Function for passing url from GUI to code -- 
ClicBtn.place(x=500, y=147)


DownloadBtn = Button(root, text='Download', font=('arial', 15, 'roman bold'),
                     bd=0, bg='black', fg='white', width=12, command=DownloadFile)# -- Calling DownloadFile function for Downloading file -----
DownloadBtn.place(x=180, y=420)

#-------looping Entire GUI ---
root.mainloop()
