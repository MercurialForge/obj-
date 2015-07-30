import maya.cmds as cmds
import maya.mel as mel

# Make a new window
windowID = 'obj++'

# Close if copy is open
if cmds.window(windowID, exists = True):
    cmds.deleteUI(windowID)

# Make window
window = cmds.window( windowID, title=windowID, widthHeight=(200, 75) )
cmds.columnLayout( adjustableColumn=True )
cmds.text('obj++ Exporter Importer')
cmds.button( label='Export', command=('Export()') )
cmds.button( label='Import', command=('Import()') )
progressControl = cmds.progressBar(width=200)
cmds.setParent( '..' )
cmds.showWindow( window )
	
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Run the Export of SKL and WGT

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def Export():
	# Open file for writing
	path = Dialog("export")
	openFile = open(path, 'w')
	
	root = cmds.ls(selection=True)
		
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
	        	bones.index( cmds.listRelatives( [bones[x]], parent=True )[0] ),
	        	cmds.joint( bones[x], q=1, r=1, p=1 )[0],
	        	cmds.joint( bones[x], q=1, r=1, p=1  )[1],
	        	cmds.joint( bones[x], q=1, r=1, p=1  )[2],
	        	cmds.joint( bones[x], q=1, o=1  )[0],
	        	cmds.joint( bones[x], q=1, o=1  )[1],
	        	cmds.joint( bones[x], q=1, o=1  )[2],
	        	cmds.joint( bones[x], q=1, roo=1  ),
	        	)
	    else:
	        WriteSKL(
	        	outputFile, 
	        	bones[x], 
	        	-1, 
	        	cmds.joint( bones[x], q=1, r=1, p=1 )[0],
	        	cmds.joint( bones[x], q=1, r=1, p=1  )[1],
	        	cmds.joint( bones[x], q=1, r=1, p=1  )[2],
	        	cmds.joint( bones[x], q=1, o=1  )[0],
	        	cmds.joint( bones[x], q=1, o=1  )[1],
	        	cmds.joint( bones[x], q=1, o=1  )[2],
	        	cmds.joint( bones[x], q=1, roo=1  ),
	        	)
	return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Writes SKL data to the file

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def WriteSKL (outputFile, boneName, parentIndex, x, y, z, rotx, roty, rotz, orientation):				
    outputFile.write('bn {0} {1} {2} {3} {4} {5} {6} {7} {8}\n'.format(boneName, parentIndex, x, y, z, rotx, roty, rotz, orientation))	
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
	
	# List skinCuster relatives to the root joint
	boneRelatives =( cmds.listConnections( bones[0], type='skinCluster'))
	
	# Get skinCluster
	sCluster = boneRelatives[0]
	
	# List shape relatives to skinCluster
	shapeRelatives = cmds.skinCluster( sCluster, q=1, g=1 )
	
	# Get owned effect shapes
	shape = shapeRelatives[0]
    
    # Get total verts
	cmds.select( shape )
	vertCount = cmds.polyEvaluate( v=True )
	
	for x in range(0, vertCount):
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
				
    outputFile.write('vw {0} {1}\n'.format(weightCount, boneWeights))	
    return

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Loads and constructs data from .skl

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def Import():
	# Get selected mesh, only the first one
	theMesh = cmds.ls( selection=True )[0]
	
	# Deselect everything
	cmds.select(clear=1)
	
	# Create list for bones
	theBones = []
	
	# Open path
	path = Dialog("import")
	skl = open(path,'r')
	
	# Start creating bones
	theLines = skl.readlines()
	skl.close()
	for line in theLines:
		if "bn" in line:
			# Get bn values
			bnValues = line.split()
			
			# Write current bone to list, going in hierarchical order so all parents are created before children
			theBones.append(bnValues[1])
			
			# Handle root bone then all children
			if (int(bnValues[2]) == -1):
				cmds.joint( n=bnValues[1], r=1, p=( bnValues[3], bnValues[4], bnValues[5] ), o=(bnValues[6], bnValues[7], bnValues[8]), roo=bnValues[9] )
			else:
				cmds.joint(theBones[int(bnValues[2])], n=bnValues[1], r=1, p=( bnValues[3], bnValues[4], bnValues[5] ), o=(bnValues[6], bnValues[7], bnValues[8]), roo=bnValues[9] )
		# Skip comments
		elif "#" in line:
			continue
		# Break after bn
		else:
			break

	# Create skin cluster for the selected mesh using the generated skeleton
	sCluster = cmds.skinCluster( theBones[0], theMesh, dr=4.5)[0]
	
	# Tracking vert
	vert = -1
	
	# Initialize progress bar
	cmds.select( theMesh )
	vertCount = cmds.polyEvaluate( v=True )
	cmds.progressBar( progressControl, edit=True, maxValue=vertCount )
	cmds.select(clear=1)
	
	# Assign vertex weights
	for line in theLines:
		if cmds.progressBar(progressControl, query=True, isCancelled=True ) :
		    break
		    
		if "vw" in line:
			# Forward vert count
			vert += 1
			
			# Get vw values
			vwValues = line.split()
			
			# Assign joint, influence to vert
			for x in range(0, int(vwValues[1])):
				joint = vwValues[x * 2 + 2]
				influence = float(vwValues[x * 2 + 3])
				cmds.skinPercent( str(sCluster), theMesh + '.vtx' + '[' + str(vert) + ']', transformValue=( joint, influence ))
				
			cmds.progressBar(progressControl, edit=True, step=1)
	
	return
