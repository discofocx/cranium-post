''' copy skinweights from a to b '''
''' Bjorn Blaabjerg 2016-02-08 '''
''' blaabjergB.com '''
import maya.cmds as cmds

def copySkin():
    objects=cmds.ls(sl=True)
    findSkinCluster=cmds.listHistory(objects[0],pdo=1,il=2)
    oldSkincluster=cmds.ls(findSkinCluster,typ='skinCluster')
    
    shapeHistory=cmds.listHistory(objects[1],il=2)

    oldSkc=cmds.ls(shapeHistory,typ='skinCluster') # test if there is a skincluster on new geo already
    if oldSkc:
        cmds.delete(oldSkc)
        print 'deleted existing skincluster on '+objects[1]

    jnt=cmds.skinCluster(oldSkincluster,weightedInfluence=True,q=True)
    newSkc=cmds.skinCluster(jnt,objects[1])[0]
    cmds.copySkinWeights( ss=oldSkincluster[0], ds=newSkc, nm=True,surfaceAssociation='closestPoint')
    cmds.rename(newSkc,oldSkincluster[0])
        
copySkin()