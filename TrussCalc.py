import numpy as np
import math
import time

class joint:
    def __init__(self, node, paired):
        self.node = node
        self.paired = paired


class member:
    def __init__(self, pair, unit_vector, length):
        self.pair = pair
        self.unit_vector = unit_vector
        self.length = length
        

def nodeMap(p1, p2, nx, ny):

    nodes = []

    x_vals = np.linspace(p1[0], p2[0], nx)
    y_vals = np.linspace(p1[1], p2[1], ny)

    for y in y_vals:
        for x in x_vals:
            nodes.append([x , y])

    return np.array(nodes)

def main():
    
    joints = []
    members = []
    memberVectors = []
    
    origin = [0,0]
    farPoint = [100,(10*math.sqrt(3))]

    #x_nodes = int(input("x nodes: "))
    #y_nodes = int(input("Y nodes: "))

    x_nodes = 11
    y_nodes = 2

    nodes = nodeMap(origin, farPoint, x_nodes, y_nodes)
    print(nodes)

    jointNodes = []
    nodePair = []
    paired = []
 
    readFile = "5sectionWarren.txt"
    file = open(readFile, 'r')
    
    for line in file:
        line = line.strip('\n')
        if line == '/':
            break
        joints = line.split(" ")
        jointNode = int(joints[0])
        jointNodes.append(jointNode)
        print(jointNode)
    
        p = 0
    for line in file:
        line = line.strip('\n')
        node = line.split('-')
        if node[0] == '/':
            break
        node1 = int(node[0])
        node2 = int(node[1])
        nodePair.append([node1, node2])
        print (nodePair[p])
        p = p + 1

    file.close()
        
    for i in range(len(nodePair)):
        delta_x = nodes[nodePair[i][1]][0] - nodes[nodePair[i][0]][0]
        delta_y = nodes[nodePair[i][1]][1] - nodes[nodePair[i][0]][1]
        norm = math.sqrt(delta_x**2 + delta_y**2)
        x = abs(delta_x/norm)
        y = abs(delta_y/norm)
        members.append(member(nodePair[i],[x,y], norm))
            
    jointVectors = []
    for i in range(len(jointNodes)):
        jointVectors = []
        for n in range(len(members)):
            if jointNodes[i] == members[n].pair[0]:
                if nodes[jointNodes[i]][0] > nodes[members[n].pair[1]][0]:
                    jointVectors.append(-members[n].unit_vector[0])
                elif nodes[jointNodes[i]][0] < nodes[members[n].pair[1]][0]:
                    jointVectors.append(members[n].unit_vector[0])
                else:
                    jointVectors.append(0)
            elif jointNodes[i] == members[n].pair[1]:
                if nodes[jointNodes[i]][0] > nodes[members[n].pair[0]][0]:
                    jointVectors.append(-members[n].unit_vector[0])
                elif nodes[jointNodes[i]][0] < nodes[members[n].pair[0]][0]:
                    jointVectors.append(members[n].unit_vector[0])
                else:
                    jointVectors.append(0)
            else:
                jointVectors.append(0)
        if i == 0:
            jointVectors.append(1)
            jointVectors.append(0)
            jointVectors.append(0)
        else:
            jointVectors.append(0)
            jointVectors.append(0)
            jointVectors.append(0)
        memberVectors.append(jointVectors)
    
    for i in range(len(jointNodes)):
        jointVectors = []
        for n in range(len(members)):
            if jointNodes[i] == members[n].pair[0]:
                if nodes[jointNodes[i]][1] > nodes[members[n].pair[1]][1]:
                    jointVectors.append(-members[n].unit_vector[1])
                elif nodes[jointNodes[i]][1] < nodes[members[n].pair[1]][1]:
                    jointVectors.append(members[n].unit_vector[1])
                else:
                    jointVectors.append(0)
            elif jointNodes[i] == members[n].pair[1]:
                if nodes[jointNodes[i]][1] > nodes[members[n].pair[0]][1]:
                    jointVectors.append(-members[n].unit_vector[1])
                elif nodes[jointNodes[i]][1] < nodes[members[n].pair[0]][1]:
                    jointVectors.append(members[n].unit_vector[1])
                else:
                    jointVectors.append(0)
            else:
                jointVectors.append(0)
        if i == 0:
            jointVectors.append(0)
            jointVectors.append(1)
            jointVectors.append(0)
        elif i == 1:
            jointVectors.append(0)
            jointVectors.append(0)
            jointVectors.append(1)
        else:
            jointVectors.append(0)
            jointVectors.append(0)
            jointVectors.append(0)
        memberVectors.append(jointVectors)
    #print(memberVectors)
    print(nodes[6])
    
    loadPoints = []
    loadMatrix = []
    tempLoad = []
    while True:
        
        point = int(input("Node to load: "))
        if point == -1:
            break
        load = float(input("Load: "))
        if load == -1:
            break

        loadPoints.append([point, load])

    for i in range(len(jointNodes)):
        loadMatrix.append(0)
    
    #print(loadMatrix)
    
    for i in range(len(jointNodes)):
        loaded = False
        for n in range(len(loadPoints)):
            if jointNodes[i] == loadPoints[n][0]:
                toLoad = loadPoints[n][1]
                #print(jointNodes[i])
                #print(loadPoints[n][0])
                #print(toLoad)
                loadMatrix.append(toLoad)
                loaded = True
        if loaded == False: 
            loadMatrix.append(0)
        
    
    #print(loadMatrix)
    

    A = np.array(memberVectors)
    B = np.array(loadMatrix)
    print(A)

    X = np.linalg.solve(A,B)
    X = -X

    #print(X)
    print('\n')

    n = 0
    for i in range(len(X) - 3):
        print(members[n].pair, ':', X[i], '\n')
        n = n + 1

    total_length = 0
    for i in range(len(members)):
        total_length =  total_length + members[i].length
    
    total_length = total_length * (100 / nodes[jointNodes[1]][0])
    
    print('\n')

    max_Force = 0
    n = 0
    for i in X:
        if n == len(members):
            break
        abs_force = abs(i)
        if abs_force > max_Force:
            max_Force = abs_force
        n = n + 1
            
    max_Tensive = 0
    n = 0
    for i in X:
        if n == len(members):
            break
        if i > max_Tensive:
            max_Tensive = i
        n = n + 1
    
    n = 0
    max_Compressive = 0
    for i in X:
        if n == len(members):
            break
        if i < max_Compressive:
            max_Compressive = i
        n = n + 1
    max_Compressive = abs(max_Compressive)

    total_Force = 0
    for i in range(len(members)):
        total_Force = total_Force + abs(X[i])
        
    total_Compressive = 0
    n = 0
    m = 0
    r = 0
    for i in X:
        if r == len(members):
            break
        if i < 0:
            i = abs(i)
            total_Compressive = total_Compressive + i
            n = n + 1
        if abs(i) < .0000001 and i < 0:
            m = m + 1
        r = r + 1
    avg_Compressive = total_Compressive / (n - m)
    
    total_Tensive = 0
    n = 0
    m = 0
    r = 0
    for i in X:
        if r == len(members):
            break
        if i > 0:
            total_Tensive = total_Tensive + i
            n = n + 1
        if abs(i) < .0000001 and i > 0:
            m = m + 1
        r = r + 1
    avg_Tensive = total_Tensive / (n - m)

    maxHeight = 0
    for i in jointNodes:
        if nodes[i][1] > maxHeight:
            maxHeight = nodes[i][1]

    lowHeight = farPoint[1]
    for i in jointNodes:
        if nodes[i][1] < lowHeight:
            lowHeight = nodes[i][1]
    
    height = maxHeight - lowHeight
    span = nodes[jointNodes[1]][0]

    height_to_span = height / span
    
    loadString = ''
    for i in range(len(loadPoints)):
        loadString = loadString + str(loadPoints[i][0]) + ': ' + str(loadPoints[i][1]) + '\n'
        1
    total_Load = abs(sum(loadMatrix))
    print(total_Load)
    max_force_Ratio = total_Load / max_Force
    max_force_Opt = max_force_Ratio / total_length
    avg_Force = total_Force / len(members)
    ext_load_ratio = total_Load / avg_Force
    length_Opt = abs((ext_load_ratio / total_length))
    tensive_load_Ratio = total_Load / avg_Tensive
    compressive_load_Ratio = total_Load / avg_Compressive
    avg_tensive_opt = tensive_load_Ratio / total_length
    avg_compressive_opt = compressive_load_Ratio / total_length
    max_tensive_Ratio = total_Load / max_Tensive
    max_compressive_Ratio = total_Load / max_Compressive
    max_tensive_opt = max_tensive_Ratio / total_length  
    max_compressive_opt = max_compressive_Ratio / total_length
    length_times_max_Force = max_Force * total_length
    avg_force_over_Length = avg_Force * total_length
    
    print("Total length of members: ", total_length)
    print('Max Force: ', max_Force)
    print("Average force per member: ", avg_Force)
    print("Max tensive: ", max_Tensive)
    print("Max compressive: ", max_Compressive )
    print("Avg.force optimization rating: ", length_Opt)
    print("Max force optimization: ", max_force_Opt)
    print("Average tension: ", avg_Tensive)
    print("Average compression", avg_Compressive)
    print("H:S: ", height_to_span)
    
    outFile = "Lenticular.sym.txt"
    resultFile = open(outFile, 'w')

    n = 0
    for i in range(len(X) - 3):
        element = str(members[i].pair)
        result = str(X[i])
        resultFile.write(element)
        resultFile.write(' : ')
        resultFile.write(result)
        resultFile.write('\n')
        n = n + 1
    
    total_Load = str(total_Load)
    length_Opt = str(length_Opt)
    max_Force = str(max_Force)
    total_length = str(total_length)
    avg_Force = str(avg_Force)
    total_length = str(total_length)
    max_Tensive = str(max_Tensive)
    max_Compressive = str(max_Compressive)
    avg_Tensive = str(avg_Tensive)
    avg_Compressive = str(avg_Compressive)
    max_force_Ratio = str(max_force_Ratio)
    ext_load_ratio = str(ext_load_ratio)
    tensive_load_Ratio = str(tensive_load_Ratio)
    compressive_load_Ratio = str(compressive_load_Ratio)
    max_tensive_Ratio = str(max_tensive_Ratio)
    max_compressive_Ratio = str(max_compressive_Ratio)
    max_force_Opt = str(max_force_Opt)
    max_tensive_opt = str(max_tensive_opt)
    max_compressive_opt = str(max_compressive_opt)
    avg_tensive_opt = str(avg_tensive_opt)
    avg_compressive_opt = str(avg_compressive_opt)
    height_to_span = str(height_to_span)
    
        
    resultFile.write('\n')

    resultFile.write("Total load: ")
    resultFile.write(total_Load)
    resultFile.write('\n')
    
    resultFile.write("Joints loaded: ")
    resultFile.write('\n')
    resultFile.write(loadString)
    resultFile.write('\n')

    resultFile.write("Length of members: ")
    resultFile.write(total_length)
    resultFile.write('\n')
    
    resultFile.write("Average force per member: ")
    resultFile.write(avg_Force)
    resultFile.write('\n')
    
    resultFile.write("Max force: ")
    resultFile.write(max_Force)
    resultFile.write('\n')

    resultFile.write("Max tensive force: ")
    resultFile.write(max_Tensive)
    resultFile.write('\n')

    resultFile.write("Avg. tensive force: ")
    resultFile.write(avg_Tensive)
    resultFile.write('\n')

    resultFile.write("Max compressive force: ")
    resultFile.write(max_Compressive)
    resultFile.write('\n')

    resultFile.write("Avg. compressive force: ")
    resultFile.write(avg_Compressive)
    resultFile.write('\n')

    resultFile.write("Load / max force: ")
    resultFile.write(max_force_Ratio)
    resultFile.write('\n')

    resultFile.write("Load / avg. force: ")
    resultFile.write(ext_load_ratio)
    resultFile.write('\n')

    resultFile.write("Load / avg. tensile force: ")
    resultFile.write(tensive_load_Ratio)
    resultFile.write('\n')

    resultFile.write("Load / avg. compressive force: ")
    resultFile.write(compressive_load_Ratio)
    resultFile.write('\n')
    
    resultFile.write("Load / max tensile force: ")
    resultFile.write(max_tensive_Ratio)
    resultFile.write('\n')

    resultFile.write("Load / max compressive force: ")
    resultFile.write(compressive_load_Ratio)
    resultFile.write('\n')

    resultFile.write("Average force optimization: ")
    resultFile.write(length_Opt)
    resultFile.write('\n')

    resultFile.write("Max force optimization: ")
    resultFile.write(max_force_Opt)
    resultFile.write('\n')

    resultFile.write("Avg. tensile force optimization: ")
    resultFile.write(avg_tensive_opt)
    resultFile.write('\n')

    resultFile.write("Avg. compressive force optimization: ")
    resultFile.write(avg_compressive_opt)
    resultFile.write('\n')
    
    resultFile.write("Max tensive force optimization: ")
    resultFile.write(max_tensive_opt)
    resultFile.write('\n')
    
    resultFile.write("Max compressive optimization: ")
    resultFile.write(max_compressive_opt)
    resultFile.write('\n')

    resultFile.write("Height to span ratio: ")
    resultFile.write(height_to_span)
    
    
    resultFile.close

main()

