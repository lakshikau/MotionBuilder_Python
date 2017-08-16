#
# Script description:
# Finds skeliton and attach and parent a cylinder to each one of them on the skeliton 
# Used when motion human mocap data needs to e renderd withouth attaching a charcter
# MadeBy: Lakshika Udakandage 
#
###########################
from pyfbsdk import *
from math import *

def SelectBranch(topModel,CyGr):
    
    print '%s <%s>' % (topModel.LongName, topModel.__class__.__name__)
    for childModel in topModel.Children:
        if topModel.__class__.__name__ == "FBModelSkeleton":
		
            #make a cylinder for the selected skeliton node
            Cy1 = FBCreateObject('Browsing/Templates/Elements/Primitives', 'Cylinder', 'Cylinder')
            Cy1.Show = True
            Cy1.GeometricTranslation=FBVector3d( 0, 10, 0 )
            #get and assgn the location
            GT = FBVector3d()
            topModel.GetVector(GT, FBModelTransformationType.kModelTranslation, True)   
            Cy1.Translation= GT
            #make the parent contrint
            par = FBCreateObject( 'Browsing/Templates/Constraints', 'Parent/Child', 'SkCyPar' )
            #Append aim to the Scene
            scene = FBSystem().Scene
            scene.Constraints.append( par )
            #add objects to the "constrined object" and "source"
            setConstraintReferenceByName( par, Cy1, 'Constrained object (Child)' )
            setConstraintReferenceByName( par, topModel, 'Source (Parent)' )
            par.Active = True
			
            #make the aim constrint
            aim = FBCreateObject( 'Browsing/Templates/Constraints', 'Aim', 'SkCyAim' )
            #Append aim to the Scene
            scene.Constraints.append( aim )
            #add objects to the "constrined object" and "aim at"
            setConstraintReferenceByName( aim, Cy1, 'Constrained Object' )
            setConstraintReferenceByName( aim, childModel, 'Aim At Object' )
            #set the constrint vector
            aimVec = FBVector3d( 0, 1, 0 )
            AimVecProp = aim.PropertyList.Find ( 'Aim Vector' )
            AimVecProp.Data = aimVec
            #set the aim constrint active      
            aim.Active = True
			
            #get the location values
            ParLoc = FBVector3d()
            ChiLoc = FBVector3d()
            topModel.GetVector(ParLoc, FBModelTransformationType.kModelTranslation, True)
            childModel.GetVector(ChiLoc, FBModelTransformationType.kModelTranslation, True)
            #calculate the distance
            distance = sqrt( pow((ParLoc[0]-ChiLoc[0]),2) + pow((ParLoc[1]-ChiLoc[1]),2) + pow((ParLoc[2]-ChiLoc[2]),2))
            #set the scale of the object
            distance = distance/20 #theis is a scaling factor in Y axis to match the size
            ###############################
            CyScl = FBVector3d(0.1,distance,0.1)
            ###################################
            Cy1.Scaling = CyScl 
            #add to the grp
            Cy1.Parent=CyGr
			
        #call for the nest level skeliton node
        SelectBranch(childModel,CyGr)

    

def setConstraintReferenceByName( constraint, model, referenceName ):
    for i in range( 0, constraint.ReferenceGroupGetCount() ):
        if constraint.ReferenceGroupGetName( i ) == referenceName:
            constraint.ReferenceAdd( i, model )
            
def main():
    CyGrp = FBCreateObject('Browsing/Templates/Elements', 'Null', 'CySkGrp')
    for model in FBSystem().Scene.RootModel.Children:
        print '%s <%s>' % (model.LongName, model.__class__.__name__)
        assert model.Parent == None # Top-level models have no Parent
        SelectBranch(model,CyGrp)
        
    
if __name__ in ('__main__', '__builtin__'):
    main()