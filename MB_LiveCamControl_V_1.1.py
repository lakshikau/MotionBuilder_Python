#
# Script description:
# setup the control GUI for the mocap virtual cam iPad interface
# Used to give touch control to the iPad vertual camera user with basic transprot and camera control
# MadeBy: Lakshika Udakandage 
#
###########################
from pyfbsdk import *
from pyfbsdk_additions import *

#create camera
iGuycamera = FBCamera( 'iGuyCam ' )
iGuycamera.Translation = FBVector3d( 0, 100, 0 )
iGuycamera.Rotation = FBVector3d( 0, 0, 0 )
iGuycamera.FocalLength=35
iGuycamera.Show = True
iGuycamera.ViewShowTimeCode = True

#create null object
iGuyNull = FBCreateObject( 'Browsing/Templates/Elements', 'Null', 'iGuyNullParent' )
iGuyNull.Name = 'iGuyNullParent'
iGuyNull.Translation = FBVector3d( 0, 100, 0 )
iGuyNull.Scaling = FBVector3d( 5, 5, 5 )
iGuyNull.Show = True

#make camera child of null object
iGuycamera.Parent = iGuyNull

#initialize transport control
lPlayer = FBPlayerControl()

#function for focus slider
def FocusChange(control,event):
    iGuycamera.FocalLength = 35 + (control.Value - 0.5)*20

#function for doly slider
def DolyControl(control,event):
    newXcoord=(control.Value-0.5)*30
    iGuycamera.Translation = FBVector3d(newXcoord, 0, 0 )
    
#function for Record button
def BtnRecCall(control, event):
    lPlayer.Record (False, True)
    #Record (bool pOverrideTake=False, bool pCopyData=True)
       
#function for stop button
def BtnStopCall(control, event):
    lPlayer.Stop()

#function for play button    
def BtnPlayCall(control, event):
    lPlayer.Play()
    
#function for Beginning button    
def BtnBegCall(control, event):
    lPlayer.GotoStart()
    
#initialize UI Dialogbox
def PopulateLayout(mainLyt):
    x = FBAddRegionParam(0,FBAttachType.kFBAttachLeft,"")
    y = FBAddRegionParam(0,FBAttachType.kFBAttachTop,"")
    w = FBAddRegionParam(0,FBAttachType.kFBAttachRight,"")
    h = FBAddRegionParam(25,FBAttachType.kFBAttachNone,"")
    mainLyt.AddRegion("main","main", x, y, w, h)
    lyt = FBHBoxLayout()
    mainLyt.SetControl("main",lyt)
    
#add focal legth slider lable
    l = FBLabel()
    l.Caption = "F"
    l.Style = FBTextStyle.kFBTextStyleBold
    lyt.Add(l, 8)
    
#add focus slider    
    FocusBar = FBSlider()    
    FocusBar.Orientation = FBOrientation.kFBHorizontal   
    FocusBar.SmallStep = 10
    FocusBar.LargeStep = 10 
    lyt.Add(FocusBar, 150, height=25) 
    FocusBar.OnChange.Add(FocusChange)  #call function for focus
    
#add doly slider lable
    l = FBLabel()
    l.Caption = "D"
    l.Style = FBTextStyle.kFBTextStyleBold
    lyt.Add(l, 8)
    
#add doly slider
    DolyBar = FBSlider()    
    DolyBar.Orientation = FBOrientation.kFBHorizontal   
    DolyBar.SmallStep = 10
    DolyBar.LargeStep = 10 
    lyt.Add(DolyBar, 150, height=25)
    DolyBar.OnChange.Add(DolyControl) #call function for doly
    
#add record button    
    BtRec = FBButton()
    BtRec.Caption = "Rec"
    BtRec.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(BtRec,60)
    BtRec.OnClick.Add(BtnRecCall) #call function for record
 
#add stop button    
    BtStop = FBButton()
    BtStop.Caption = "Stop"
    BtStop.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(BtStop,60)
    BtStop.OnClick.Add(BtnStopCall) #call function for stop

#add play button     
    BtPlay = FBButton()
    BtPlay.Caption = "Play"
    BtPlay.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(BtPlay,60)
    BtPlay.OnClick.Add(BtnPlayCall) #call function for play

#add beginning button     
    BtBeg = FBButton()
    BtBeg.Caption = "Beginning"
    BtBeg.Justify = FBTextJustify.kFBTextJustifyCenter
    lyt.Add(BtBeg,60)
    BtBeg.OnClick.Add(BtnBegCall) #call function for begnning
    
   
# function to create UI dialogbox    
def CreateTool():
    # Tool creation will serve as the hub for all other controls
    t = FBCreateUniqueTool("iGuy Live Control")
    t.StartSizeX = 610
    t.StartSizeY = 50
    PopulateLayout(t)
    ShowTool(t)
    
#call function for create dialogbox   
CreateTool()