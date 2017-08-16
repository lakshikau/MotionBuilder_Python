#
# Script description:
# Finds if the Joint of a given name is there and attach a 3d camera to it
# Used to attach and parent a motion builder 3D Camera to mocap data stream
# MadeBy: Lakshika Udakandage 
#
###########################
# After running the script, adjust the place and rotation
###########################

from pyfbsdk import *

# constants
SEARCH_MODELS_ONLY = False
BY_SHORT_NAME = True

#function def for the fining and attaching cam
def FindJointObject(pattern, byShortName):
    cl = FBComponentList()    
    if byShortName:
        # First param is a pattern
        # second param is a boolean saying if the search must be made in LongName (including namespace)
        # third param is a boolean. If True: we search for models only, if False, we search for all objects
        # including textures, materials, etc...
        FBFindObjectsByName( pattern, cl, False, SEARCH_MODELS_ONLY )
    else:
        # This function search objects by including their namespace part (called LabelName, or LongName)
        FBFindObjectsByName( pattern, cl, True, SEARCH_MODELS_ONLY )
        
   # if there is a joint with the name 
   # then create a 3D cam and parent it to the joint 
    if len(cl) < 1:
        FBMessageBox( "Oculus Stereo Camera Error", "Please check the search joint name", "OK" )
        
    if len(cl) > 1:
        FBMessageBox( "Oculus Stereo Camera Error", "More than one object with the same name", "OK" ) 
          
    if len(cl) == 1:
        #create the 3d Cam
        OculusCam = FBCameraStereo('NewOculusCam')
        OculusCam.Show = True
        OculusCam.LookAtProperty = None
        
        for o in cl:
            ParentJoint=o
        
        #parent and translate to the joint location    
        JointLoc = FBVector3d()
        ParentJoint.GetVector(JointLoc, FBModelTransformationType.kModelTranslation, True)   
        OculusCam.Translation= JointLoc
        JointRot = FBVector3d(0,0,0)
        OculusCam.Rotation= JointRot
        OculusCam.Parent=ParentJoint
    
# function call for to find objects with the name
# replace "Occulus2016_root" with the proper joint name
########################################
FindJointObject( "Occulus2016_root", BY_SHORT_NAME )
############################################
