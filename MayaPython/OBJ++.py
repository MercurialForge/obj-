import maya.cmds as cmds
import maya.mel as mel

# Make a new window
windowID = 'obj++'

# Close if copy is open
if cmds.window(windowID, exists = True):
    cmds.deleteUI(windowID)

# Make window
window = cmds.window( windowID, title=windowID, widthHeight=(200, 55) )
cmds.columnLayout( adjustableColumn=True )
cmds.text('obj++ Exporter Importer')
cmds.button( label='Export', command=('Export()') )
cmds.button( label='Import', command=('Import()') )
cmds.setParent( '..' )
cmds.showWindow( window )
	
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Run the Export of SKL and WGT

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def Export():
	# Open file for writing
	path = Dialog("export")
	openFile = open(path, 'w')
	
	root = cmds.ls()
		
	openFile.write('# skeleton output' + '\n')
	ExportSKL(openFile, root)
	print ('SKL section written successfully')
	
	openFile.write('\n')
	openFile.write('# weight output' + '\n')
	ExportWGT(openFile, root)
	print ('WGT section written successfully')
	openFile.close()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Opens dialog menu

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def Dialog(mode):
	singleFilter = "SKL Files (*.skl)"
	
	if mode == "export":
	    path = cmds.fileDialog2(ff=singleFilter, fm=0, okc = "OK")[0].rpartition(".")[0]
	    
	if mode == "import":
	    path = cmds.fileDialog2(ff=singleFilter, fm=1, okc = "OK")[0].rpartition(".")[0]
	    
	return path + ".skl"

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Exports the .skl

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Command run for exporting the SKL
def ExportSKL(outputFile, rootJoint):
    
    # Select the bone hierarchy
	cmds.select( rootJoint, hi=True )
	bones = cmds.ls( type='joint', sl=True )
    
	# Get bone count
	count = len(bones)
	
	# Iterate through bones writing each and it's parent
	for x in range(0, count):
	    if (x != 0):
	        WriteSKL(
	        	outputFile, 
	        	bones[x],
	        	str( bones.index( cmds.listRelatives( [bones[x]], parent=True )[0] ) ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[0] ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[1] ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[2] )
	        	)
	    else:
	        WriteSKL(
	        	outputFile, 
	        	bones[x], 
	        	str(-1), 
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[0] ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[1] ),
	        	str( cmds.xform( bones[x], q=1, ws=1, t=1 )[2] )
	        	)
	return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Writes SKL data to the file

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def WriteSKL (outputFile, boneName, parentIndex, x, y, z):				
    outputFile.write('bn' + ' ' + boneName + ' ' + parentIndex + ' ' + x + ' ' + y + ' ' + z + '\n')	
    return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Processes WGT export data

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #   
def ExportWGT(outputFile, rootJoint):
    # Select the bone hierarchy
	cmds.select( rootJoint, hi=True )
	bones = cmds.ls( type='joint', sl=True )

	# Get bone count
	count = len(bones)
	
	#############################################################
	# List skinCuster relatives to the root joint
	boneRelatives = []
	for i in range(0, count):
		boneRelatives =( cmds.listConnections( bones[i], type='skinCluster'))
		if boneRelatives is None: 
		    break
	#############################################################
	
	# Get skinCluster
	sCluster = boneRelatives[0]
	
	# List shape relatives to skinCluster
	shapeRelatives = cmds.listConnections( sCluster, type='shape' )
	
	# Get owned effect shapes
	shape = shapeRelatives[0]
    
    # Get total verts
	cmds.select( shape )
	vertCount = cmds.polyEvaluate( v=True )
	
	for x in range(0, vertCount):
		#WriteWGT(outputFile, )

	    # Get Bones
		skinBones = []
		tempBones = cmds.skinPercent(sCluster, shape + '.vtx' + '[' + str(x) + ']', ignoreBelow=0.01, query=True, transform=None)
		skinBonesCount = len(tempBones)
		for i in range(0, skinBonesCount):
		    skinBones.append( tempBones[i] )
		 
		
		# Get Weights
		skinWeights  = cmds.skinPercent(sCluster, shape + '.vtx' + '[' + str(x) + ']', ignoreBelow=0.01, query=True, value=True )
		
		WriteWGT(outputFile, skinBonesCount, skinBones, skinWeights)
	
	return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Writes WGT data to the file

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def WriteWGT (outputFile, weightCount, bones, weights):
    boneWeights = ""
    for i in range(0, int(weightCount)):
        boneWeights += bones[i] + ' ' + str(weights[i]) + ' '
				
    outputFile.write('vw' + ' ' + str(weightCount) + ' ' + boneWeights + '\n')	
    return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Loads and constructs data from .skl

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def Import():
    theBones = []
    path = Dialog("import")
    skl = open(path,'r')
    for line in skl.readlines():
        if "bn" in line:
        	words = line.split()
        	theBones.append(words[1])
        	if (int(words[2]) == -1):
        	    cmds.joint(p=( words[3], words[4], words[5] ), n=words[1] )
        	else:
        	    cmds.joint(theBones[int(words[2])], p=( words[3], words[4], words[5] ), n=words[1] )
	        
    skl.close()
    return
